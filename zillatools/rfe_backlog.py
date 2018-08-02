"""
This script goes over lists of bugs per predefined bugzilla query and outputs
a CSV with data to be digested elsewhere.
"""
from os import path
from os import remove
from sys import argv
from sys import exit
from threading import Thread
import update_sheet
import rfe_backlog_data
import common_functions
import common_data
import rfe_backlog_statistics

if '--help' in argv:
    print("{}".format(rfe_backlog_data.HELP))
    exit(0)

# Setting a default name for the CSV file.
LOG_FILE = common_functions.get_log_name(argv, 'rfe_backlog.csv')
if path.isfile(LOG_FILE):
    remove(LOG_FILE)

# These lists are globals for THREADS and RESULTS and need to have fixed size.
THREADS = [None] * len(common_data.DFGS)
RESULTS = [None] * len(common_data.DFGS)
THREAD_INDEX = 0

# Getting the weeks to work on, and these serve as headers as well.
dates = common_functions.get_weeks_dates(common_data.START_DATE)

for dfg in common_data.DFGS:
    STATS = rfe_backlog_statistics.BacklogStatistics(
        dfg, dates, RESULTS, THREAD_INDEX)
    THREADS[THREAD_INDEX] = Thread(target=STATS.main)
    THREADS[THREAD_INDEX].daemon = True
    print("Starting thread for {}".format(dfg))
    THREADS[THREAD_INDEX].start()
    THREAD_INDEX += 1

print("Waiting for threads to finish.")
for index in range(len(THREADS)):
    THREADS[index].join()

print("Writing to {}".format(LOG_FILE))
LOG = open("{}".format(LOG_FILE), "a")
LOG.write("DFG,{}\n".format(",".join(map(str, dates))))
LOG.write("".join(RESULTS))
LOG.write("\n{}\n".format(common_functions.get_time_now()))
LOG.close()

UPDATE = update_sheet.UpdateSheet(
    rfe_backlog_data.SHEET,
    common_data.API_SECRET,
    common_data.API_TOKEN,
    LOG_FILE,
    common_data.RANGE,
)

UPDATE()

# Finally
print("DONE!")
