#!/usr/bin/python2.7
"""
This script goes over individual contributes and fetches data and statistics.
"""
from threading import Thread
from sys import argv
import user_state_statistics
import update_sheet
from common_functions import get_log_name
import user_state_data
import common_data

if '--help' in argv:
    print '{}'.format(user_state_data.HELP)
    exit(0)

# Setting a default name for the log file.
LOG_FILE = get_log_name(argv, 'user_state.csv')

# This first line of output serves as columns titles.
LOG = open(LOG_FILE, "w")
LOG.write("{}\n".format(user_state_data.HEADERS))
LOG.close()

# These lists are globals for THREADS and RESULTS and need to have fixed size.
THREADS = [None] * len(user_state_data.USERS)
RESULTS = [None] * len(user_state_data.USERS)
THREAD_INDEX = 0

for user in user_state_data.USERS:
    STATS = user_state_statistics.UserStatistics(user, RESULTS, THREAD_INDEX)
    THREADS[THREAD_INDEX] = Thread(target=STATS.run)
    THREADS[THREAD_INDEX].daemon = True
    print 'Starting thread for {}'.format(user)
    THREADS[THREAD_INDEX].start()
    THREAD_INDEX += 1

print 'Waiting for threads to finish.'
for index in range(len(THREADS)):
    THREADS[index].join()

print 'Writing to {}'.format(LOG_FILE)
LOG = open("{}".format(LOG_FILE), "a")
LOG.write("".join(RESULTS))
LOG.close()

UPDATE = update_sheet.UpdateSheet(
    user_state_data.SHEET,
    common_data.API_SECRET,
    common_data.API_TOKEN,
    LOG_FILE,
    common_data.RANGE,
)

UPDATE()

# Finally
print "DONE!"
