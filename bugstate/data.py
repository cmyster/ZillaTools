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

# RHOSP versions as coded into BZ.
versions = [
    '10.0 (Newton)',
    '11.0 (Ocata)',
    '12.0 (Pike)'
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
