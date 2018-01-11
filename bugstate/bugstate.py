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
print(HEADERS)

# These lists are globals for THREADS and RESULTS and need to have fixed size.
LIST_LEN = len(DFGS) * len(VERSIONS)
THREADS = [None] * LIST_LEN
RESULTS = [None] * LIST_LEN
THREAD_INDEX = 0

for dfg in DFGS:
    for version in VERSIONS:
        STATS = statistics.PrintStatistics(version, dfg, RESULTS, THREAD_INDEX)
        THREADS[THREAD_INDEX] = Thread(target=STATS.run)
        THREADS[THREAD_INDEX].daemon = True
        THREADS[THREAD_INDEX].start()
        THREAD_INDEX += 1

for index in enumerate(THREADS):
    THREADS[index].join()

print("".join(RESULTS))
