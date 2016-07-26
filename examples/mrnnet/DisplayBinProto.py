import caffe
import numpy as np
import sys
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print "Usage: python DisplayBinProto.py BinProtoFile"
    sys.exit()

binProtoFilename = sys.argv[1]

data = open( binProtoFilename , 'rb' ).read()

blob = caffe.proto.caffe_pb2.BlobProto()
blob.ParseFromString(data)
arr = np.array( caffe.io.blobproto_to_array(blob) )
rows=arr.shape[2]
cols=arr.shape[3]
arr=arr.reshape((rows,cols))
plt.imshow(arr,cmap='gray') ### ,title=binProtoFilename)
plt.show()

