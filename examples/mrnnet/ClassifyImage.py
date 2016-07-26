import os
os.environ["GLOG_minloglevel"] ="3"
import sys
import caffe
import numpy as np
import matplotlib.pyplot as plt

def SetDisplayDefaults() :
    plt.rcParams['figure.figsize'] = (10, 10)        # large images
    plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
    plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap


class Classifier():
    def __init__(self,modelDefFilename, modelWeightsFilename, meanImageFilename, labelsFilename ):
        self.net = caffe.Net( modelDefFilename, modelWeightsFilename, caffe.TEST )
        self.net.blobs['data'].reshape(50,3,227,227)

        mu = np.load(meanImageFilename)
        mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values

        # create transformer for the input called 'data'
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
        self.transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
        self.transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
        self.transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

        self.labels = np.loadtxt(labelsFilename, str, delimiter='\t')


    def Classify( self, imageFileName, nTopVals = 5 ) :
        image = caffe.io.load_image(imageFileName)
        self.net.blobs['data'].data[...] = self.transformer.preprocess('data', image)
        output = self.net.forward()
        output_prob = output['prob'][0]  # the output probability vector for the first image in the batch
        # sort top five predictions from softmax output
        top_inds = output_prob.argsort()[::-1][:nTopVals]  # reverse sort and take largest items
        retvals = [ (self.labels[i],output_prob[i]) for i in top_inds ]
        return retvals





def ClassifyImage(imageFileName) :
    modelDefFilename     = "E:\\home\\tools\\caffe\\models\\bvlc_reference_caffenet\\deploy.prototxt"
    modelWeightsFilename = "E:\\home\\tools\\caffe\\models\\bvlc_reference_caffenet\\bvlc_reference_caffenet.caffemodel"

    net = caffe.Net(modelDefFilename,      # defines the structure of the model
                    modelWeightsFilename,  # contains the trained weights
                    caffe.TEST)            # use test mode (e.g., don't perform dropout)



    # load the mean ImageNet image (as distributed with Caffe) for subtraction
    meanImageFilename = "E:\\home\\tools\\caffe\\python\\caffe\\imagenet\\ilsvrc_2012_mean.npy"
    mu = np.load(meanImageFilename)
    mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
    ### print 'mean-subtracted values:', zip('BGR', mu)

    # create transformer for the input called 'data'
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
    transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
    transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
    transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

    caffe.set_device(0)
    caffe.set_mode_gpu()
    ### caffe.set_mode_cpu()

    # set the size of the input (we can skip this if we're happy
    #  with the default; we can also change it later, e.g., for different batch sizes)
    net.blobs['data'].reshape(50,        # batch size
                               3,        # 3-channel (BGR) images
                             227, 227)   # image size is 227x227


    ### imageFileName = "E:\\home\\tools\\caffe\\examples\\images\\cat.jpg"
    image = caffe.io.load_image(imageFileName)
    plt.imshow(image)
    plt.show()
    ### wait = input("Press Enter to Continue")
    transformed_image = transformer.preprocess('data', image)

    # copy the image data into the memory allocated for the net
    net.blobs['data'].data[...] = transformed_image

    ### perform classification
    output = net.forward()

    output_prob = output['prob'][0]  # the output probability vector for the first image in the batch

    ### print 'predicted class is:', output_prob.argmax()

    # load ImageNet labels
    labelsFilename = "E:\\home\\tools\\caffe\\data\\ilsvrc12\\synset_words.txt"
    labels = np.loadtxt(labelsFilename, str, delimiter='\t')

    ### print 'output label:', labels[output_prob.argmax()]

    # sort top five predictions from softmax output
    top_inds = output_prob.argsort()[::-1][:5]  # reverse sort and take five largest items

    print 'labels (probabilities)'
    for i in top_inds:
        print "%s (%f)" % (labels[i],output_prob[i])
    ### print zip(output_prob[top_inds], labels[top_inds])


def main():
    ### SetDisplayDefaults()
    imageFilename = sys.argv[1]

    modelDefFilename     = "E:\\home\\tools\\caffe\\models\\bvlc_reference_caffenet\\deploy.prototxt"
    modelWeightsFilename = "E:\\home\\tools\\caffe\\models\\bvlc_reference_caffenet\\bvlc_reference_caffenet.caffemodel"
    meanImageFilename    = "E:\\home\\tools\\caffe\\python\\caffe\\imagenet\\ilsvrc_2012_mean.npy"
    labelsFilename       = "E:\\home\\tools\\caffe\\data\\ilsvrc12\\synset_words.txt"

    classifier = Classifier(modelDefFilename,modelWeightsFilename,meanImageFilename,labelsFilename)
    vals = classifier.Classify( imageFilename )
    for val in vals:
        print "%s (%f)" % (val[0],val[1])


if __name__ == '__main__':
    main()
