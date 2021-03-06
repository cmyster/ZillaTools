"""
Basic helper methods for the main business logic.
"""
from datetime import datetime, timedelta
import common_data


def get_status_times(raw_history, creation_time):
    # type: (dict, str) -> dict
    """
    Parsing a bug's raw history and returning a dictionary of the bug's change
    over time with a status,date format.
    :type raw_history: dict
    :type creation_time: str
    :rtype: dict
    """
    status_time = {}
    for events in raw_history['bugs']:
        for event in events['history']:
            for change in event['changes']:
                for status in common_data.BUG_STATUS:
                    if status == change['added']:
                        status_time[status] = int(
                            (datetime.strptime(
                                event['when'].value,
                                '%Y%m%dT%H:%M:%S')).strftime('%s'))
    new_time = datetime.strptime(creation_time, '%Y%m%dT%H:%M:%S')
    int_new_time = int(new_time.strftime('%s'))
    status_time['NEW'] = int_new_time
    return status_time


def convert_bz_str_epoch(str_date):
    # type: (str) -> int
    """
    Gets a date in string format (YYYY-MM-DD) and returns a datetime object.
    :type str_date: str
    :rtype: datetime
    """
    int_epoch = int(datetime.strptime(str_date, '%Y-%m-%d').strftime('%s'))
    return int_epoch


def get_log_name(argv, name):
    # type: (list, str) -> str
    """
    Defining a logfile and making sure its writeable.
    :type argv: list
    :type name: str
    :rtype: str
    """
    # Getting a default name first.
    log_file = name

    if '--file' in argv:
        try:
            if argv[argv.index('--file') + 1] is not str:
                log_file = argv[argv.index('--file') + 1]
                # Making sure that file is writeable
                try:
                    log = open("{}".format(log_file), "w")
                    log.close()
                except IOError as e:
                    print('IOError: {0} - {1}').format(e.errno, e.strerror)
                    exit(1)
        except IndexError as e:
            print('Missing argument\n{}').format(e)
            exit(1)

    # If there are more arguments, print ignore message.
    if len(argv) > 3:
        print('Ignoring arguments: '),
        for i in range(3, len(argv)):
            print("{} ").format(argv[i]),
        print('')

    print('Data is saved to {}').format(log_file)

    return log_file


def get_weeks_dates(start_date):
    # type: (str) -> list
    """
    Returns a list of strings ('YYYY-MM-DD',) dates from a range created from
    the previous Wednesday before start_date to the next Wednesday from today.
    :type start_date: str
    :rtype list
    """
    # Creating dates from Year/Month/Day from the first version's beginning
    # to the current date.
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.now()

    # Setting the starting date to the Wednesday prior to the beginning of the
    # first version.
    if int(start_date.strftime('%w')) < 3:
        start_date -= timedelta(days=(int(start_date.strftime('%w'))) + 4)
    if int(start_date.strftime('%w')) > 3:
        start_date -= timedelta(days=int(start_date.strftime('%w')))
        start_date += timedelta(days=3)
    # Setting the end date to the next Wednesday from today.
    if int(end_date.strftime('%w')) < 3:
        end_date -= timedelta(days=int(end_date.strftime('%w')))
        end_date += timedelta(days=3)
    if int(end_date.strftime('%w')) >= 3:
        end_date -= timedelta(days=int(end_date.strftime('%w')))
        end_date += timedelta(days=10)
    # Number of weeks to work on.
    weeks = (end_date - start_date).days / 7
    # Initialize the list with the first date.
    dates = [start_date.strftime('%Y-%m-%d')]

    for week in range(weeks):
        start_date += timedelta(weeks=1)
        dates.append(start_date.strftime('%Y-%m-%d'))

    return dates


def get_time_now():
    # type: (none) -> str
    """
    Returns now from datetime. This happens here so we don't need to include
    datetime in other classes.
    """
    now = str(datetime.now())
    return now
