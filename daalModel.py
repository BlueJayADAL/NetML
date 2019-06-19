from daal4py import logistic_regression_training, logistic_regression_prediction
from daal4py import decision_forest_classification_training, decision_forest_classification_prediction
from daal4py import svm_training, svm_prediction, kernel_function_linear
from tensorflow import keras
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
		#create prediction classes
		predictAlgTrain = logistic_regression_prediction(nClasses=nClasses)
		predictAlgTest = logistic_regression_prediction(nClasses=nClasses)
		#make train and test predictions
		predictResultTrain = predictAlgTrain.compute(trainData, trainResult.model)
		predictResultTest = predictAlgTest.compute(testData, trainResult.model)
		#end train timing
		endTime = time.time()
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
		print("Training and test (Logistic Regression) elapsed in %s seconds" %(str(endTime - startTime)))
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
		joblib.dump(trainResult.model, 'LRmodel.pkl')
		json.dump(paramMap, open(outputFileName, 'w'))
		#accuracy
		return (trainAccu, testAccu)
	def test(self, data, label):
		startTime = time.time()
		#create prediction class
		predictAlg = logistic_regression_prediction(nClasses=2)
		#make predictions
		predictResultTest = predictAlg.compute(data, joblib.load('LRmodel.pkl'))
		endTime = time.time()
		print("Test (Logistic Regression) elapsed in %s seconds" %(str(endTime - startTime)))
		#assess accuracy
		count = 0
		for i in range(0, len(label)):
			if label[i] == predictResultTest.prediction[i]:
				count += 1
		return float(count)/len(label)*100

class DF:
	def __init__(self, numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature):
		self.numTLSFeature = numTLSFeature
		self.numDNSFeature = numDNSFeature
		self.numHTTPFeature = numHTTPFeature
		self.numTimesFeature = numTimesFeature
		self.numLengthsFeature = numLengthsFeature
		self.numDistFeature = numDistFeature
	def train(self, data, label, outputFileName):
		#shuffle the data first
		tmp = list(zip(data, label))
		random.shuffle(tmp)
		data[:], label[:] = zip(*tmp)
		data = np.array(data)
		label = pd.DataFrame(label, dtype=np.float64)
		#begin train timing
		#print("Beginning train timing...")
		startTime = time.time()
		#Decision Forest
		trainAlg = decision_forest_classification_training(2, nTrees=100, maxTreeDepth=0)
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
		#create prediction classes
		predictAlgTrain = decision_forest_classification_prediction(2) 
		predictAlgTest = decision_forest_classification_prediction(2) 
		#make train and test predictions
		predictResultTrain = predictAlgTrain.compute(trainData, trainResult.model) 
		predictResultTest = predictAlgTest.compute(testData, trainResult.model) 
		#end train timing
		endTime = time.time()
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
		print("Training and test (Decision Forest) elapsed in %s seconds" %(str(endTime - startTime)))
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
		joblib.dump(trainResult.model, 'DFmodel.pkl')
		json.dump(paramMap, open(outputFileName, 'w'))
		#accuracy
		return (trainAccu, testAccu)
	def test(self, data, label):
		startTime = time.time()
		#create prediction class
		predictAlg = decision_forest_classification_prediction(2)
		#make predictions
		predictResultTest = predictAlg.compute(data, joblib.load('DFmodel.pkl'))
		endTime = time.time()
		print("Test (Decision Forest) elapsed in %s seconds" %(str(endTime - startTime)))
		#assess accuracy
		count = 0
		for i in range(0, len(label)):
			if label[i] == predictResultTest.prediction[i]:
				count += 1
		return float(count)/len(label)*100

class SVM:
	def __init__(self, numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature):
		self.numTLSFeature = numTLSFeature
		self.numDNSFeature = numDNSFeature
		self.numHTTPFeature = numHTTPFeature
		self.numTimesFeature = numTimesFeature
		self.numLengthsFeature = numLengthsFeature
		self.numDistFeature = numDistFeature
	def train(self, data, label, outputFileName):
		#make 0 values -1
		label = [-1 if i==0 else 1 for i in label]
		#shuffle the data first
		tmp = list(zip(data, label))
		random.shuffle(tmp)
		data[:], label[:] = zip(*tmp)
		data = np.array(data)
		label = pd.DataFrame(label, dtype=np.float64)
		#begin train timing
		#print("Beginning train timing...")
		startTime = time.time()
		#Support Vector Machine
		kern = kernel_function_linear(method='defaultDense')
		trainAlg = svm_training(nClasses=2, C=1e+6, maxIterations=1e+7, cacheSize=2000, kernel=kern, accuracyThreshold=1e-3, doShrinking=True) 
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
		#create prediction classes
		predictAlgTrain = svm_prediction(nClasses=2, kernel=kern) 
		predictAlgTest = svm_prediction(nClasses=2, kernel=kern) 
		#make train and test predictions
		predictResultTrain = predictAlgTrain.compute(trainData, trainResult.model) 
		predictResultTest = predictAlgTest.compute(testData, trainResult.model) 
		#end train timing
		endTime = time.time()
		#compare train predictions
		count = 0
		for i in range(0, len(trainLabel)):
			if (trainLabel[0][i] > 0 and predictResultTrain.prediction[i] > 0) or (trainLabel[0][i] < 0 and predictResultTrain.prediction[i] < 0):
				count += 1
		trainAccu = float(count)/len(trainLabel)*100
		#compare test predictions
		count = 0
		for i in range(0, len(testLabel)):
			if (testLabel[0][len(trainLabel) + i] > 0 and predictResultTest.prediction[i] > 0) or (testLabel[0][len(trainLabel) + i] < 0 and predictResultTest.prediction[i] < 0):
				count += 1
		testAccu = float(count)/len(testLabel)*100
		print("Training and test (Support Vector Machine) elapsed in %s seconds" %(str(endTime - startTime)))
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
		joblib.dump(trainResult.model, 'SVMmodel.pkl')
		json.dump(paramMap, open(outputFileName, 'w'))
		#accuracy
		return (trainAccu, testAccu)
	def test(self, data, label):
		startTime = time.time()
		#create prediction class
		kern = kernel_function_linear(method='defaultDense')
		predictAlg = svm_prediction(nClasses=2, kernel=kern)
		#make predictions
		predictResultTest = predictAlg.compute(data, joblib.load('SVMmodel.pkl'))
		endTime = time.time()
		print("Test (Support Vector Machine) elapsed in %s seconds" %(str(endTime - startTime)))
		#assess accuracy
		count = 0
		for i in range(0, len(label)):
			if (label[i] > 0 and predictResultTest.prediction[i] > 0) or (label[i] < 0 and predictResultTest.prediction[i] < 0):
				count += 1
		return float(count)/len(label)*100


class ANN:
	def __init__(self, numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature):
		self.numTLSFeature = numTLSFeature
		self.numDNSFeature = numDNSFeature
		self.numHTTPFeature = numHTTPFeature
		self.numTimesFeature = numTimesFeature
		self.numLengthsFeature = numLengthsFeature
		self.numDistFeature = numDistFeature
	def train(self, data, label, outputFileName):
		epochs = 100
		#shuffle the data first
		tmp = list(zip(data, label))
		random.shuffle(tmp)
		data[:], label[:] = zip(*tmp)
		data = np.array(data)
		label = np.array(label)
		#begin train timing
		#print("Beginning train timing...")
		startTime = time.time()
		#ANN
		#initialize
		model = keras.models.Sequential()
		#add layers (23-13-11-7-5)
		model.add(keras.layers.Dense(units=23, input_dim=331, activation='relu'))
		model.add(keras.layers.Dense(units=13, activation='relu'))
		model.add(keras.layers.Dense(units=11, activation='relu'))
		model.add(keras.layers.Dense(units=7, activation='relu'))
		model.add(keras.layers.Dense(units=5, activation='relu'))
		#add output layer for binary
		model.add(keras.layers.Dense(1, activation='sigmoid'))
		#compile model
		model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
		#setup train/test data
		dataLen = len(data)
		mark = 0.8
		upperBound = int(dataLen * mark)
		trainData = data[0:upperBound]
		trainLabel = label[0:upperBound]
		testData = data[upperBound:]
		testLabel = label[upperBound:]
		#train/fit model
		#print("Training model...")
		model.fit(trainData, trainLabel, epochs=epochs, batch_size=1000)
		#make train and test predictions
		predictResultTrain = model.predict_classes(trainData)
		predictResultTest = model.predict_classes(testData)
		#end train timing
		endTime = time.time()
		#sum prediction results
		correctTrain = np.sum(trainLabel == predictResultTrain.flatten(), axis = 0)
		correctTest = np.sum(testLabel == predictResultTest.flatten(), axis = 0)
		#compare train predictions
		trainAccu = float(correctTrain)/len(trainLabel)*100
		#compare test predictions
		testAccu = float(correctTest)/len(testLabel)*100
		print("Training and test (Artificial Neural Network [%d epochs]) elapsed in %s seconds" %(epochs, str(endTime - startTime)))
		#save model
		modelJSON = model.to_json()
		with open("ANNmodel.json", "w") as json_file:
			json_file.write(modelJSON)
		#serialize weights to HDF5
		model.save_weights("ANNmodel.h5")
		print("Saved model to disk.")
		#accuracy
		return (trainAccu, testAccu)
	def test(self, data, label):
		startTime = time.time()
		#read in trained model
		jsonFile = open('ANNmodel.json', 'r')
		loadedModelJSON = jsonFile.read()
		jsonFile.close()
		loadedModel = keras.models.model_from_json(loadedModelJSON)
		# load weights into new model
		loadedModel.load_weights("ANNmodel.h5")
		print("Loaded model from disk")
		#compile model
		loadedModel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
		#make predictions
		predictResultTest = loadedModel.predict_classes(data)
		endTime = time.time()
		print("Test (Artificial Neural Network) elapsed in %s seconds" %(str(endTime - startTime)))
		#assess accuracy
		correctTest = np.sum(label == predictResultTest.flatten(), axis = 0)
		return float(correctTest)/len(label)*100
