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
                 o1='substring',
                 v1='DFG:{}'.format(dfg),
                 f2='component',
                 o2='notsubstring',
                 v2='doc',
                 keywords='FutureFeature, Tracking, Documentation',
                 keywords_type='nowords',
                 include_fields=common_data.INCLUDE_FIELDS)
    return query


def get_on_qa_query(username):
    # type: (str) -> dict
    """
    Returns a query of all bugs that are ON_QA for a qa_contact.
    :param username: str
    :rtype: dict
    """
    query = dict(bug_status='ON_QA',
                 qa_contact='{}{}'.format(username, common_data.RHDT))

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
             'v1': '{}{}'.format(username, common_data.RHDT)}
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
                 v1='{}{}'.format(username, common_data.RHDT))

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
                 v1='{}{}'.format(username, common_data.RHDT))

    return query


def get_totals(logfile, version, dfgs):
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

    if dfgs == 0:
        return '0,0,0,0,0'
    else:
        return '{},{},{},{},{}'.format(
            total / dfgs, goods / dfgs, on_qa / dfgs, verify / dfgs,
            close / dfgs)
