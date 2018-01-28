"""
Generates a single line of bug statistics for a combination of DFG and version.
"""
from bugzilla import RHBugzilla
from datetime import datetime
import data
import functions


class BugStatistics:
    """
    Generates a single CSV line. It is returned as string item inside a list in
    the position that corresponds to the calling thread number to be merged in
    the calling class.

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

    def run(self):
        # type: (self) -> None
        """
        :rtype: None
        """
        # Creating the bz client and bugs queries.
        bz_client = RHBugzilla(data.URL)
        query = functions.get_bs_query(self.version, self.dfg)
        bugs = bz_client.query(query)
        link = data.BS_QUICKSEARCH
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
            if bug.resolution not in data.BAD_STATUS:
                ok_bugs += 1
                link += '{}%2C'.format(bug.id)
                status_times = functions.get_status_times(
                    bug.get_history_raw())
                new_time = datetime.strptime(bug.creation_time.value,
                                             '%Y%m%dT%H:%M:%S')
                int_new_time = int(new_time.strftime('%s'))
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

                # Bugs that were closed due to an issue are not used.
                if 'CLOSED' in status_times.keys():
                    closed_bugs += 1
                    time_to_close += (status_times['CLOSED'] -
                                      status_times['NEW'])

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
