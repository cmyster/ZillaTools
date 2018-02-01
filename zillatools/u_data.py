"""
Here userstate specific data is kept, its hard coded and not calculated.
"""

# Default userstate help.
HELP = "Userstate generates a CSV containing data from BugZilla with\
the following data:\n\
    UserID: Login name.\n\
    ON_QA: Number of on ON_QA bugs on the user and a link.\n\
    Open bugs: Number of all open bugs on the user and a link.\n\
    Reported bugs: Number of all the bugs reported by the user and a link.\n\
    Needed info: Number of bugs with needinfo on the user and a link.\n\
\n\
Usage: userstate.py [ --help: print this. ; --file <CSV path/name> ]\n\
"
# Usernames to be tracked. No leading @domain.xyz is needed.
USERS = [
    'agurenko',
    'ahrechan',
    'augol',
    'dbrusilo',
    'dkholodo',
    'iovadia',
    'jhajyahy',
    'mcornea',
    'mlammon',
    'ohochman',
    'opavlenk',
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
    'Reported bugs,link,'\
    'needinfo,link,'

# Google sheet that holds user statistics.
SHEET = '11WTyjmbgU1K98xu_8TnhjPrAjmDb2uEmUD4PJ5xkML4'
SHEET_RANGE = 'DATA!A1:J20'
