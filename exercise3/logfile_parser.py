import re


LINE_REGEXP = re.compile(r'^(?P<ip>\d+(\.\d+){3}) - - '
                         r'\[(?P<timestamp>[^\]]+)\] "(?P<request>[^"]+)".*')


def parse_logfile(filename):
    with open(filename) as logfile:
        for line in logfile:
            match = LINE_REGEXP.match(line)
            if match:
                data = {'ip_address': match.group('ip'),
                        'timestamp': match.group('timestamp'),
                        'request': match.group('request')}
                yield data


def log_to_list(filename):
    return list(parse_logfile(filename))
