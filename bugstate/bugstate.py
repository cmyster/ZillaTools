"""
This script goes over lists of bugs per predefined bugzilla query and outputs
a CSV with data to be later digested elsewhere.
"""
from __future__ import print_function
from bugzilla import RHBugzilla

# Local helpers
import functions
import data


BZ = RHBugzilla(data.URL)

# This first line of output serves as columns titles.
print('DFG,Version,Total,Filtered,To ON_QA,To VERIFIED,AVG to CLOSED,URL')
for dfg in data.DFGS:
    for version in data.VERSIONS:
        q = functions.get_query(version, dfg)

        # This is where BZ is being queried.
        bugs = BZ.query(q)

        # If no bugs were found, no need to calculate, just break iteration.
        if not bugs:
            print('{},{},,,,,,'.format(dfg, version[0]))
            continue

        # Base URL to report with quick search.
        link = data.QUICKSEARCH

        # Some integers to help calculate times.
        on_qa_bugs = 0
        verified_bugs = 0
        closed_bugs = 0

        time_to_on_qa = 0
        time_to_verify = 0
        time_to_close = 0

        average_on_qa_time = 0
        average_verify_time = 0
        average_close_time = 0

        ok_bugs = 1
        for bug in bugs:
            if bug.resolution not in data.BAD_STATUS:
                link += '{}%2C'.format(bug.id)
                status_times = functions.get_status_times(
                    bug.get_history_raw())
                new_time = functions.get_datetime(bug.creation_time.value)
                int_new_time = functions.get_int_datetime(new_time)
                status_times['NEW'] = int_new_time

                if 'ON_QA' in status_times.keys():
                    on_qa_bugs += 1
                    time_to_on_qa += (status_times['ON_QA'] -
                                      status_times['NEW'])

                # Bugs that skip ON_QA are not used.
                if 'VERIFIED' in status_times.keys() \
                        and 'ON_QA' in status_times.keys():
                    verified_bugs += 1
                    time_to_verify += (status_times['VERIFIED'] -
                                       status_times['ON_QA'])

                # Bugs that were closed due to an issue with the bug are not
                # used.
                if 'CLOSED' in status_times.keys():
                    closed_bugs += 1
                    time_to_close += (status_times['CLOSED'] -
                                      status_times['NEW'])

                ok_bugs += 1

        # Removing last ',' from the link.
        link = link[:-3]

        # If there are no bugs, keep the link empty.
        if on_qa_bugs == 0 and verified_bugs == 0 and closed_bugs == 0:
            link = ''

        # In case of 0 bugs, print nothing. Else, devide time by number of bugs
        # by 86400 which is the number of seconds in one day.
        if on_qa_bugs == 0:
            final_onq = ''
        else:
            final_onq = time_to_on_qa / on_qa_bugs / 86400
        if verified_bugs == 0:
            final_ver = ''
        else:
            final_ver = time_to_verify / verified_bugs / 86400
        if closed_bugs == 0:
            final_cls = ''
        else:
            final_cls = time_to_close / closed_bugs / 86400

        print('{},{},{},{},{},{},{},{}'.format(
            dfg, version[0], len(bugs), ok_bugs, final_onq,
            final_ver, final_cls, link))
