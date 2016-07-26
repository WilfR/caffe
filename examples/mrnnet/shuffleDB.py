import leveldb
from random import shuffle


indb = leveldb.LevelDB('./HvsVLevelDB2')
outdb = leveldb.LevelDB('./HvsVLevelDB2Shuffled')

keys=[]
for k,v in indb.RangeIter():
    keys.append(k)

shuffle(keys)
i=0

batch=leveldb.WriteBatch()
for k,v in indb.RangeIter():
    batch.Put( keys[i], v )
    i=i+1
outdb.Write(batch)





