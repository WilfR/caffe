import numpy as np
import matplotlib.pyplot as plt

class LabelledImage():
    def __init__( self, nRows, nColumns, nLabel ) :
        self.rows = nRows
        self.columns = nColumns
        self.label = nLabel
        self.image = np.zeros((self.rows,self.columns),dtype=np.uint8)

    def DrawRow( self, nRowIndex ) :
        self.image[ nRowIndex, : ] = 255

    def DrawColumn( self, nColumnIndex ) :
        self.image[ :, nColumnIndex ] = 255

    def Display( self ) :
        plt.imshow( self.image, cmap=plt.cm.gray )
        ### plt.rcParams['image.interpolation'] = 'nearest'
        plt.rcParams['image.interpolation'] = None
        plt.axis('off')
        plt.title('Label = %d' % self.label)
        plt.show()

    def IsEqual( self, other ) :
        if self.label != other.label :
            return False
        if self.rows != other.rows :
            return False
        if self.columns != other.columns :
            return False
        if np.array_equal( self.image, other.image ) != True :
            return False
        return True

    def Dump( self, header ) :
        print header
        print "label = %d" % self.label
        print "rows  = %d  columns=%d" % (self.rows,self.columns)
        print "shape = ", self.image.shape


