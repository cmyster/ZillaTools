from datetime import datetime

from data import bug_status


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
