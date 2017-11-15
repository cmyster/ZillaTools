from __future__ import print_function
from bugzilla import RHBugzilla
import funtions
import data


bz_q = RHBugzilla(data.URL)

# Earliest version to test
# TODO: Once query builder will be used, make this less silly...
rhosp = 10

for version in data.versions:
    # TODO: Move this URL query to be built from query builder.
    q_url = ('https://bugzilla.redhat.com/buglist.cgi?classification=Red%20Hat&f1=cf_internal_whiteboard&j_top=OR&o1=substring&product=Red%20Hat%20OpenStack&query_format=advanced&target_release={}&v1=DFG%3AUpgrades'.format(version))
    q = bz_q.url_to_query(q_url)

    # No need for all possible fields, this saves time. ID must be there.
    q['include_fields'] = data.include_fields

    # This is where BZ is being queried.
    bugs = bz_q.query(q)

    # A couple of integers to help calculate average time.
    closed_bugs = 0
    time_to_close = 0

    print ('Total number of bugs opened in rhosp {} is {}'.format(rhosp, len(bugs)))
    for bug in bugs:
        if bug.status in 'CLOSED' and bug.resolution not in data.bad_status:
            closed_bugs += 1
            delta = funtions.get_delta(bug.creation_time.value, bug.last_change_time.value)
            time_to_close += delta

    if closed_bugs > 0:
        average_time = funtions.get_average_time(time_to_close, closed_bugs, rhosp)
        print (average_time)

    rhosp += 1
