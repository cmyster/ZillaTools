#!/usr/bin/python2.7
"""
This script goes over lists of bugs per predefined bugzilla query and outputs
a CSV with data to be digested elsewhere.
"""
from threading import Thread
from sys import argv
from sys import exit
import update_sheet
import bug_backlog_data
from common_functions import get_log_name, get_weeks_dates
import common_data
import bug_backlog_statistics

if '--help' in argv:
    print('{}'.format(bug_backlog_data.HELP))
    exit(0)

# Getting the weeks to work on, and these serve as headers as well.
dates = get_weeks_dates(common_data.START_DATE)

# Setting a default name for the CSV file.
LOG_FILE = get_log_name(argv, 'bug_backlog.csv')

# This first line of output serves as columns titles.
log = open(LOG_FILE, "w")
log.write('DFG,{}\n'.format(','.join(map(str, dates))))
log.close()

# These lists are globals for THREADS and RESULTS and need to have fixed size.
THREADS = [None] * len(common_data.DFGS)
RESULTS = [None] * len(common_data.DFGS)
THREAD_INDEX = 0

for dfg in common_data.DFGS:
    STATS = bug_backlog_statistics.BacklogStatistics(
        dfg, dates, RESULTS, THREAD_INDEX)
    THREADS[THREAD_INDEX] = Thread(target=STATS.main)
    THREADS[THREAD_INDEX].daemon = True
    print('Starting thread for {}'.format(dfg))
    THREADS[THREAD_INDEX].start()
    THREAD_INDEX += 1

print('Waiting for threads to finish.')
for index in range(len(THREADS)):
    THREADS[index].join()

print 'Writing to {}'.format(LOG_FILE)
log = open("{}".format(LOG_FILE), "a")
log.write("".join(RESULTS))
log.close()

update = update_sheet.UpdateSheet(
    bug_backlog_data.SHEET,
    common_data.API_SECRET,
    common_data.API_TOKEN,
    LOG_FILE,
    common_data.RANGE,
)

update()

# Finally
print "DONE!"
