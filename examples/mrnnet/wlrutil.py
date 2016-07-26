import sys
import leveldb
import LabelledImage
import numpy as np
import caffe
from caffe.proto import caffe_pb2
from random import shuffle
import matplotlib.pyplot as plt


def IsEqualLevelDBValues( value1, value2 ) :
    datum1 = LevelDBValueToDatum( value1 )
    datum2 = LevelDBValueToDatum( value2 )
    if datum1.channels != datum2.channels :
        return False
    if datum1.width != datum2.width :
        return False
    if datum1.height != datum2.height :
        return False
    if datum1.label != datum2.label :
        return False
    if np.array_equal( datum1.data, datum2.data ) != True :
        return False
    if datum1.label != datum2.label :
        return False
    return True


def LevelDBToTSNE( dbName, tsneDataName, tsneLabelName ) :
    db = leveldb.LevelDB(dbName)
    dataFile = open(tsneDataName,'w')
    labelFile = open(tsneLabelName,'w')

    datum = caffe_pb2.Datum()
    for key, value in db.RangeIter():
        labelledImage = LevelDBValueToLabelledImage( value )
        label = labelledImage.label
        image = labelledImage.image
        labelFile.write( '%d\n' % label )
        nRows=image.shape[0]
        nCols=image.shape[1]
        print "nrows=%d ncols=%d\n" % (nRows,nCols)
        for r in xrange( nRows ):
            for c in xrange( nCols ) :
                dataFile.write( '%d\t' % int(image[r,c]) )
        dataFile.write('\n')
    dataFile.close()
    labelFile.close()


def LevelDBValueToDatum( value ) :
    datum = caffe_pb2.Datum()
    datum.ParseFromString(value)
    return datum


def LevelDBValueToLabelledImage( value ) :
    datum = caffe_pb2.Datum()
    datum.ParseFromString(value)
    image = caffe.io.datum_to_array(datum)
    nRows = image.shape[1]
    nColumns = image.shape[2]
    label = datum.label
    labelledImage = LabelledImage.LabelledImage( nRows, nColumns, label )
    labelledImage.image = image.reshape((nRows,nColumns))
    return labelledImage

def DatumToLevelDBValue( datum ):
    return datum.SerializeToString()

def DatumToLabelledImage( datum ) :
    image = caffe.io.datum_to_array(datum)
    nChannels = image.shape[0]
    nRows = image.shape[1]
    nColumns = image.shape[2]
    label = datum.label
    labelledImage = LabelledImage.LabelledImage( nRows, nColumns, label )
    labelledImage.image = image.reshape((nRows,nColumns))
    return labelledImage

def LabelledImageToDatum( labelledImage ) :
    label    = labelledImage.label
    image    = labelledImage.image
    nRows    = labelledImage.rows
    nColumns = labelledImage.columns

    datum = caffe_pb2.Datum()
    datum.channels = 1
    datum.height   = nRows
    datum.width    = nColumns
    datum.data = image.tostring()
    datum.label    = label

    return datum



def LabelledImageToLevelDBValue( labelledImage ) :
    datum = LabelledImageToDatum( labelledImage )
    return DatumToLevelDBValue( datum )





def GetRecordsByLabel( dbName ) :
    db = leveldb.LevelDB(dbName)
    records={}
    datum = caffe_pb2.Datum()
    for key, value in db.RangeIter():
         datum.ParseFromString(value)
         label = datum.label
         if label in records:
            records[ label ].append( (key,value) )
         else:
            records[ label ] = [ (key,value) ]
    return records


def ShuffleDB( inputDBName, outputDBName ) :
    indb = leveldb.LevelDB(inputDBName)
    outdb = leveldb.LevelDB(outputDBName)

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



def ExtractRecordsWithLabels( inputDBName, outputDBName, labelList ) :
    inputDB = leveldb.LevelDB(inputDBName)
    datum = caffe_pb2.Datum()
    batch=leveldb.WriteBatch()
    nOutputRecordNumber = 0
    for key, value in inputDB.RangeIter():
         datum.ParseFromString(value)
         newKey = "%0*d" % (8,nOutputRecordNumber)
         label = datum.label
         if label in labelList :
            batch.Put( newKey, value )
         nOutputRecordNumber += 1
    outputDB = leveldb.LevelDB(outputDBName)
    outputDB.Write( batch )

def GetRandomSelection( inputDBName, nRecords ) :

    inputDB = leveldb.LevelDB(inputDBName)
    keys=[ key for key, value in inputDB.RangeIter()]
    shuffle(keys)
    randomSelection=[]
    for i in xrange( nRecords ) :
        key = keys[i]
        value = inputDB.Get( key )
        randomSelection.append( (key,value) )
    return randomSelection




def GetRandomSelectionOfLabelledImages( inputDBName, nRecords ) :
    inputDB = leveldb.LevelDB(inputDBName)
    keys=[ key for key, value in inputDB.RangeIter()]
    shuffle(keys)
    labelledImages = []
    for n in xrange( nRecords ) :
        key = keys[ n ]
        value = inputDB.Get( key )
        labelledImage = LevelDBValueToLabelledImage( value )
        ### label, image = LevelDBValueToLabelledImage( value )
        labelledImages.append( labelledImage )
    return labelledImages


###
###
###
### def loadFromDB( db, nRecords, nFirstRecord ):
###     datum = caffe_pb2.Datum()
###     labelledImages = []
###     for n in xrange( nRecords ) :
###         nRecordNumber = nFirstRecord + n
###         key = "%0*d" % (8,nRecordNumber)
###         value = db.Get( key )
###         datum.ParseFromString(value)
###         image = caffe.io.datum_to_array(datum)
###         label = datum.label
###         labelledImages.append( (image,label) )
###     return labelledImages
###
###
###
###
###


### From caffe classification example IPython notebook
def DisplayArrayOfImages(data):
    """Take an array of shape (n, height, width) or (n, height, width, 3)
       and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)"""

    # normalize data for display
    data = (data - data.min()) / (data.max() - data.min())

    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = (((0, n ** 2 - data.shape[0]),
               (0, 1), (0, 1))                 # add some space between filters
               + ((0, 0),) * (data.ndim - 3))  # don't pad the last dimension (if there is one)
    data = np.pad(data, padding, mode='constant', constant_values=1)  # pad with ones (white)

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])

    plt.imshow(data); plt.axis('off')


def GetSolver( solverFilename ) :
    return caffe.SGDSolver(solverFilename)

def GetNetworkDimensions( solver ) :
    ret = [ (k,v.data.shape) for k,v in solver.net.blobs.items() ]
    return ret

def GetWeightSizes( solver ) :
    ret = [ (k,v[0].data.shape) for k,v in solver.net.params.items() ]
    return ret

def ShowSolverTrainImages( solver ) :
    pass

def ShowSolverTestImages( solver ) :
    pass


