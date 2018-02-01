#!/usr/bin/python2.7
"""
This script goes over lists of bugs per predefined bugzilla query and outputs
a CSV with data to be later digested elsewhere.
"""
from threading import Thread
from sys import argv
from sys import exit
import b_statistics
import update_sheet
from functions import get_bs_totals
from functions import get_log_name
import b_data
import c_data


if '--help' in argv:
    print('{}'.format(b_data.HELP))
    exit(0)

# Setting a default name for the CSV file.
LOG_FILE = get_log_name(argv, 'bugstate.csv')

# This first line of output serves as columns titles.
log = open(LOG_FILE, "w")
log.write("{}\n".format(b_data.HEADERS))
log.close()

# These lists are globals for THREADS and RESULTS and need to have fixed size.
THREADS = [None] * len(c_data.DFGS) * len(c_data.VERSIONS)
RESULTS = [None] * len(c_data.DFGS) * len(c_data.VERSIONS)
THREAD_INDEX = 0

for dfg in c_data.DFGS:
    for version in c_data.VERSIONS:
        STATS = b_statistics.BugStatistics(version, dfg, RESULTS, THREAD_INDEX)
        THREADS[THREAD_INDEX] = Thread(target=STATS.main)
        THREADS[THREAD_INDEX].daemon = True
        print('Starting thread for {} in {}'.format(dfg, version[0]))
        THREADS[THREAD_INDEX].start()
        THREAD_INDEX += 1

print('Waiting for threads to finish.')
for index in range(len(THREADS)):
    THREADS[index].join()

print 'Writing to {}'.format(LOG_FILE)
log = open("{}".format(LOG_FILE), "a")
log.write("".join(RESULTS))
log.close()

for version in c_data.VERSIONS:
    log = open("{}".format(LOG_FILE), "a")
    totals = get_bs_totals(LOG_FILE, version[0], len(c_data.DFGS))
    log.write("Total averages, for {},{}\n".format(version[0], totals))
    log.close()

update = update_sheet.UpdateSheet(
    b_data.SHEET,
    c_data.API_SECRET,
    c_data.API_TOKEN,
    LOG_FILE,
    b_data.SHEET_RANGE,
)

update()

# Finally
print "DONE!"
