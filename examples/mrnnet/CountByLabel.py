import sys
### import caffe
import leveldb
import numpy as np
from caffe.proto import caffe_pb2

dbName = sys.argv[1]
db = leveldb.LevelDB(dbName)
datum = caffe_pb2.Datum()

counts={}

for key, value in db.RangeIter():
    datum.ParseFromString(value)

    label = datum.label
    ### data = caffe.io.datum_to_array(datum)
    if label in counts:
        counts[label] += 1
    else:
        counts[label] = 1

total = 0
for label in counts:
    print "%d : %d" % (label, counts[label])
    total += counts[label]
print "Total Records : ", total


