"""
Basic helper methods for the main business logic.
"""
import common_data


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
                 v1='{}'.format(dfg),
                 f2='component',
                 o2='notsubstring',
                 v2='documentation',
                 keywords='FutureFeature, Tracking, Documentation',
                 keywords_type='nowords',
                 include_fields=common_data.INCLUDE_FIELDS)
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
        print ('IOError: {0} - {1}').format(e.errno, e.strerror)
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
