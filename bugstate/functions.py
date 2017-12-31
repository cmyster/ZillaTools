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
    q = {'chfield': '[Bug creation]',
         'chfieldfrom': '{}'.format(version[1]),
         'chfieldto': '{}'.format(version[2]),
         'classification': 'Red Hat',
         'f1': 'cf_internal_whiteboard',
         'f2': 'keywords',
         'f3': 'resolution',
         'f4': 'resolution',
         'f5': 'resolution',
         'f6': 'resolution',
         'f7': 'resolution',
         'f8': 'resolution',
         'f9': 'resolution',
         'n2': '1',
         'n3': '1',
         'n4': '1',
         'n5': '1',
         'n6': '1',
         'n7': '1',
         'n8': '1',
         'n9': '1',
         'o1': 'equals',
         'o2': 'equals',
         'o3': 'equals',
         'o4': 'equals',
         'o5': 'equals',
         'o6': 'equals',
         'o7': 'equals',
         'o8': 'equals',
         'o9': 'equals',
         'product': 'Red Hat OpenStack',
         'query_format': 'advanced',
         'target_release': '{}'.format(version[0]),
         'v1': 'DFG:{}'.format(dfg),
         'v2': 'FutureFeature',
         'v3': 'NOTABUG',
         'v4': 'WONTFIX',
         'v5': 'DEFERRED',
         'v6': 'WORKSFORME',
         'v7': 'DUPLICATE',
         'v8': 'CANTFIX',
         'v9': 'INSUFFICIENT_DATA'}
    q['include_fields'] = include_fields
    return q
