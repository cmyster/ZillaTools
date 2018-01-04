from datetime import datetime

from data import bug_status
from data import include_fields


# Returns a datetime from the time format used by BZ.
def get_datetime(bz_time):
    dt = datetime.strptime(bz_time, '%Y%m%dT%H:%M:%S')
    return dt


# Returns an int representation of a datetime.
def get_int_datetime(dt):
    return int(dt.strftime('%s'))


# Returns a dict of time and status per bug.
def get_status_times(raw_history):
    status_time = {}
    for events in raw_history['bugs']:
        for event in events['history']:
            for change in event['changes']:
                for status in bug_status:
                    if status == change['added']:
                        event_time = get_datetime(event['when'].value)
                        status_time[status] = int(event_time.strftime('%s'))
    return status_time


# Return a query dict BZ can use.
def get_query(version, dfg):
    q = {
        'query_format': 'advanced',
        'classification': 'Red Hat',
        'product': 'Red Hat OpenStack',
        'chfield': '[Bug creation]',
        'version': '{}'.format(version[0]),
        'chfieldfrom': '{}'.format(version[1]),
        'chfieldto': '{}'.format(version[2]),
        'f1': 'cf_internal_whiteboard',
        'f2': 'keywords',
        'o1': 'substring',
        'o2': 'equals',
        'v1': 'DFG:{}'.format(dfg),
        'v2': 'FutureFeature',
        'n2': '1'
    }
    q['include_fields'] = include_fields
    return q
