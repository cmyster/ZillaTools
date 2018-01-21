#!/usr/bin/python2.7
"""
This script goes over lists of bugs per predefined bugzilla query and outputs
a CSV with data to be later digested elsewhere.
"""
from threading import Thread
from sys import argv
from sys import exit
import statistics
import data


if '--help' in argv:
    print('{}'.format(data.BS_HELP))
    exit(0)

# Setting a default name for the CSV file.
LOG_FILE = '{}'.format(data.BS_OUTFILE)
if '--file' in argv:
    if argv[argv.index('--file') + 1] is not str:
        LOG_FILE = argv[argv.index('--file') + 1]

# Making sure that file is writeable
try:
    log = open("{}".format(LOG_FILE), "w")
    log.write(data.HEADERS)
    log.close()
except IOError as e:
    print 'IOError: {0} - {1}'.format(e.errno, e.strerror)
    exit(1)

# This first line of output serves as columns titles.
print 'CSV data is writen to {}'.format(LOG_FILE)

# These lists are globals for THREADS and RESULTS and need to have fixed size.
THREADS = [None] * len(data.DFGS) * len(data.VERSIONS)
RESULTS = [None] * len(data.DFGS) * len(data.VERSIONS)
THREAD_INDEX = 0

for dfg in data.DFGS:
    for version in data.VERSIONS:
        STATS = statistics.PrintStatistics(version, dfg, RESULTS, THREAD_INDEX)
        THREADS[THREAD_INDEX] = Thread(target=STATS.run)
        THREADS[THREAD_INDEX].daemon = True
        print('Starting work on {} in {}'.format(dfg, version[0]))
        THREADS[THREAD_INDEX].start()
        THREAD_INDEX += 1

print('Waiting for threads to finish.')
for index in range(len(THREADS)):
    THREADS[index].join()

print 'Writing to {}'.format(LOG_FILE)
log = open("{}".format(LOG_FILE), "a")
log.write("".join(RESULTS))
log.close()

# Finally
print "DONE!"
