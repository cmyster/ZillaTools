"""
Generates averages of times in days it takes to switch from NEW to ON_QA, from
ON_QA to VERIFIED and from VERIFIED to CLOSED per DFG per version.
"""
from bugzilla import RHBugzilla
from common_data import BAD_STATUS, URL, QUICKSEARCH
from common_functions import get_status_times
from bug_state_functions import get_query


class BugStatistics:
    """
    Generates a single CSV line. It is returned as string item inside a list
    in the position that corresponds to the calling thread number to be merged
    in the calling class.

    :rtype: list
    """
    def __init__(self, version, dfg, results, index):
        # type: (list, str, list, int) -> None
        """
        :type version: list
        :type dfg: str
        :type results: list
        :type index: int
        :rtype: None
        """

        # Assignments and Definitions
        self.version = version
        self.dfg = dfg
        self.results = results
        self.index = index

    def main(self):
        # type: (self) -> None
        """
        :rtype: None
        """
        # Creating the bz client and bugs queries.
        bz_client = RHBugzilla(URL)
        query = get_query(self.version, self.dfg)
        bugs = bz_client.query(query)
        link = QUICKSEARCH
        # Some integers to help calculate times.
        on_qa_bugs = 0
        verified_bugs = 0
        closed_bugs = 0
        time_to_on_qa = 0
        time_to_verify = 0
        time_to_close = 0
        ok_bugs = 0

        # If no bugs, print empty and leave.
        if not bugs:
            self.results[self.index] = \
                '{},{},0,0,0,0,0,\n'.format(self.dfg, self.version[0])
            return

        for bug in bugs:
            if bug.resolution not in BAD_STATUS:
                ok_bugs += 1
                link += '{}%2C'.format(bug.id)
                status_times = get_status_times(
                    bug.get_history_raw(),
                    bug.creation_time.value,
                )

                """
                Bugs go into 3 stages:

                NEW      => current status >= ON_QA    - Development stage.
                ON_QA    => current status >= VERIFIED - Testing stage.
                VERIFIED => current status >= CLOSED   - Done.

                If the lower limit of the stages above is not the newest for
                that stage, it means that the bug was re-opened or failed QA.
                status_times is a dict (unsortable), so to make sure that
                a status is the youngest for a certain range, we remove the
                next statuses for the next stages and test the time.
                """

                if 'ON_QA' in status_times.keys():
                    temp_d = status_times.copy()
                    for status in ['VERIFIED', 'RELEASE_PENDING', 'CLOSED']:
                        if status in temp_d.keys():
                            del temp_d[status]

                    youngest = max(temp_d.values())

                    if status_times['ON_QA'] == youngest:
                        on_qa_bugs += 1
                        time_to_on_qa += (status_times['ON_QA'] -
                                          status_times['NEW'])

                """
                Statistics for verifying a bug will be gathered only for bugs
                that have VERIFIED state AND ON_QA because bugs can get marked
                as VERIFIED without going through QA.
                """
                if 'VERIFIED' in status_times.keys() \
                        and 'ON_QA' in status_times.keys():
                    temp_d = status_times.copy()
                    for status in ['RELEASE_PENDING', 'CLOSED']:
                        if status in temp_d.keys():
                            del temp_d[status]

                    youngest = max(temp_d.values())
                    if status_times['VERIFIED'] == youngest:
                        verified_bugs += 1
                        time_to_verify += (status_times['VERIFIED'] -
                                           status_times['ON_QA'])

                """
                With CLOSED bugs we can get negative days-to-close numbers:
                Bugs that were closed due to an issue are not used, therefore
                we are looking for bugs that were CLOSED after being VERIFIED.
                CLOSED needs to be the latest entry. If it is not, than this
                is a bug was reopened.
                """
                if 'CLOSED' in status_times.keys() \
                        and 'VERIFIED' in status_times.keys():
                    youngest = max(status_times.values())
                    if status_times['CLOSED'] == youngest:
                        closed_bugs += 1
                        time_to_close += (status_times['CLOSED'] -
                                          status_times['VERIFIED'])

        # Removing last ',' from the link.
        link = link[:-3]

        # If there are no bugs, keep the link empty.
        if on_qa_bugs == 0 and verified_bugs == 0 and closed_bugs == 0:
            link = ''

        # In case of 0 bugs, print nothing. Else, divide time by number and
        # by 86400 which is the number of seconds in one day.
        if on_qa_bugs == 0:
            final_onq = '0'
        else:
            final_onq = time_to_on_qa / on_qa_bugs / 86400
        if verified_bugs == 0:
            final_ver = '0'
        else:
            final_ver = time_to_verify / verified_bugs / 86400
        if closed_bugs == 0:
            final_cls = '0'
        else:
            final_cls = time_to_close / closed_bugs / 86400

        self.results[self.index] = \
            '{},{},{},{},{},{},{},{}\n'.format(
                self.dfg, self.version[0], len(bugs), ok_bugs, final_onq,
                final_ver, final_cls, link)
