from datetime import datetime

from data import bug_status


# Returns a datetime from the time format used by BZ.
def get_datetime(bz_time):
    dt = datetime.strptime(bz_time, '%Y%m%dT%H:%M:%S')
    return dt


# Returns an int representation of a datetime.
def get_int_datetime(dt):
    return int(dt.strftime('%s'))


# Returns average time message.
def get_average_time_msg(change_time, closed_bugs, msg):
    average = datetime.fromtimestamp(change_time / closed_bugs)
    # years = (eval(average.strftime('%Y')) - 1970)
    months = average.strftime('%m')
    days = average.strftime('%d')
    message = (
        'On average it took {} months and {} days {}.').format(
        months, days, msg)
    return message


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


# Return the delta for a bug to reach from new to on_qa.
def get_state_time_delta(hist_times, from_state, to_state):
    t = 0
    for time, state in hist_times.items():
        if state == from_state:
            t = time
        if state == to_state:
            return time - t
