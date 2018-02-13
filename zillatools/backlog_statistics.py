"""
Generates statistics for a combination of DFG and version.
"""
from bugzilla import RHBugzilla
from common_data import URL
from bisect import bisect_left as bl
from common_functions import get_status_times, convert_bz_str_epoch
import backlog_functions


class BacklogStatistics:
    """
    Generates a single CSV line. It is returned as string item inside a list in
    the position that corresponds to the calling thread number to be merged in
    the calling class.

    :rtype: list
    """
    def __init__(self, dfg, dates, results, index):
        # type: (str, list, list, int) -> None
        """
        :type dfg: str
        :type dates: list
        :type results: list
        :type index: int
        :rtype: None
        """

        # Assignments and Definitions
        self.dfg = dfg
        self.dates = dates
        self.results = results
        self.index = index

    def main(self):
        # type: (self) -> None
        """
        :rtype: None
        """
        # Creating the bz client and bug query.
        bz_client = RHBugzilla(URL)
        query = backlog_functions.get_query(self.dfg)
        bugs = bz_client.query(query)
        # Converting all the dates to ints for easier search within ranges.
        int_dates = []
        for date in self.dates:
            int_dates.append(convert_bz_str_epoch(date))

        counter = [0] * len(int_dates)
        for bug in bugs:
            status_times = get_status_times(
                bug.get_history_raw(),
                bug.creation_time.value,
            )

            start_week = bl(int_dates, status_times['NEW'])
            if start_week > (len(int_dates) - 1):
                continue

            if 'CLOSED' in status_times:
                end_week = bl(int_dates, status_times['CLOSED'])
            elif 'VERIFIED' in status_times:
                end_week = bl(int_dates, status_times['VERIFIED'])
            else:
                end_week = len(int_dates) - 1

            if 0 <= start_week <= end_week:
                for i in range(start_week, end_week):
                    counter[i] += 1

        self.results[self.index] = '{},{}\n'.format(
            self.dfg, ','.join(map(str, counter)))
