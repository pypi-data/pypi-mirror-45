import json
from urllib.parse import unquote_plus

import logging
from otest.proc import find_test_instances

logger = logging.getLogger(__name__)


class OutOfRange(Exception):
    pass


class AssignedPorts(object):
    def __init__(self, filename, min, max):
        self.filename = filename
        self.min = min
        self.max = max
        self._db = {}

    def make_key(self, *args):
        return ']['.join([unquote_plus(v) for v in args])

    def __setitem__(self, key, value):
        if '%' in key:
            key = unquote_plus(key)

        self._db[key] = value
        self.dump()

    def __getitem__(self, item):
        if "%" in item:
            item = unquote_plus(item)

        return self._db[item]

    def __delitem__(self, key):
        if '%' in key:
            key = unquote_plus(key)

        logger.info("Removed {}".format(key))
        del self._db[key]
        self.dump()

    def keys(self):
        return self._db.keys()

    def values(self):
        return self._db.values()

    def items(self):
        return self._db.items()

    def __contains__(self, item):
        if "%" in item:
            item = unquote_plus(item)
        return item in self._db

    def dump(self):
        fp = open(self.filename, 'w')
        fp.write(json.dumps(self._db))
        fp.close()

    def sync(self, test_script):
        running_processes = {}

        update = False
        inst = find_test_instances(test_script)
        if inst:
            for pid, info in inst.items():
                key = self.make_key(info["iss"], info["tag"])
                if key not in self._db:
                    self[key] = int(info["port"])
                    update = True
                running_processes[key] = pid

        if update:
            self.dump()

        return running_processes

    def load(self):
        try:
            _ass = open(self.filename, 'r').read()
        except FileNotFoundError:
            pass
        else:
            if _ass:
                # So not to write back to disc
                for key, val in json.loads(_ass).items():
                    self._db[key] = val

    def next_free_port(self, prev=0):
        if not prev:
            prev = self.min
        pl = list(self._db.values())
        if not pl:
            return prev
        else:
            _port = prev
            while _port <= self.max:
                if not _port in pl:
                    break
                _port += 1
            if _port > self.max:
                raise OutOfRange('Out of ports')
        return _port

    def register_port(self, *args):
        """
        Get an assigned port. If no one is assigned, find the next available.
        :param args: entity identifiers
        :return: Integer
        """
        eid = self.make_key(*args)

        try:
            # already registered ?
            _port = self._db[eid]
        except KeyError:
            if self._db == {}:
                _port = self.min
            else:
                _port = self.next_free_port()
            logger.info('Assigned port {} for {}'.format(_port, eid))
            self._db[eid] = _port
            self.dump()
        return _port
