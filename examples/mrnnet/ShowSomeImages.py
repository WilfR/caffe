import sys
import matplotlib.pyplot as plt
import leveldb
import caffe
import numpy as np
from caffe.proto import caffe_pb2


def labelToText(partLabel):
    if (partLabel < 0) or (partLabel >7 ) :
        return 'Invalid'
    names=['Unknown','Ankle','Femur','Foot','Hip','Knee','Leg','Pelvis']
    return names[ partLabel ]


def loadFromDB( db, nRecords, nFirstRecord ):
    datum = caffe_pb2.Datum()
    labelledImages = []
    for n in xrange( nRecords ) :
        nRecordNumber = nFirstRecord + n
        key = "%0*d" % (8,nRecordNumber)
        value = db.Get( key )
        datum.ParseFromString(value)
        image = caffe.io.datum_to_array(datum)
        label = datum.label
        labelledImages.append( (image,label) )
    return labelledImages



def showLabelledImages( labelledImages, nRows, nColumns ) :
    plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams['image.cmap'] = 'gray'

    nImageNumber = 0
    for r in xrange(nRows):
        for c in xrange(nColumns):
            image, label = labelledImages[ nImageNumber ]
            index = r*nColumns+c+1
            textLabel = labelToText( label )
            plt.subplot(nRows, nColumns, index)
            plt.imshow( image[0,:,:], cmap=plt.cm.gray )
            plt.axis('off')
            plt.title(textLabel)
            nImageNumber += 1

    plt.show()




dbName = sys.argv[1]

nRows=8
nColumns=7
nFirstRecordNumber=56*100
nImages = nRows * nColumns


db = leveldb.LevelDB(dbName)


labelledImages = loadFromDB( db, nImages, nFirstRecordNumber )
showLabelledImages( labelledImages, nRows, nColumns )



