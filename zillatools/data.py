"""
Here data is kept, its hard coded and not calculated.
"""

# Default help.
BS_HELP = "bugstate generates a CSV containing data from BugZilla with\
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
Usage: bugstate [ --help - print this. ; --file <logname> ]\n\
"

# Default bugstate file name.
BS_OUTFILE = 'bugstate.csv'

# These are the possible statuses a bug can be in.
BUG_STATUS = [
    'NEW',        # The bug has not been triaged yet.
    'ASSIGNED',   # The bug has been assigned and is in progress.
    'ON_DEV',     # The bug or feature has a complete patch set which has been
                  # posted upstream for review.
    'POST',       # The solution for the bugzilla has been merged upstream and
                  # is ready to be imported for a build.
    'MODIFIED',   # The bug or feature is included in a build and is ready to
                  # be consumed by QE.
    'ON_QA',      # The bug has been added to an erratum and should be ready
                  # for QE to test, if applicable.
    'VERIFIED',   # The bug has been verified as resolved with the build
                  # indicated in the Fixed-in-version field or a newer build.
    'RELEASE_PENDING',  # The fix is about to be shipped.
    'CLOSED'      # The bug has been closed.
]


# Bugs that were closed with this state should not be used.
BAD_STATUS = [
    'NOTABUG',
    'WONTFIX',
    'DEFERRED',
    'WORKSFORME',
    'DUPLICATE',
    'CANTFIX',
    'INSUFFICIENT_DATA'
]


# RHOSP versions as coded into BZ with starting and ending dates.
VERSIONS = [
    ['10.0 (Newton)', '2016-07-28', '2016-12-15'],
    ['11.0 (Ocata)', '2016-11-30', '2017-05-08'],
    ['12.0 (Pike)', '2017-05-09', '2017-12-08']
]

# Main BZ URL
URL = 'bugzilla.redhat.com'

# These are the only needed fields. Less fields is less taxing on BZ.
INCLUDE_FIELDS = [
    'id',
    'creation_time',
    'last_change_time',
    'resolution',
    'status',
]

# DFGs are defined here.
DFGS = [
    'Ceph',
    'CloudApp',
    'Compute',
    'Containers',
    'DF',
    'HardProv',
    'Infra',
    'MetMon',
    'NFV',
    'Networking',
    'ODL',
    'OVN',
    'OpsTools',
    'PIDONE',
    'PerfScale',
    'ProdInfra',
    'ReleaseDelivery',
    'Security',
    'Storage',
    'Telemetry',
    'UI',
    'Upgrades',
    'Workflows',
]

# Quicksearch link starts like this, then IDs are added with a comma.
QUICKSEARCH = 'https://bugzilla.redhat.com/buglist.cgi?quicksearch='

# CSV headers
HEADERS = 'DFG,Version,Total,Filtered,To ON_QA,To VERIFIED,To CLOSE,URL'
