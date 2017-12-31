# Bugs that were closed with this state should not be used.
bad_status = [
    'NOTABUG',
    'WONTFIX',
    'DEFERRED',
    'WORKSFORME',
    'DUPLICATE',
    'CANTFIX',
    'INSUFFICIENT_DATA'
]

# These are the possible statuses a bug can be in.
bug_status = [
    'NEW',       # The bug has not been triaged yet.
    'ASSIGNED',  # The bug has been assigned to an engineer and is in progress.
    'ON_DEV',    # The bug or feature has a complete patch set which has been
                 # posted upstream for review.
    'POST',      # The solution for the bugzilla has been merged upstream and is
                 # ready to be imported for a build.
    'MODIFIED',  # The bug or feature is included in a build and is ready to be
                 # consumed by QE.
    'ON_QA',     # The bug has been added to an erratum and should be ready for
                 # QE to test, if applicable.
    'VERIFIED',  # The bug has been verified as resolved with the build
                 # indicated in the Fixed-in-version field or a newer build.
    'RELEASE_PENDING',  # The fix is about to be shipped.
    'CLOSED'     # The bug has been closed.
]


# RHOSP versions as coded into BZ with starting and ending dates.
versions = [
    ['10.0 (Newton)', '2016-07-28', '2016-12-15'],
    ['11.0 (Ocata)', '2016-11-30', '2017-05-08'],
    ['12.0 (Pike)', '2017-05-09', '2017-12-08']
]

# Main BZ URL
URL = 'bugzilla.redhat.com'

# These are the only needed fields.
# Less fields is less taxing on BZ. ID must remain.
include_fields = [
    'id',
    'creation_time',
    'last_change_time',
    'resolution',
    'status',
]

# DFGs are defined here.
dfgs = [
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
    'ProdInfra',
    'ReleaseDelivery',
    'Security',
    'Storage',
    'DFG:Storage Squad:Cinder',
    'DFG:Storage Squad:Glance',
    'DFG:Storage Squad:Manila',
    'DFG:Storage Squad:Swift',
    'Telemetry',
    'UI',
    'Upgrades',
    'Workflows',
]
