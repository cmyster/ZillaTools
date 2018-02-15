"""
Basic helper methods for the main business logic.
"""
from common_data import INCLUDE_FIELDS


def get_query(dfg):
    # type: (str) -> dict
    """
    Building a query usable by bugzilla.
    :type dfg: str
    :rtype: dict
    """
    query = dict(
        include_fields=INCLUDE_FIELDS,
        classification='Red Hat',
        product='Red Hat OpenStack',
        keywords='Documentation, FutureFeature, Tracking',
        keywords_type='nowords',
        order='Bug Number',
        query_format='advanced',
        f1='cf_internal_whiteboard',
        f2='component',
        f3='resolution',
        f4='resolution',
        f5='resolution',
        f6='resolution',
        f7='resolution',
        f8='resolution',
        f9='resolution',
        n2='1',
        n3='1',
        n4='1',
        n5='1',
        n6='1',
        n7='1',
        n8='1',
        n9='1',
        o1='substring',
        o2='equals',
        o3='equals',
        o4='equals',
        o5='equals',
        o6='equals',
        o7='equals',
        o8='equals',
        o9='equals',
        v1='{}'.format(dfg),
        v2='documentation',
        v3='NOTABUG',
        v4='WONTFIX',
        v5='DEFERRED',
        v6='WORKSFORME',
        v7='DUPLICATE',
        v8='CANTFIX',
        v10='INSUFFICIENT_DATA',
    )
    return query
