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
    query = dict(
        f1='qa_contact',
        f2='OP',
        f3='bug_status',
        f4='bug_status',
        f5='bug_status',
        f6='bug_status',
        f7='bug_status',
        f9='CP',
        j2='OR',
        o1='substring',
        o3='equals',
        o4='equals',
        o5='equals',
        o6='equals',
        o7='equals',
        query_format='advanced',
        v1='{}{}'.format(username, common_data.RHDT),
        v3='NEW',
        v4='ASSIGNED',
        v5='POST',
        v6='MODIFIED',
        v7='ON_QA',
    )
    return query


def get_reported_query(username, version):
    # type: (str, str) -> dict
    """
    Returns a query of all bugs that were reported by a qa_contact
    in a specific version.
    :param username: str
    :param version: str
    :rtype: dict
    """
    query = dict(
        f1='reporter',
        o1='equals',
        v1='{}{}'.format(username, common_data.RHDT),
        version='{}'.format(version),
    )

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


def gen_per_version_headers():
    # type: (none) -> str
    """
    Returns a string to be used as CSV header that looks like:
    'version X,link,version Y,link, ...'
    :return: str
    """
    headers = ''
    for version in common_data.VERSIONS:
        headers += "reported in {},link,".format(version[0])
    return headers



