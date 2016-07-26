import re
import numpy as np
import matplotlib.pyplot as plt
import sys


#### filename='mrnnetQuickGPU.1000000.log'

def parseLogFile( filename ) :
   ### Iteration 2000, loss = 0.679579
   iterLossPattern = re.compile('Iteration ([0-9]+), loss = ([0-9\.]+)')

   ### Iteration 0, lr = 0.01
   iterLearningPattern = re.compile('Iteration ([0-9]+), lr = ([0-9\.e\-]+)')

   ### Iteration 10000, Testing net (#0)
   iterTestingPattern = re.compile('Iteration ([0-9]+), Testing net')

   ### Test net output #0: accuracy = 0.607766
   accuracyTestPattern = re.compile('Test net output #\d: accuracy = ([0-9\.e\-]+)')

   ### Test net output #1: loss = 1.35449 (* 1 = 1.35449 loss)
   lossTestPattern = re.compile('Test net output #\d: loss = ([0-9\.]+)')

   ### Train net output #0: accuracy = 0.4375
   accuracyTrainPattern = re.compile('Train net output #\d: accuracy = ([0-9\.e\-]+)')

   trainLossIterations = []
   trainLoss=[]
   trainAccuracy = []
   trainAccuracyIterations = []

   trainLearningRateIterations =[]
   trainLearningRate = []

   testIterations = []
   testAccuracy = []
   testLoss = []

   ### nIterationDivisor = 10000
   nIterationDivisor = 1000

   for line in open(filename,'r'):
       m = iterLossPattern.search( line )
       if m:
           iteration = int(m.group(1)) / nIterationDivisor
           loss = float(m.group(2))
           trainLossIterations.append( iteration )
           trainLoss.append( loss )

       m = iterLearningPattern.search( line )
       if m:
           iteration = int( m.group(1) ) / nIterationDivisor
           learningRate = float( m.group(2) )
           trainLearningRateIterations.append(iteration)
           trainLearningRate.append( learningRate )

       m = iterTestingPattern.search( line )
       if m:
           iteration = int( m.group(1) ) / nIterationDivisor

       m = accuracyTestPattern.search( line )
       if m:
           testAcc = float( m.group(1) )
           testIterations.append( iteration )
           testAccuracy.append( testAcc )

       m = accuracyTrainPattern.search( line )
       if m:
           trainAcc = float( m.group(1) )
           trainAccuracyIterations.append( iteration )
           trainAccuracy.append( trainAcc )


       m = lossTestPattern.search( line )
       if m:
           testLossValue = float( m.group(1) )
           testLoss.append( testLossValue )


   plt.subplot(2,2,1)
   plt.plot( trainLossIterations, trainLoss )
   plt.title('Training Loss vs Iteration')

   ### plt.subplot(2,2,2)
   ### plt.plot( trainLearningRateIterations, trainLearningRate )
   ### plt.title( 'Learning Rate vs Iteration')

   plt.subplot(2,2,2)
   plt.plot( trainAccuracyIterations, trainAccuracy )
   plt.title( 'Training Accuracy vs Iteration')
   plt.xlabel('Iteration x %d' % nIterationDivisor )


   plt.subplot(2,2,3)
   plt.plot( testIterations, testLoss )
   plt.title( 'Test Loss vs Iteration')
   plt.xlabel('Iteration (%ds)' % nIterationDivisor )

   plt.subplot(2,2,4)
   plt.plot( testIterations, testAccuracy )
   plt.title( 'Test Accuracy vs Iteration')
   plt.xlabel('Iteration x %d' % nIterationDivisor )



   plt.show()




parseLogFile( sys.argv[1] )



