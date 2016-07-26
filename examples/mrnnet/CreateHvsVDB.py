import wlrutil
import leveldb
import LabelledImage

nRows = 32
nColumns = 32
dbName = "HvsVLevelDB2"


batch=leveldb.WriteBatch()

nRecordNumber = 0

for i in xrange(nRows):
    for j in xrange( nRows ) :
        himage = LabelledImage.LabelledImage( nRows, nColumns, 0 )
        himage.DrawRow( i )
        himage.DrawRow( j )
        value = wlrutil.LabelledImageToLevelDBValue( himage )
        key = "%0*d" % (8,nRecordNumber)
        batch.Put( key, value )
        nRecordNumber += 1
        vimage = LabelledImage.LabelledImage( nRows, nColumns, 1 )
        vimage.DrawColumn( i )
        vimage.DrawColumn( j )
        value = wlrutil.LabelledImageToLevelDBValue( vimage )
        key = "%0*d" % (8,nRecordNumber)
        batch.Put( key, value )
        nRecordNumber += 1

db = leveldb.LevelDB(dbName)
db.Write( batch )



