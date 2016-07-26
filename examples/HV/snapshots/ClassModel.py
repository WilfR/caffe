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
        blobs=fields[1][1][layerIndex].blobs
        return blobs


