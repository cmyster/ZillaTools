"""
This script goes over lists of bugs per predefined bugzilla query and outputs
a CSV with data to be later digested elsewhere.
"""
from threading import Thread
import statistics

from data import DFGS
from data import HEADERS
from data import VERSIONS

# This first line of output serves as columns titles.
print HEADERS
threads = [None] * len(DFGS) * len(VERSIONS)
results = [None] * len(DFGS) * len(VERSIONS)
thread_index = 0

for dfg in DFGS:
    for version in VERSIONS:
        stat = statistics.PrintStatistics(version, dfg, results, thread_index)
        threads[thread_index] = Thread(target=stat.run)
        threads[thread_index].daemon = True
        threads[thread_index].start()
        thread_index += 1

for index in range(len(threads)):
    threads[index].join()

print "".join(results)
