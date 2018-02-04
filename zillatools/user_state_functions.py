"""
Basic helper methods for the main business logic.
"""
import common_data


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
