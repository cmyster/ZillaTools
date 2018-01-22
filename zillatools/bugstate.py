#!/usr/bin/python2.7
"""
This script goes over lists of bugs per predefined bugzilla query and outputs
a CSV with data to be later digested elsewhere.
"""
from threading import Thread
from sys import argv
from sys import exit
import statistics
from functions import get_totals
from functions import get_logfile
import data


if '--help' in argv:
    print('{}'.format(data.BS_HELP))
    exit(0)

# Setting a default name for the CSV file.
LOG_FILE = get_logfile(argv)
print 'CSV data is writen to {}'.format(LOG_FILE)

# If there are more arguments, print ignore message.
if len(argv) > 3:
    print 'Ignoring arguments: ',
    for i in range(3, len(argv)):
        print "{} ".format(argv[i]),
    print ''

# This first line of output serves as columns titles.
log = open(LOG_FILE, "w")
log.write("{}\n".format(data.HEADERS))
log.close()

# These lists are globals for THREADS and RESULTS and need to have fixed size.
THREADS = [None] * len(data.DFGS) * len(data.VERSIONS)
RESULTS = [None] * len(data.DFGS) * len(data.VERSIONS)
THREAD_INDEX = 0

for dfg in data.DFGS:
    for version in data.VERSIONS:
        STATS = statistics.PrintStatistics(version, dfg, RESULTS, THREAD_INDEX)
        THREADS[THREAD_INDEX] = Thread(target=STATS.run)
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

for version in data.VERSIONS:
    log = open("{}".format(LOG_FILE), "a")
    totals = get_totals(LOG_FILE, version[0], len(data.DFGS))
    log.write("Total averages, for {},{}\n".format(version[0], totals))
    log.close()

# Finally
print "DONE!"
