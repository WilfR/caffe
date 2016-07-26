import numpy as np
import matplotlib.pyplot as plt
from caffe.proto import caffe_pb2


class CM :
    def __init__ (self, filename) :
        msg = open(filename, 'rb').read()
        netParam = caffe_pb2.NetParameter()
        netParam.ParseFromString(msg)
        self.netParam = netParam
        fields=netParam.ListFields()
        ### Repeated Composite Field Container
        rcfc=fields[1][1]
        self.layerNames = [ rcfc[i].name for i in range( len(rcfc) ) ]
        self.layerDict={}
        for i in range( len(rcfc) ) :
            self.layerDict[ rcfc[i].name ] = i

    def GetLayerNames( self ) :
        return self.layerNames

    def GetData( self, layerName ) :
        layerIndex = self.layerDict[ layerName ]
        fields=self.netParam.ListFields()
        blobs=fields[1][1][layerIndex]
        return blobs



def GetWeights( filename ) :
    msg = open(filename, 'rb').read()
    cm = caffe_pb2.NetParameter()
    cm.ParseFromString(msg)
    fields = cm.ListFields()
    ### work only with flat -> fully connected network
    blob = fields[1][1][3].blobs[0]
    nRows = blob.shape.dim[0]
    nCols = blob.shape.dim[1]
    w=[x for x in blob.data]
    a=np.array(w)
    a=a.reshape((nRows,nCols))
    return a

def ExtractEvolvedWeights( weightDict, iters, nRow, nCol ) :
    y=[]
    for iter in iters:
        wi=weights[iter]
        y.append( wi[nRow,nCol] )
    return y


baseName='Network8'
iters=range(10000,110000,10000)
x=[i/1000 for i in iters]
ymin=-2
ymax=2


weights={}
for iter in iters:
    filename = "%s_iter_%d.caffemodel"%(baseName,iter)
    wi=GetWeights(filename)
    weights[iter]=wi

y=ExtractEvolvedWeights( weights, iters, 0, 234 )
plt.subplot(2,4,1)
plt.plot( x, y )
plt.ylim([ymin,ymax])

y=ExtractEvolvedWeights( weights, iters, 0, 416 )
plt.subplot(2,4,2)
plt.plot( x, y )
plt.ylim([ymin,ymax])

y=ExtractEvolvedWeights( weights, iters, 0, 731 )
plt.subplot(2,4,3)
plt.plot( x, y )
plt.ylim([ymin,ymax])

y=ExtractEvolvedWeights( weights, iters, 0, 966 )
plt.subplot(2,4,4)
plt.plot( x, y )
plt.ylim([ymin,ymax])


y=ExtractEvolvedWeights( weights, iters, 1, 234 )
plt.subplot(2,4,5)
plt.plot( x, y )
plt.ylim([ymin,ymax])

y=ExtractEvolvedWeights( weights, iters, 1, 416 )
plt.subplot(2,4,6)
plt.plot( x, y )
plt.ylim([ymin,ymax])

y=ExtractEvolvedWeights( weights, iters, 1, 731 )
plt.subplot(2,4,7)
plt.plot( x, y )
plt.ylim([ymin,ymax])

y=ExtractEvolvedWeights( weights, iters, 1, 966 )
plt.subplot(2,4,8)
plt.plot( x, y )
plt.ylim([ymin,ymax])


plt.show()




