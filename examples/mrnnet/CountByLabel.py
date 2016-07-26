import wlrutil
import sys

dbName = sys.argv[1]
records = wlrutil.GetRecordsByLabel( dbName )
total = 0
for label in records:
    nRecs = len( records[label])
    print "%d : %d" % (label, nRecs )
    total += nRecs
print "Total Records : ", total

