from datetime import datetime
from ipaddress import ip_address
import re


LINE_REGEXP = re.compile(r'^(?P<ip>\d+(\.\d+){3}) - - '
                         r'\[(?P<timestamp>[^\]]+)\] "(?P<request>[^"]+)".*')
TIMESTAMP_FORMAT = '%d/%b/%Y:%H:%M:%S %z'


class LogDicts:

    def __init__(self, filename, line_regexp=LINE_REGEXP,
                 timestamp_format=TIMESTAMP_FORMAT):
        self._filename = filename
        self._line_regexp = line_regexp
        self._timestamp_format = timestamp_format
        self._entries = self._get_logfile_entries()

    def _get_logfile_entries(self):
        result = []
        with open(self._filename) as logfile:
            for line in logfile:
                match = self._line_regexp.match(line)
                if match:
                    timestamp = datetime.strptime(match.group('timestamp'),
                                                  self._timestamp_format)
                    data = {'ip_address': ip_address(match.group('ip')),
                            'timestamp': timestamp,
                            'request': match.group('request')}
                    result.append(data)
        return result

    def dicts(self, key=None):
        return self._get_dict_list(self._entries)

    def iterdicts(self, key=None):
        return iter(self.dicts(key))

    def earliest(self):
        return self._entries[0]

    def latest(self):
        return self._entries[-1]

    def for_ip(self, ip, key=None):
        ip = ip_address(ip)
        result = [e for e in self._entries if e['ip_address'] == ip]
        return self._get_dict_list(result, key)

    def for_request(self, text, key=None):
        result = [e for e in self._entries if text in e['request']]
        return self._get_dict_list(result, key)

    @staticmethod
    def _get_dict_list(dict_list, key=None):
        if key:
            return sorted(dict_list, key=key)
        return list(dict_list)
