"""
Here user_state specific data is kept, its hard coded and not calculated.
"""

# Default user_state help.
HELP = "user_state generates a CSV containing data from BugZilla with\
the following data:\n\
    UserID: Login name.\n\
    ON_QA: Number of on ON_QA bugs on the user and a link.\n\
    Open bugs: Number of all open bugs on the user and a link.\n\
    Reported bugs: Number of all the bugs reported by the user and a link.\n\
    Needed info: Number of bugs with needinfo on the user and a link.\n\
\n\
Usage: user_state.py [ --help: print this. ; --file <CSV path/name> ]\n\
"
# Usernames to be tracked. No leading @domain.xyz is needed.
USERS = [
    'achernet',
    'afiodoro',
    'agurenko',
    'ahrechan',
    'augol',
    'bjacot',
    'dkholodo',
    'grozov',
    'iovadia',
    'jhajyahy',
    'mcornea',
    'mlammon',
    'nlevinki',
    'ohochman',
    'rbartal',
    'rrasouli',
    'sasha',
    'ssmolyak',
    'ukalifon',
    'yprokule',
]

# Userstate CSV headers
HEADERS = 'UserID,'\
    'ON_QA,link,'\
    'Open bugs,link,'\
    'needinfo,link,'

# Google sheet that holds user statistics.
SHEET = '11WTyjmbgU1K98xu_8TnhjPrAjmDb2uEmUD4PJ5xkML4'
SHEET_RANGE = 'DATA!A1:J20'
