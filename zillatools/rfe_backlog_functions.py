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
        query_format='advanced',
        keywords='Documentation, Tracking',
        keywords_type='nowords',
        f1='cf_internal_whiteboard',
        f2='keywords',
        f3='component',
        n3='1',
        o1='substring',
        o2='substring',
        o3='equals',
        v1='{}'.format(dfg),
        v2='FutureFeature',
        v3='documentation',
    )
    return query
