#!/usr/bin/python2.7
"""
This script goes over lists of bugs per predefined bugzilla query and outputs
a CSV with data to be digested elsewhere.
"""
from threading import Thread
from sys import argv
import bug_state_statistics
import update_sheet
import common_functions
from bug_state_functions import get_totals
import bug_state_data
import common_data

if '--help' in argv:
    print("{}".format(bug_state_data.HELP))
    exit(0)

# Setting a default name for the CSV file.
LOG_FILE = common_functions.get_log_name(argv, 'bug_state.csv')

# This first line of output serves as columns titles.
LOG = open(LOG_FILE, "w")
LOG.write("{}\n".format(bug_state_data.HEADERS))
LOG.close()

# These lists are globals for THREADS and RESULTS and need to have fixed size.
THREADS = [None] * len(common_data.DFGS) * len(common_data.VERSIONS)
RESULTS = [None] * len(common_data.DFGS) * len(common_data.VERSIONS)
THREAD_INDEX = 0

for dfg in common_data.DFGS:
    for version in common_data.VERSIONS:
        STATS = bug_state_statistics.BugStatistics(
            version, dfg, RESULTS, THREAD_INDEX)
        THREADS[THREAD_INDEX] = Thread(target=STATS.main)
        THREADS[THREAD_INDEX].daemon = True
        print("Starting thread for {} in {}".format(dfg, version[0]))
        THREADS[THREAD_INDEX].start()
        THREAD_INDEX += 1

print("Waiting for threads to finish.")
for index in range(len(THREADS)):
    THREADS[index].join()

print("Writing to {}".format(LOG_FILE))
LOG = open("{}".format(LOG_FILE), "a")
LOG.write("".join(RESULTS))
LOG.close()

for version in common_data.VERSIONS:
    LOG = open("{}".format(LOG_FILE), "a")
    TOTALS = get_totals(LOG_FILE, version[0], len(common_data.DFGS))
    LOG.write("Total averages, {},{}\n".format(version[0], TOTALS))

LOG.write("\n{}\n".format(common_functions.get_time_now()))
LOG.close()

UPDATE = update_sheet.UpdateSheet(
    bug_state_data.SHEET,
    common_data.API_SECRET,
    common_data.API_TOKEN,
    LOG_FILE,
    common_data.RANGE,
)

UPDATE()

# Finally
print("DONE!")
