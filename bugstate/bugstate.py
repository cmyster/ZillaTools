"""
This script goes over lists of bugs per predefined bugzilla query and outputs
a CSV with data to be later digested elsewhere.
"""
from bugzilla import RHBugzilla

# Local helpers
import data
import statistics

BZ = RHBugzilla(data.URL)

# This first line of output serves as columns titles.
print('DFG,Version,Total,Filtered,To ON_QA,To VERIFIED,To CLOSE,URL')
for dfg in data.DFGS:
    for version in data.VERSIONS:
        statistics.PrintStatistics(version, dfg)
