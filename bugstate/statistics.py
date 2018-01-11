"""
Receiving DFG and version, and printing statstics.
"""
from bugzilla import RHBugzilla
import data
import functions


class PrintStatistics:
    def __init__(self, version, dfg, results, index):
        # type: (list, str) -> None
        """
        :rtype: None

        :type version: list
        :type dfg: str
        :type results: list
        :type index: int
        """

        # Assignments and Definitions
        self.version = version
        self.dfg = dfg
        self.results = results
        self.index = index
        self.bz = RHBugzilla(data.URL)
        self.query = functions.get_query(self.version, self.dfg)
        self.bugs = self.bz.query(self.query)
        self.link = data.QUICKSEARCH

        # Some integers to help calculate times.
        self.on_qa_bugs = 0
        self.verified_bugs = 0
        self.closed_bugs = 0

        self.time_to_on_qa = 0
        self.time_to_verify = 0
        self.time_to_close = 0

        self.average_on_qa_time = 0
        self.average_verify_time = 0
        self.average_close_time = 0

        self.ok_bugs = 0

    def run(self):
        # If no bugs, print empty and leave.
        if not self.bugs:
            self.results[self.index] = \
                '{},{},,,,,,\n'.format(self.dfg, self.version[0])

        for bug in self.bugs:
            if bug.resolution not in data.BAD_STATUS:
                self.ok_bugs += 1
                self.link += '{}%2C'.format(bug.id)
                status_times = functions.get_status_times(
                    bug.get_history_raw())
                new_time = functions.get_datetime(bug.creation_time.value)
                int_new_time = functions.get_int_datetime(new_time)
                status_times['NEW'] = int_new_time

                if 'ON_QA' in status_times.keys():
                    self.on_qa_bugs += 1
                    self.time_to_on_qa += (status_times['ON_QA'] -
                                           status_times['NEW'])

                # Bugs that skip ON_QA are not used.
                if 'VERIFIED' in status_times.keys() \
                        and 'ON_QA' in status_times.keys():
                    self.verified_bugs += 1
                    self.time_to_verify += (status_times['VERIFIED'] -
                                            status_times['ON_QA'])

                # Bugs that were closed due to an issue with the bug are not
                # used.
                if 'CLOSED' in status_times.keys():
                    self.closed_bugs += 1
                    self.time_to_close += (status_times['CLOSED'] -
                                           status_times['NEW'])

        # Removing last ',' from the link.
        self.link = self.link[:-3]

        # If there are no bugs, keep the link empty.
        if self.on_qa_bugs == 0 and \
                self.verified_bugs == 0 and \
                self.closed_bugs == 0:
            self.link = ''

        # In case of 0 bugs, print nothing. Else, divide time by number and
        # by 86400 which is the number of seconds in one day.
        if self.on_qa_bugs == 0:
            final_onq = ''
        else:
            final_onq = self.time_to_on_qa / self.on_qa_bugs / 86400
        if self.verified_bugs == 0:
            final_ver = ''
        else:
            final_ver = self.time_to_verify / self.verified_bugs / 86400
        if self.closed_bugs == 0:
            final_cls = ''
        else:
            final_cls = self.time_to_close / self.closed_bugs / 86400

        self.results[self.index] = \
            '{},{},{},{},{},{},{},{}\n'.format(
            self.dfg, self.version[0], len(self.bugs), self.ok_bugs,
            final_onq, final_ver, final_cls, self.link)
