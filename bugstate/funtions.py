from datetime import datetime


# Returns time delta from the time formats used by BZ.
def get_delta(status_a, status_b):
    a = datetime.strptime(status_a, '%Y%m%dT%H:%M:%S')
    b = datetime.strptime(status_b, '%Y%m%dT%H:%M:%S')
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
