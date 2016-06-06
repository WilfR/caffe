import leveldb

### db = leveldb.LevelDB('./AugmentedOriginalLevelDB')
### iter = db.RangeIter('00000000','00000200')
db = leveldb.LevelDB('f:\\MRToNN\\LevelDB5')
iter = db.RangeIter()
for k,v in iter:
    print "Key : %s Len(val)=%d" % (k,len(v))


