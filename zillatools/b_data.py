"""
Here bugstate specific data is kept, its hard coded and not calculated.
"""

# Default bugstate help.
HELP = "Bugstate generates a CSV containing data from BugZilla with\
the following data:\n\
    DFG name: Internal group name.\n\
    Version: OpenStack version.\n\
    Total opened bugs: According to a specific search criteria.\n\
    Good bugs: From those opened, those bugs that DEV/QA spent time on.\n\
    Average time to reach ON_QA: Average time it took \"good\" bugs to change\
from NEW to ON_QA status.\n\
    Average time to reach VERIFIED: Average time it took \"good\" bugs to\
change from ON_QA to VERIFIED status.\n\
    Average time to close: Average time it took \"good\" bugs to change from\
NEW to CLOSED.\n\
\n\
Usage: bugstate.py [ --help: print this. ; --file <CSV path/name> ]\n\
"

# Bugstate CSV headers
HEADERS = 'DFG,Version,Total,Filtered,To ON_QA,To VERIFIED,To CLOSE,LINK'

# Google sheet that holds bug statistics.
SHEET = '1hJkSWyzB2dCOlajZgw2ZmVrjwX7fUFSDQm2nLF461_I'
SHEET_RANGE = 'DATA!A1:I80'
