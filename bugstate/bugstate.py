"""
This script goes over lists of bugs per predefined bugzilla query and outputs
a CSV with data to be later digested elsewhere.
"""
import statistics

from data import DFGS
from data import VERSIONS


# This first line of output serves as columns titles.
print('DFG,Version,Total,Filtered,To ON_QA,To VERIFIED,To CLOSE,URL')
for dfg in DFGS:
    for version in VERSIONS:
        statistics.PrintStatistics(version, dfg)
