#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015, 2016 Panu Lahtinen

# Author(s): Panu Lahtinen

#   Panu Lahtinen <panu.lahtinen@fmi.fi>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Gather GEO stationary segments, or polar satellite granules for one
timestep, and send them in a bunch as a dataset.
"""

import datetime as dt
import logging
import logging.handlers
import os.path
import Queue
import time
from collections import OrderedDict
from six.moves.configparser import RawConfigParser, NoOptionError
from six.moves.urllib.parse import urlparse, urlunparse

from posttroll import message, publisher
from posttroll.listener import ListenerContainer
from trollsift import Parser, compose

SLOT_NOT_READY = 0
SLOT_READY = 1
SLOT_READY_BUT_WAIT_FOR_MORE = 2
SLOT_OBSOLETE_TIMEOUT = 3

DO_NOT_COPY_KEYS = ("uid", "uri", "channel_name", "segment", "sensor")
REMOVE_TAGS = {'path', 'segment'}


class SegmentGatherer(object):

    """Gatherer for geostationary satellite segments and multifile polar
    satellite granules."""

    def __init__(self, config, section):
        self._config = config
        self._section = section
        topics = config.get(section, 'topics').split()

        try:
            nameservers = config.get(section, 'nameserver')
            nameservers = nameservers.split()
        except (NoOptionError, ValueError):
            nameservers = []

        try:
            addresses = config.get(section, 'addresses')
            addresses = addresses.split()
        except (NoOptionError, ValueError):
            addresses = None

        try:
            publish_port = config.get(section, 'publish_port')
        except NoOptionError:
            publish_port = 0

        try:
            services = config.get(section, 'services').split()
        except (NoOptionError, ValueError):
            services = ""

        self._listener = ListenerContainer(topics=topics, addresses=addresses
                                           services=services)
        self._publisher = publisher.NoisyPublisher("segment_gatherer",
                                                   port=publish_port,
                                                   nameservers=nameservers)
        self._subject = config.get(section, "publish_topic")
        self._pattern = config.get(section, 'pattern')
        self._parser = Parser(self._pattern)
        try:
            self._time_tolerance = config.getint(section, "time_tolerance")
        except NoOptionError:
            self._time_tolerance = 30
        try:
            self._timeliness = dt.timedelta(seconds=config.getint(section,
                                                                  "timeliness"))
        except (NoOptionError, ValueError):
            self._timeliness = dt.timedelta(seconds=1200)

        try:
            self._num_files_premature_publish = \
                config.getint(section, "num_files_premature_publish")
        except (NoOptionError, ValueError):
            self._num_files_premature_publish = -1

        self.slots = OrderedDict()

        self.time_name = config.get(section, 'time_name')

        self.logger = logging.getLogger("segment_gatherer")
        self._loop = False
        self._providing_server = None
        if config.has_option(section, 'providing_server'):
            self._providing_server = config.get(section, 'providing_server')

    def _clear_data(self, time_slot):
        """Clear data."""
        if time_slot in self.slots:
            del self.slots[time_slot]

    def _init_data(self, mda):
        """Init wanted, all and critical files"""
        # Init metadata struct
        metadata = mda.copy()
        metadata['dataset'] = []

        time_slot = str(metadata[self.time_name])
        self.logger.debug("Adding new slot: %s", time_slot)
        self.slots[time_slot] = {}
        self.slots[time_slot]['metadata'] = metadata.copy()

        # Critical files that are required, otherwise production will fail.
        # If there are no critical files, empty set([]) is used.
        try:
            critical_segments = self._config.get(self._section,
                                                 "critical_files")
            self.slots[time_slot]['critical_files'] = \
                self._compose_filenames(time_slot, critical_segments)
        except (NoOptionError, ValueError):
            self.slots[time_slot]['critical_files'] = set([])

        # These files are wanted, but not critical to production
        self.slots[time_slot]['wanted_files'] = \
            self._compose_filenames(time_slot,
                                    self._config.get(self._section,
                                                     "wanted_files"))
        # Name of all the files
        self.slots[time_slot]['all_files'] = \
            self._compose_filenames(time_slot,
                                    self._config.get(self._section,
                                                     "all_files"))

        self.slots[time_slot]['received_files'] = set([])
        self.slots[time_slot]['delayed_files'] = dict()
        self.slots[time_slot]['missing_files'] = set([])
        self.slots[time_slot]['timeout'] = None
        self.slots[time_slot]['files_till_premature_publish'] = \
            self._num_files_premature_publish

    def _compose_filenames(self, time_slot, itm_str):
        """Compose filename set()s based on a pattern and item string.
        itm_str is formated like ':PRO,:EPI' or 'VIS006:8,VIS008:1-8,...'"""

        # Empty set
        result = set()

        # Get copy of metadata
        meta = self.slots[time_slot]['metadata'].copy()

        # Replace variable tags (such as processing time) with
        # wildcards, as these can't be forecasted.
        try:
            meta = _copy_without_ignore_items(
                meta, ignored_keys=self._config.get(self._section,
                                                    'variable_tags').split(','))
        except NoOptionError:
            pass

        for itm in itm_str.split(','):
            channel_name, segments = itm.split(':')
            segments = segments.split('-')
            if len(segments) > 1:
                format_string = '%d'
                if len(segments[0]) > 1 and segments[0][0] == '0':
                    format_string = '%0' + str(len(segments[0])) + 'd'
                segments = [format_string % i for i in range(int(segments[0]),
                                                             int(segments[-1]) + 1)]
            meta['channel_name'] = channel_name
            for seg in segments:
                meta['segment'] = seg
                fname = self._parser.globify(meta)
                result.add(fname)

        return result

    def _publish(self, time_slot, missing_files_check=True):
        """Publish file dataset and reinitialize gatherer."""

        data = self.slots[time_slot]

        # Diagnostic logging about delayed ...
        delayed_files = data['delayed_files']
        if len(delayed_files) > 0:
            file_str = ''
            for key in delayed_files:
                file_str += "%s %f seconds, " % (key, delayed_files[key])
            self.logger.warning("Files received late: %s",
                                file_str.strip(', '))

        if missing_files_check:
            # and missing files
            missing_files = data['all_files'].difference(
                data['received_files'])
            if len(missing_files) > 0:
                self.logger.warning("Missing files: %s",
                                    ', '.join(missing_files))

        # Remove tags that are not necessary for datasets
        for tag in REMOVE_TAGS:
            try:
                del data['metadata'][tag]
            except KeyError:
                pass

        msg = message.Message(self._subject, "dataset", data['metadata'])
        self.logger.info("Sending: %s", str(msg))
        self._publisher.send(str(msg))

        # self._clear_data(time_slot)

    def set_logger(self, logger):
        """Set logger."""
        self.logger = logger

    def update_timeout(self, slot):
        slot['timeout'] = dt.datetime.utcnow() + self._timeliness
        time_slot = str(slot['metadata'][self.time_name])
        self.logger.info("Setting timeout to %s for slot %s.",
                         str(slot['timeout']),
                         time_slot)

    def slot_ready(self, slot):
        """Determine if slot is ready to be published."""
        # If no files have been collected, return False
        if len(slot['received_files']) == 0:
            return SLOT_NOT_READY

        time_slot = str(slot['metadata'][self.time_name])

        wanted_and_critical_files = slot[
            'wanted_files'].union(slot['critical_files'])
        num_wanted_and_critical_files_received = len(
            wanted_and_critical_files & slot['received_files'])

        self.logger.debug("Got %s wanted or critical files in slot %s.",
                          num_wanted_and_critical_files_received,
                          time_slot)

        if num_wanted_and_critical_files_received \
                == slot['files_till_premature_publish']:
            slot['files_till_premature_publish'] = -1
            return SLOT_READY_BUT_WAIT_FOR_MORE

        # If all wanted files have been received, return True
        if wanted_and_critical_files.issubset(
                slot['received_files']):
            self.logger.info("All files received for slot %s.",
                             time_slot)
            return SLOT_READY

        if slot['timeout'] is None:
            self.update_timeout(slot)

        if slot['timeout'] < dt.datetime.utcnow():
            if slot['critical_files'].issubset(slot['received_files']):
                # All critical files have been received
                # Timeout reached, collection ready
                self.logger.info("Timeout occured, required files received "
                                 "for slot %s.", time_slot)
                return SLOT_READY
            else:
                # Timeout reached, collection is obsolete
                self.logger.warning("Timeout occured and required files "
                                    "were not present, data discarded for "
                                    "slot %s.",
                                    time_slot)
                return SLOT_OBSOLETE_TIMEOUT

        # Timeout not reached, wait for more files
        return SLOT_NOT_READY

    def run(self):
        """Run SegmentGatherer"""
        self._publisher.start()
        self._loop = True
        while self._loop:
            # Check if there are slots ready for publication
            slots = self.slots.copy()
            for slot in slots:
                slot = str(slot)
                status = self.slot_ready(slots[slot])
                if status == SLOT_READY:
                    # Collection ready, publish and remove
                    self._publish(slot)
                    self._clear_data(slot)
                if status == SLOT_READY_BUT_WAIT_FOR_MORE:
                    # Collection ready, publish and but wait for more
                    self._publish(slot, missing_files_check=False)
                elif status == SLOT_OBSOLETE_TIMEOUT:
                    # Collection unfinished and obslote, discard
                    self._clear_data(slot)
                else:
                    # Collection unfinished, wait for more data
                    pass

            # Check listener for new messages
            msg = None
            try:
                msg = self._listener.output_queue.get(True, 1)
            except AttributeError:
                msg = self._listener.queue.get(True, 1)
            except KeyboardInterrupt:
                self.stop()
                continue
            except Queue.Empty:
                continue

            if msg.type == "file":
                if (self._providing_server and
                        self._providing_server != msg.host):
                    continue

                self.logger.info("New message received: %s", str(msg))
                self.process(msg)

    def stop(self):
        """Stop gatherer."""
        self.logger.info("Stopping gatherer.")
        self._loop = False
        if self._listener is not None:
            self._listener.stop()
        if self._publisher is not None:
            self._publisher.stop()

    def process(self, msg):
        """Process message"""
        try:
            mda = self._parser.parse(msg.data["uid"])
        except ValueError:
            self.logger.debug("Unknown file, skipping.")
            return

        metadata = {}

        # Use values parsed from the filename as basis
        for key in mda:
            if key not in DO_NOT_COPY_KEYS:
                metadata[key] = mda[key]

        # Update with data given in the message
        for key in msg.data:
            if key not in DO_NOT_COPY_KEYS:
                metadata[key] = msg.data[key]

        time_slot = self._find_time_slot(metadata[self.time_name])

        # Init metadata etc if this is the first file
        if time_slot not in self.slots:
            self._init_data(metadata)
            slot = self.slots[time_slot]
            to_add = []
            for filename in slot['all_files']:
                if filename == msg.data['uid']:
                    continue
                url = urlparse(msg.data['uri'])
                path = os.path.join(os.path.dirname(url.path), filename)
                if not os.path.exists(path):
                    continue
                new_url = list(url)
                new_url[2] = path
                uri = urlunparse(new_url)

                slot['metadata']['dataset'].append({'uri': uri,
                                                    'uid': filename})
                to_add.append(filename)

            slot['received_files'].update(to_add)
            if to_add:
                self.logger.debug("Some files were already received %s",
                                  str(to_add))
                self.update_timeout(slot)

        slot = self.slots[time_slot]

        # Replace variable tags (such as processing time) with
        # wildcards, as these can't be forecasted.
        try:
            mda = _copy_without_ignore_items(
                mda, ignored_keys=self._config.get(self._section,
                                                   'variable_tags').split(','))
        except NoOptionError:
            pass

        mask = self._parser.globify(mda)

        if mask in slot['received_files']:
            return

        # Add uid and uri
        slot['metadata']['dataset'].append({'uri': msg.data['uri'],
                                            'uid': msg.data['uid']})

        # Collect all sensors, not only the latest
        if type(msg.data["sensor"]) not in (tuple, list, set):
            msg.data["sensor"] = [msg.data["sensor"]]
        for sensor in msg.data["sensor"]:
            if "sensor" not in slot["metadata"]:
                slot["metadata"]["sensor"] = []
            if sensor not in slot["metadata"]["sensor"]:
                slot["metadata"]["sensor"].append(sensor)

        # If critical files have been received but the slot is
        # not complete, add the file to list of delayed files
        if len(slot['critical_files']) > 0 and \
           slot['critical_files'].issubset(slot['received_files']):
            delay = dt.datetime.utcnow() - (slot['timeout'] - self._timeliness)
            slot['delayed_files'][msg.data['uid']] = delay.total_seconds()

        # Add to received files
        slot['received_files'].add(mask)

    def _find_time_slot(self, time_obj):
        """Find time slot and return the slot as a string.  If no slots are
        close enough, return *str(time_obj)*"""
        for slot in self.slots:
            time_slot = self.slots[slot]['metadata'][self.time_name]
            time_diff = time_obj - time_slot
            if abs(time_diff.total_seconds()) < self._time_tolerance:
                self.logger.debug("Found existing time slot, using that")
                return str(time_slot)

        return str(time_obj)


def _copy_without_ignore_items(the_dict, ignored_keys=['ignore']):
    """
    get a copy of *the_dict* without entries having substring
    'ignore' in key
    """
    new_dict = {}
    for (key, val) in list(the_dict.items()):
        if key not in ignored_keys:
            new_dict[key] = val
    return new_dict


def arg_parse():
    '''Handle input arguments.
    '''
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log",
                        help="File to log to (defaults to stdout)",
                        default=None)
    parser.add_argument("-v", "--verbose", help="print debug messages too",
                        action="store_true")
    parser.add_argument("-c", "--config", help="config file to be used")
    parser.add_argument("-C", "--config_item", help="config item to use")

    return parser.parse_args()


def main():
    '''Main. Parse cmdline, read config etc.'''

    args = arg_parse()

    config = RawConfigParser()
    config.read(args.config)

    print("Setting timezone to UTC")
    os.environ["TZ"] = "UTC"
    time.tzset()

    handlers = []
    if args.log:
        handlers.append(
            logging.handlers.TimedRotatingFileHandler(args.log,
                                                      "midnight",
                                                      backupCount=7))

    handlers.append(logging.StreamHandler())

    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    for handler in handlers:
        handler.setFormatter(logging.Formatter("[%(levelname)s: %(asctime)s :"
                                               " %(name)s] %(message)s",
                                               '%Y-%m-%d %H:%M:%S'))
        handler.setLevel(loglevel)
        logging.getLogger('').setLevel(loglevel)
        logging.getLogger('').addHandler(handler)

    logging.getLogger("posttroll").setLevel(logging.INFO)
    logger = logging.getLogger("segment_gatherer")

    gatherer = SegmentGatherer(config, args.config_item)
    gatherer.set_logger(logger)
    gatherer.run()


if __name__ == "__main__":
    main()
