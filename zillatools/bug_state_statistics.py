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

                if 'ON_QA' in status_times.keys():
                    on_qa_bugs += 1
                    time_to_on_qa += (status_times['ON_QA'] -
                                      status_times['NEW'])

                """
                Statistics for verifying a bug will be gathered only for bugs
                that have VERIFIED state and ON_QA because bugs can get to be
                marked as VERIFIED without passing through QA.
                Also the age of the VERIFIED state needs to be te youngest
                except RELEASE_PENDING or CLOSED otherwise the bug was
                reopened or have failed QA.
                """
                if 'VERIFIED' in status_times.keys() \
                        and 'ON_QA' in status_times.keys():
                    closed_less = status_times
                    if 'CLOSED' in closed_less.keys():
                        closed_less.pop('CLOSED')
                    if 'RELEASE_PENDING' in closed_less.keys():
                        closed_less.pop('RELEASE_PENDING')

                    latest = max(closed_less.values())
                    if status_times['VERIFIED'] == latest:
                        verified_bugs += 1
                        time_to_verify += (status_times['VERIFIED'] -
                                           status_times['ON_QA'])

                """
                With CLOSED bugs we can get negative days-to-close numbers:
                Bugs that were closed due to an issue are not used, therefore
                we are looking for bugs that were CLOSED after being VERIFIED.
                CLOSED needs to be the latest entry. If it is not, than this
                is a bug that was reopened, and we don't need to take it into
                consideration when calculating time to close because it will
                get another CLOSED in the future to overwrite the current one.
                """
                if 'CLOSED' in status_times.keys() \
                        and 'VERIFIED' in status_times.keys():
                    latest = max(status_times.values())
                    if status_times['CLOSED'] == latest:
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
