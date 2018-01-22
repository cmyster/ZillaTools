"""
Generates a single line of bug statistics for a username.
"""
from bugzilla import RHBugzilla
import data
import functions


class UserStatistics:
    """
    Generates a single CSV line. It is returned as string item inside a list in
    the position that corresponds to the calling thread number to be merged in
    the calling class.

    :rtype: list
    """
    def __init__(self, user, results, index):
        # type: (str, list, int) -> None
        """
        :type user: str
        :type results: list
        :type index: int
        :rtype: None
        """

        # Assignments and Definitions
        self.user = user
        self.results = results
        self.index = index

    def run(self):
        # type: (self) -> None
        """
        :rtype: None
        """
        # Creating the bz client.
        bz_client = RHBugzilla(data.URL)
        # Creating needed queries.
        q_on_qa = functions.get_on_qa_query(self.user)
        q_open = functions.get_open_query(self.user)
        q_reported = functions.get_reported_query(self.user)
        q_needinfo = functions.get_needinfo_query(self.user)

        # Getting bug lists.
        b_on_qa = bz_client.query(q_on_qa)
        b_open = bz_client.query(q_open)
        b_reported = bz_client.query(q_reported)
        b_needinfo = bz_client.query(q_needinfo)

        # Quicksearch links
        l_on_qa = ''
        l_open = ''
        l_reported = ''
        l_needinfo = ''

        if len(b_on_qa) != 0:
            l_on_qa = data.BS_QUICKSEARCH
            for bug in b_on_qa:
                l_on_qa += '{}%2C'.format(bug.id)

        if len(b_open) != 0:
            l_open = data.BS_QUICKSEARCH
            for bug in b_open:
                l_open += '{}%2C'.format(bug.id)

        if len(b_reported) != 0:
            l_reported = data.BS_QUICKSEARCH
            for bug in b_reported:
                l_reported += '{}%2C'.format(bug.id)

        if len(b_needinfo) != 0:
            l_needinfo = data.BS_QUICKSEARCH
            for bug in b_needinfo:
                l_needinfo += '{}%2C'.format(bug.id)

        # Removing last ',' from the links.
        l_on_qa = l_on_qa[:-3]
        l_open = l_open[:-3]
        l_reported = l_reported[:-3]
        l_needinfo = l_needinfo[:-3]

        self.results[self.index] = \
            '{},{},{},{},{},{},{},{},{}\n'.format(
                self.user,
                len(b_on_qa), l_on_qa,
                len(b_open), l_open,
                len(b_reported), l_reported,
                len(b_needinfo), l_needinfo)
