from daal4py import logistic_regression_training, logistic_regression_prediction, logistic_regression_model
from sklearn.externals import joblib
from operator import itemgetter
import numpy as np
import pandas as pd
import random
import copy
import json
import math
import time
import os
import argparse
from collections import defaultdict, OrderedDict

class LR:
	def __init__(self, numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature):
		self.numTLSFeature = numTLSFeature
		self.numDNSFeature = numDNSFeature
		self.numHTTPFeature = numHTTPFeature
		self.numTimesFeature = numTimesFeature
		self.numLengthsFeature = numLengthsFeature
		self.numDistFeature = numDistFeature

	def train(self, data, label, outputFileName):		
		nClasses = 2
		#shuffle the data first
		tmp = list(zip(data, label))
		random.shuffle(tmp)
		data[:], label[:] = zip(*tmp)
		data = np.array(data)
		label = pd.DataFrame(label, dtype=np.float64)
		#begin train timing
		#print("Beginning train timing...")
		startTime = time.time()
		#saga, sgd, adagrad, lbfgs (default sgd)
		trainAlg = logistic_regression_training(nClasses=nClasses, interceptFlag=True)
		#setup train/test data
		dataLen = len(data)
		mark = 0.8
		upperBound = int(dataLen * mark)
		trainData = data[0:upperBound]
		trainLabel = label[0:upperBound]
		testData = data[upperBound:]
		testLabel = label[upperBound:]
		#train model
		#print("Training model...")
		trainResult = trainAlg.compute(trainData, trainLabel)
		#create prediction classe(s?)->[don't think second is needed]
		predictAlgTrain = logistic_regression_prediction(nClasses=nClasses)
		predictAlgTest = logistic_regression_prediction(nClasses=nClasses)
		#make train and test predictions
		predictResultTrain = predictAlgTrain.compute(trainData, trainResult.model)
		predictResultTest = predictAlgTest.compute(testData, trainResult.model)
		#end train timing
		endTime = time.time()
		print("Training and test elapsed in %s seconds" %(str(endTime - startTime)))
		#compare train predictions
		count = 0
		for i in range(0, len(trainLabel)):
			if trainLabel[0][i] == predictResultTrain.prediction[i]:
				count += 1
		trainAccu = float(count)/len(trainLabel)*100
		#compare test predictions
		count = 0
		for i in range(0, len(testLabel)):
			if testLabel[0][len(trainLabel) + i] == predictResultTest.prediction[i]:
				count += 1
		testAccu = float(count)/len(testLabel)*100
		#save the model to the output
		#print("saving model parameters into " + outputFileName)
		paramMap = {}
		paramMap["feature"] = {}
		paramMap["feature"]["tls"] = self.numTLSFeature
		paramMap["feature"]["dns"] = self.numDNSFeature
		paramMap["feature"]["http"] = self.numHTTPFeature
		paramMap["feature"]["times"] = self.numTimesFeature
		paramMap["feature"]["lengths"] = self.numLengthsFeature
		paramMap["feature"]["dist"] = self.numDistFeature
		joblib.dump(trainResult.model, 'model.pkl')
		json.dump(paramMap, open(outputFileName, 'w'))
		#accuracy
		return (trainAccu, testAccu)

	def test(self, data, label):
		startTime = time.time()
		#create prediction class
		predictAlg = logistic_regression_prediction(nClasses=2)
		#make predictions
		predictResultTest = predictAlg.compute(data, joblib.load('model.pkl'))
		endTime = time.time()
		print("Test elapsed in %s seconds" %(str(endTime - startTime)))
		#assess accuracy
		count = 0
		for i in range(0, len(label)):
			if label[i] == predictResultTest.prediction[i]:
				count += 1
		return float(count)/len(label)*100
