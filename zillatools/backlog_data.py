"""
Here bug_state specific data is kept, its hard coded and not calculated.
"""

# Default bug_state help.
HELP = "backlog generates a CSV containing data from BugZilla with\
the what constitutes as a backlog per DFG.\n\
There are two sheets that are updated: pre status and per release.\n\
\n\
Usage: backlog.py [ --help: print this. ; --file <CSV path/name> ]\n\
"

# Google sheet that holds bug statistics.
SHEET = '1j4BnO41kwwSRSEapp5_aHb9bJa3pFuhFK2xK9OPfg5w'
RANGE = 'DATA!A:DZ'
