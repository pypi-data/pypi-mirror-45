from datetime import datetime


def parse_iso_datetime(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')
