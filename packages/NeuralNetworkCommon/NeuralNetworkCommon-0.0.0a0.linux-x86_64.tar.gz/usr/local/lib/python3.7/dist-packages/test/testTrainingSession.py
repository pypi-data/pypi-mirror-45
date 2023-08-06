#!/usr/bin/env python3
# coding=utf-8
from unittest import TestCase
from random import randint, random
from neuralnetworkcommon.perceptron import Perceptron
from neuralnetworkcommon.trainingElement import TrainingElement
from neuralnetworkcommon.trainingSet import TrainingSet
from neuralnetworkcommon.trainingSession import TrainingSession
# import
# test perceptron
class testTrainingSession(TestCase):
    # test sigmoid computing
    def testConstructFromTrainingSet(self):
        # randomize perceptron
        layersNumber = randint(2,12)
        dimensions = [randint(2,100) for _ in range(layersNumber)]
        perceptron = Perceptron.constructRandomFromDimensions(dimensions)
        # randomize training set
        trainingElements = list()
        trainingSize = randint(15, 95)
        inputDimension = randint(20, 100)
        outputDimension = randint(20, 100)
        for _ in range(trainingSize):
            input = [(random() - .5) * 2 for _ in range(inputDimension)]
            expectedOutput = [(random() - .5) * 2 for _ in range(outputDimension)]
            trainingElement = TrainingElement.constructFromAttributes(input, expectedOutput)
            trainingElements.append(trainingElement)
        trainingSet = TrainingSet.constructFromAttributes(None,trainingElements)
        expectedDataSet = set(trainingSet.trainingElements)
        # generate training session
        trainingSession = TrainingSession.constructFromTrainingSet(perceptron,trainingSet,randint(2,10),randint(100,200),randint(1,10),randint(1,10),random(),random())
        # check trainer
        actualTrainingSet = set(trainingSession.trainingSet)
        actualTestSet = set(trainingSession.testSet)
        commonData = actualTrainingSet.intersection(actualTestSet)
        actualDataSet = actualTrainingSet.union(actualTestSet)
        self.assertSetEqual(commonData, set(), "ERROR : test & training data collides")
        self.assertSetEqual(actualDataSet,expectedDataSet, "ERROR : merged test & training data does not fill data set")
        pass
    pass
pass
