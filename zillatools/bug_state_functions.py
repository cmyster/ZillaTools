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


def get_totals(logfile, version):
    # type: (str, str, int) -> str
    """
    Reading lines of relevant versions from log and returning their average.
    :type logfile: str
    :type version: str
    :rtype: str
    """
    try:
        log = open(logfile, "r")
        log.close()
    except IOError as e:
        print("IOError: {0} - {1}".format(e.errno, e.strerror))
        exit(1)

    total = 0
    goods = 0
    assigned = 0
    on_dev = 0
    post = 0
    modified = 0
    on_qa = 0
    verified = 0
    pending = 0
    close = 0
    dfgs = 0
    with open(logfile, 'r') as log:
        for line in log:
            if version in line.split(",")[1]:
                if int(line.split(",")[2]) == 0:
                    continue
                else:
                    dfgs += 1
                    total += int(line.split(",")[2])
                    goods += int(line.split(",")[3])
                    assigned += int(line.split(",")[4])
                    on_dev += int(line.split(",")[5])
                    post += int(line.split(",")[6])
                    modified += int(line.split(",")[7])
                    on_qa += int(line.split(",")[8])
                    verified += int(line.split(",")[9])
                    pending += int(line.split(",")[10])
                    close += int(line.split(",")[11])
    log.close()

    if dfgs == 0:
        return '0,0,0,0,0,0,0,0,0,0'
    else:
        return '{},{},{},{},{},{},{},{},{},{}'.format(
            total / dfgs,
            goods / dfgs,
            assigned / dfgs,
            on_dev / dfgs,
            post / dfgs,
            post / dfgs,
            on_qa / dfgs,
            verified / dfgs,
            pending / dfgs,
            close / dfgs)
