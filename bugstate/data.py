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

# Versions in their HTML coding to be used as a parameter for url_to_query function.
versions = [
    '10.0%20%28Newton%29',
    '11.0%20%28Ocata%29',
    '12.0%20%28Pike%29&',
    '13.0%20%28Queens%29&',
]

# Main BZ URL
URL = 'bugzilla.redhat.com'

# These are the only needed fields. Less fields is less taxing on BZ. ID must remain.
include_fields = [
    'id',
    'creation_time',
    'last_change_time',
    'resolution',
    'status',
]
