import caffe
import leveldb
import numpy as np
from caffe.proto import caffe_pb2

inputDB = leveldb.LevelDB('AugmentedOriginalLevelDB')
datum = caffe_pb2.Datum()

### Get label-specific lists of values
values={}

for key, value in inputDB.RangeIter():
    datum.ParseFromString(value)
    label = datum.label
    if label in values:
        values[label].append(value)
    else:
        values[label] = [value]

counts={}
for label in values:
    counts[label]=len( values[label] )

for label in counts:
    print "%d : %d" % (label,counts[label])

currentIndexes={}
for label in counts:
    currentIndexes[label]=0

maxIndex = max( counts.values() )

outputDB = leveldb.LevelDB('EqualAugmentedLevelDB')

outputRecordNumber = 0

## we are going to write maxIndex * Number of Classes records

for index in xrange(maxIndex):
    batch = leveldb.WriteBatch()
    for label in values :
        value = values[label][ currentIndexes[label] ]
        currentIndexes[label] += 1
        if currentIndexes[label] >= counts[label] :
            currentIndexes[label] = 0
        key = "%0*d" % (8,outputRecordNumber)
        outputRecordNumber += 1
        batch.Put( key, value )
    outputDB.Write(batch)

























