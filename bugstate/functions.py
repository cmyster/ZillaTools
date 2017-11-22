from datetime import datetime
from collections import OrderedDict

from data import bug_status


# Returns a datetime from the time format used by BZ.
def _get_datetime(bz_time):
    dt = datetime.strptime(bz_time, '%Y%m%dT%H:%M:%S')
    return dt


# Returns time delta as int.
def get_delta(status_a, status_b):
    a = _get_datetime(status_a)
    b = _get_datetime(status_b)
    delta = int(b.strftime('%s')) - int(a.strftime('%s'))
    return delta


# Returns the average time to close a bug message.
def get_average_time(time_to_close, closed_bugs, version):
    average = datetime.fromtimestamp(time_to_close / closed_bugs)
    years = (eval(average.strftime('%Y')) - 1970)
    months = average.strftime('%m')
    days = average.strftime('%d')
    message = (
        'On average it took {} years, {} months and {} days '
        'to close a bug in rhosp {}.').format(
            years, months, days, version)
    return message


# Returns a dict of time and status per bug.
def get_status_times(raw_history):
    status_change = {}
    for events in raw_history['bugs']:
        for event in events['history']:
            for change in event['changes']:
                for status in bug_status:
                    if status == change['removed']:
                        event_time = _get_datetime(event['when'].value)
                        status_change[int(event_time.strftime('%s'))] = status
    return OrderedDict(sorted(status_change.items()))


# Return the delta for a bug to reach from new to on_qa.
