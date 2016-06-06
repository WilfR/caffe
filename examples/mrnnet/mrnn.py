import struct
import numpy as np
import matplotlib.pyplot as plt
import leveldb


class MRNN :
  def __init__(self):
      pass

  def labelToText(self,partLabel):
      if (partLabel < 0) or (partLabel >7 ) :
          return 'Invalid'
      names=['Unknown','Ankle','Femur','Foot','Hip','Knee','Leg','Pelvis']
      return names[ partLabel ]

  def display( self ) :
      partNameText = self.labelToText( self.partLabel )

      fig, ax1 = plt.subplots()
      ax1.set_xlabel(partNameText)

      plt.imshow( self.image, cmap=plt.cm.gray )
      plt.show()

def readFromLevelDB( db, key ) :
    val=db.Get(key)
    nRows=32
    nCols=32
    img=np.fromstring( val[9:1033], dtype='uint8' ).reshape((nRows,nCols))
    return img


### db = leveldb.LevelDB('./testLevelDB')
db = leveldb.LevelDB('./AugmentedOriginalLevelDB')
### for k,v in db.RangeIter('00000000','00000010'):
img = readFromLevelDB( db, '00000000' )
plt.imshow( img, cmap=plt.cm.gray )
plt.show()


