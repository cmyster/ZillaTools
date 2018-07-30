"""
Generates averages of times in days it takes to switch from NEW to ON_QA, from
ON_QA to VERIFIED and from VERIFIED to CLOSED per DFG per version.
"""
from bugzilla import RHBugzilla
from common_data import BAD_STATUS, BUG_STATUS, QUICKSEARCH, URL
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
        # Creating the bz client and bug query.
        bz_client = RHBugzilla(URL)
        query = get_query(self.version, self.dfg)
        bugs = bz_client.query(query)
        link = QUICKSEARCH
        # Some arguments to save data between iterations.
        empty = "0,0,0,0,0,0,0,0,0,0"
        temp_bugs = {}
        temp_time = {}
        for i in range(0, len(BUG_STATUS)):
            status = BUG_STATUS[i]
            temp_bugs[status] = 0
            temp_time[status] = 0

        ok_bugs = 0
        final_time = ""

        # If no bugs, print empty and leave.
        if not bugs:
            self.results[self.index] = '{},{},{}\n'.format(
                self.dfg, self.version[0], empty)
            return

        for bug in bugs:
            """
            Skip calculations if the bug was closed with a 'bad' resolution.
            If it closed 'cleanly' or it is still open, the bug is 'OK' and we 
            can calculate how long it took to reach each state.
            """
            if bug.resolution in BAD_STATUS:
                continue

            # Add to total OK bugs.
            ok_bugs += 1
            # Add to the link of OK bugs.
            link += '{}%2C'.format(bug.id)
            # Get a dictionary of {"string status, int time",}
            status_times = get_status_times(bug.get_history_raw(),
                                            bug.creation_time.value)
            """
            Going over all possible bug statuses as defined by BZ and first we 
            test that such a pair exists for the current bug. For instance after
            NEW comes ASSIGNED etc'. 
            """
            for i in range(1, len(BUG_STATUS)):
                current = "{}".format(BUG_STATUS[i])
                previous = "{}".format(BUG_STATUS[i - 1])
                """
                Statistics are taken only if a bug has two consecutive statuses.
                """
                if current in status_times.keys() and \
                        previous in status_times.keys():
                    """
                    If the current status is younger than the previous status, 
                    it means that the bug is being re-fixed.
                    For instance if QA failed the fix, a status will go from
                    'ON_QA' to 'ASSIGNED' and that will have a newer time than
                    the next status after 'ASSIGNED' which is 'ON_DEV'.
                    """
                    if status_times[current] > status_times[previous]:
                        temp_bugs[previous] += 1
                        temp_time[previous] +=\
                            (status_times[current] - status_times[previous])

        """
        If during calculations the total number of bugs is 0, were setting
        the final result to a "0".
        """
        for i in range(0, len(BUG_STATUS)):
            status = "{}".format(BUG_STATUS[i])
            if temp_bugs[status] == 0:
                final_time += "0,"
            else:
                final_time += str(temp_time[status] / temp_bugs[status] /
                                  86400) + ","
        final_time = final_time[:-1]

        self.results[self.index] = \
            '{},{},{},{},{},{}\n'.format(
                self.dfg, self.version[0], len(bugs), ok_bugs, final_time, link)
