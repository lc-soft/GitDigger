from datetime import datetime

def datetime_from_utc(datestr):
    return datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%SZ')
