"""
Generates a single line of bug statistics per username.
"""
from bugzilla import RHBugzilla
import common_data
import user_state_functions


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
        bz_client = RHBugzilla(common_data.URL)

        # Creating needed queries.
        q_on_qa = user_state_functions.get_on_qa_query(self.user)
        q_open = user_state_functions.get_open_query(self.user)
        q_need_info = user_state_functions.get_needinfo_query(self.user)
        q_opened = user_state_functions.get_all_opened(self.user)

        # Getting bug lists.
        b_on_qa = bz_client.query(q_on_qa)
        b_open = bz_client.query(q_open)
        b_need_info = bz_client.query(q_need_info)
        b_opened = bz_client.query(q_opened)

        # Quicksearch links
        l_on_qa = ''
        l_open = ''
        l_need_info = ''
        l_opened = ''

        if len(b_on_qa) != 0:
            l_on_qa = common_data.QUICKSEARCH
            for bug in b_on_qa:
                l_on_qa += '{}%2C'.format(bug.id)

        if len(b_open) != 0:
            l_open = common_data.QUICKSEARCH
            for bug in b_open:
                l_open += '{}%2C'.format(bug.id)

        if len(b_need_info) != 0:
            l_need_info = common_data.QUICKSEARCH
            for bug in b_need_info:
                l_need_info += '{}%2C'.format(bug.id)

        if len(b_opened) != 0:
            l_opened = common_data.QUICKSEARCH
            for bug in b_need_info:
                l_opened += '{}%2C'.format(bug.id)

        # Removing last ',' from the links.
        l_on_qa = l_on_qa[:-3]
        l_open = l_open[:-3]
        l_need_info = l_need_info[:-3]
        l_opened = l_opened[:-3]

        # For reported bugs per user, same as the above but per version.
        per_version = ''
        for version in common_data.VERSIONS:
            q_reported = user_state_functions.get_reported_query(
                self.user,
                version,
            )
            b_reported = bz_client.query(q_reported)

            l_reported = ''
            if len(b_reported) != 0:
                l_reported = common_data.QUICKSEARCH
                for bug in b_reported:
                    l_reported += '{}%2C'.format(bug.id)
                l_reported = l_reported[:-3]

            per_version += "{},{},".format(len(b_reported), l_reported)

        self.results[self.index] = \
            '{},{},{},{},{},{},{},{},{},{}\n'.format(
                self.user,
                len(b_on_qa), l_on_qa,
                len(b_open), l_open,
                len(b_need_info), l_need_info,
                len(b_opened), l_opened,
                per_version,
            )
