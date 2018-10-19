from logfile_parser import log_to_list


LOGFILENAME = 'mini-access-log.txt'
LOG_FILE_LINE_COUNT = 206


def test_read_logs():
    log_list = log_to_list(LOGFILENAME)
    assert len(log_list) == LOG_FILE_LINE_COUNT


def got_a_list():
    log_list = log_to_list(LOGFILENAME)
    assert type(log_list) is list


def all_are_dicts():
    log_list = log_to_list(LOGFILENAME)
    assert all([type(x) is dict for x in log_list])


def test_check_keys():
    log_list = log_to_list(LOGFILENAME)
    assert set(log_list[0].keys()) == {'ip_address', 'timestamp', 'request'}


def test_check_values():
    log_list = log_to_list(LOGFILENAME)
    first_log_dict = log_list[0]

    assert first_log_dict['ip_address'] == '67.218.116.165'
    assert first_log_dict['timestamp'] == '30/Jan/2010:00:03:18 +0200'
    assert first_log_dict['request'] == 'GET /robots.txt HTTP/1.0'
