"""
RFE backlog script specific data is kept, its hard coded and not calculated.
"""

# Default bug_state help.
HELP = "rfe_backlog generates a CSV containing data from BugZilla with\
the what constitutes as an RFE backlog per DFG.\n\
There are two sheets that are updated: pre status and per release.\n\
\n\
Usage: rfe_backlog.py [ --help: print this. ; --file <CSV path/name> ]\n\
"

# Google sheet that holds bug statistics.
SHEET = '1mqTunAjY8kVVsWc-zUlTxXr_x8h5HHtWAbvW1m1NSFY'
RANGE = 'DATA!A:LZ'
