"""
Basic helper functions for the main business logic.
"""
from datetime import datetime
from data import BUG_STATUS
from data import INCLUDE_FIELDS


def get_datetime(bz_time):
    # type: (str) -> datetime
    """
    Returns a datetime object from the date used in bugzilla.
    :type bz_time: str
    :rtype: datetime
    """
    return datetime.strptime(bz_time, '%Y%m%dT%H:%M:%S')


def get_int_datetime(date_time):
    # type: (datetime) -> int
    """
    Returns the number of seconds from EPOCH to a datetime object.
    :type date_time: datetime
    :rtype: int
    """
    return int(date_time.strftime('%s'))


def get_status_times(raw_history):
    # type: (dict) -> dict
    """
    Parsing a bug's raw history and returning a dictionary of the bug's change
    over time with a status,date format.
    :type raw_history: dict
    :rtype: dict
    """
    status_time = {}
    for events in raw_history['bugs']:
        for event in events['history']:
            for change in event['changes']:
                for status in BUG_STATUS:
                    if status == change['added']:
                        event_time = get_datetime(event['when'].value)
                        status_time[status] = int(event_time.strftime('%s'))
    return status_time


def get_query(version, dfg):
    # type: (list, str) -> dict
    """
    Building a query usable by bugzilla.
    :type version: list
    :type dfg: str
    :rtype: dict
    """
    query = dict(query_format='advanced',
                 classification='Red Hat',
                 product='Red Hat OpenStack',
                 chfield='[Bug creation]',
                 version='{}'.format(version[0]),
                 chfieldfrom='{}'.format(version[1]),
                 chfieldto='{}'.format(version[2]),
                 f1='cf_internal_whiteboard',
                 f2='keywords',
                 f3='keywords',
                 o1='substring',
                 o2='equals',
                 o3='equals',
                 v1='DFG:{}'.format(dfg),
                 v2='FutureFeature',
                 v3='Documentation',
                 n2='1',
                 n3='1',
                 include_fields=INCLUDE_FIELDS)
    return query
