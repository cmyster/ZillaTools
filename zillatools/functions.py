"""
Basic helper functions for the main business logic.
"""
from datetime import datetime
from data import BUG_STATUS
from data import INCLUDE_FIELDS
from data import RHDT


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
                        status_time[status] = int(
                            (datetime.strptime(
                                event['when'].value,
                                '%Y%m%dT%H:%M:%S')).strftime('%s'))
    return status_time


def get_bs_query(version, dfg):
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


def get_on_qa_query(username):
    # type: (str) -> dict
    """
    Returns a query of all bugs that are ON_QA for a qa_contact.
    :param username: str
    :rtype: dict
    """
    query = dict(bug_status='ON_QA',
                 qa_contact='{}{}'.format(username, RHDT))

    return query


def get_open_query(username):
    # type: (str) -> dict
    """
    Returns a query of all bugs that are still open for a qa_contact.
    :param username: str
    :rtype: dict
    """
    query = {'bug_status': 'NEW',
             'bug_status': 'ASSIGNED',
             'bug_status': 'POST',
             'bug_status': 'MODIFIED',
             'bug_status': 'ON_DEV',
             'f1': 'qa_contact',
             'o1': 'equals',
             'v1': '{}{}'.format(username, RHDT)}
    return query


def get_reported_query(username):
    # type: (str) -> dict
    """
    Returns a query of all bugs that were reported by a qa_contact.
    :param username: str
    :rtype: dict
    """
    query = dict(f1='reporter',
                 o1='equals',
                 v1='{}{}'.format(username, RHDT))

    return query


def get_needinfo_query(username):
    # type: (str) -> dict
    """
    Returns a query of all bugs that have a need info flag on a qa_contact.
    :param username: str
    :rtype: dict
    """
    query = dict(f1='requestees.login_name',
                 o1='equals',
                 v1='{}{}'.format(username, RHDT))

    return query


def get_bs_totals(logfile, version, dfgs):
    # type: (str, str, int) -> str
    """
    Reading lines of relevant versions from log and returning their average.
    :type logfile: str
    :type version: str
    :type dfgs: int
    :rtype: str
    """
    try:
        log = open(logfile, "r")
        log.close()
    except IOError as e:
        print 'IOError: {0} - {1}'.format(e.errno, e.strerror)
        exit(1)

    total = 0
    goods = 0
    on_qa = 0
    verify = 0
    close = 0
    with open(logfile, 'r') as log:
        for line in log:
            if version in line.split(",")[1]:
                total += int(line.split(",")[2])
                goods += int(line.split(",")[3])
                on_qa += int(line.split(",")[4])
                verify += int(line.split(",")[5])
                close += int(line.split(",")[6])
    log.close()

    return '{},{},{},{},{}'.format(total / dfgs,
                                   goods / dfgs,
                                   on_qa / dfgs,
                                   verify / dfgs,
                                   close / dfgs)


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
