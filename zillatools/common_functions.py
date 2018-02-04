"""
Basic helper methods for the main business logic.
"""
from datetime import datetime
import common_data


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
                for status in common_data.BUG_STATUS:
                    if status == change['added']:
                        status_time[status] = int(
                            (datetime.strptime(
                                event['when'].value,
                                '%Y%m%dT%H:%M:%S')).strftime('%s'))
    return status_time


def get_log_name(argv, name):
    # type: (list, str) -> str
    """
    Defining a logfile and making sure its writable.
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
                    print 'IOError: {0} - {1}'.format(e.errno, e.strerror)
                    exit(1)
        except IndexError as e:
            print 'Missing argument\n{}'.format(e)
            exit(1)

    # If there are more arguments, print ignore message.
    if len(argv) > 3:
        print 'Ignoring arguments: ',
        for i in range(3, len(argv)):
            print "{} ".format(argv[i]),
        print ''

    print 'Data is saved to {}'.format(log_file)

    return log_file
