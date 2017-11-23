from __future__ import print_function
from sys import stdout
from bugzilla import RHBugzilla

# Local helpers
import functions
import data


bz_q = RHBugzilla(data.URL)

for version in data.versions:
    q = {
        'query_format': 'advanced',
        'f1': 'cf_internal_whiteboard',
        'v1': 'DFG:Upgrades',
        'j_top': 'OR',
        'o1': 'substring',
        'product': 'Red Hat OpenStack',
        'target_release': '{}'.format(version)
    }

    # No need for all possible fields, this saves time. ID must be there.
    q['include_fields'] = data.include_fields

    # This is where BZ is being queried.
    bugs = bz_q.query(q)

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

    print ('Version {}:'.format(version))
    num_bugs = len(bugs)
    counter = 1
    for bug in bugs:
        stdout.write('\rWorking on bug {} out of {}'.format(counter, num_bugs))
        status_times = functions.get_status_times(bug.get_history_raw())
        new_time = functions.get_datetime(bug.creation_time.value)
        int_new_time = functions.get_int_datetime(new_time)
        status_times['NEW'] = int_new_time

        if 'ON_QA' in status_times.keys():
            on_qa_bugs += 1
            time_to_on_qa += (status_times['ON_QA'] - status_times['NEW'])

        # Bugs that skip ON_QA are not used.
        if 'VERIFIED' in status_times.keys() and 'ON_QA' in status_times.keys():
            verified_bugs += 1
            time_to_verify += (status_times['VERIFIED'] - status_times['ON_QA'])

        # Bugs that were closed due to an issue with the bug are not used.
        if 'CLOSED' in status_times.keys() and bug.resolution not in data.bad_status:
            closed_bugs += 1
            time_to_close += (status_times['CLOSED'] - status_times['NEW'])

        stdout.flush()
        counter += 1

    stdout.write('\n')
    if on_qa_bugs > 0:
        average_on_qa_msg = functions.get_average_time_msg(
            time_to_on_qa, on_qa_bugs, 'for a bug to reach ON_QA')
        print (average_on_qa_msg)
    if verified_bugs > 0:
        average_verify_msg = functions.get_average_time_msg(
            time_to_verify, verified_bugs, 'for ON_QA bugs to be verified')
        print (average_verify_msg)
    if closed_bugs > 0:
        average_close_msg = functions.get_average_time_msg(
            time_to_close, closed_bugs, 'for a bug to be closed')
        print (average_close_msg)
