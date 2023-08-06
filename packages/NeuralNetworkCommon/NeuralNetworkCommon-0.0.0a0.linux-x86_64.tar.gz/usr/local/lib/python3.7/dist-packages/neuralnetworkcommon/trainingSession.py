# coding=utf-8
# import
from pythoncommontools.objectUtil.POPO import POPO
from random import shuffle
# training session progress
class TrainingSessionProgress(POPO):
    @staticmethod
    def constructFromAttributes(meanDifferentialErrors, errorElementsNumbers, resets):
        # initialize training set
        trainingSessionProgress = TrainingSessionProgress()
        # add attributs
        trainingSessionProgress.meanDifferentialErrors = meanDifferentialErrors
        trainingSessionProgress.errorElementsNumbers = errorElementsNumbers
        trainingSessionProgress.resets = resets
        # return
        return trainingSessionProgress
# training session
class TrainingSession(POPO):
    # constructors
    @staticmethod
    # INFO : test ration between 0 (no data used to test, all for training) and 1 (no data used to training, all for test)
    def constructFromTrainingSet(perceptronId,trainingSet,trainingChunkSize,saveInterval,maximumTry,maximumErrorRatio,testRatio,comments=''):
        # initialize trivial attributs
        trainingSession = TrainingSession()
        # add ids & comments
        trainingSession.perceptronId = perceptronId
        trainingSession.trainingSetId = trainingSet.id
        trainingSession.trainingChunkSize = trainingChunkSize
        trainingSession.saveInterval = saveInterval
        trainingSession.maximumTry = maximumTry
        trainingSession.maximumErrorRatio = maximumErrorRatio
        trainingSession.comments = comments
        # split training / test sets
        dataElements = trainingSet.trainingElements
        shuffle(dataElements)
        testSetLength = int(len(dataElements)*testRatio)
        trainingSession.testSet = dataElements[:testSetLength]
        trainingSession.trainingSet = dataElements[testSetLength:]
        # return
        return trainingSession
    @staticmethod
    def constructFromAttributes(perceptronId,trainingSetId,trainingChunkSize,saveInterval,maximumTry,maximumErrorRatio,trainingSet,testSet,pid,loadedLinesNumber,errorMessage,meanDifferentialErrors,errorElementsNumbers,resets,testScore,comments=''):
        # initialize training set
        trainingSession = TrainingSession()
        # add attributs
        trainingSession.perceptronId = perceptronId
        trainingSession.trainingSetId = trainingSetId
        trainingSession.trainingChunkSize = trainingChunkSize
        trainingSession.saveInterval = saveInterval
        trainingSession.maximumTry = maximumTry
        trainingSession.maximumErrorRatio = maximumErrorRatio
        trainingSession.trainingSet = trainingSet
        trainingSession.testSet = testSet
        trainingSession.pid = pid
        trainingSession.loadedLinesNumber = loadedLinesNumber
        trainingSession.errorMessage = errorMessage
        trainingSession.meanDifferentialErrors = meanDifferentialErrors
        trainingSession.errorElementsNumbers = errorElementsNumbers
        trainingSession.resets = resets
        trainingSession.testScore = testScore
        trainingSession.comments = comments
        # return
        return trainingSession
    pass
# training session summary
class TrainingSessionSummary(POPO):
    @staticmethod
    def constructFromAttributes(trainingSetId,trainingChunkSize,saveInterval,maximumTry,maximumErrorRatio,trainingSetsNumber,testSetsNumber,pid,loadedLinesNumber,errorMessage,progressRecordsNumber,meanDifferentialErrors,errorElementsNumbers,resets,testScore,comments=''):
        # initialize training set
        trainingSessionSummary = TrainingSessionSummary()
        # add attributs
        trainingSessionSummary.trainingSetId = trainingSetId
        trainingSessionSummary.trainingChunkSize = trainingChunkSize
        trainingSessionSummary.saveInterval = saveInterval
        trainingSessionSummary.maximumTry = maximumTry
        trainingSessionSummary.maximumErrorRatio = maximumErrorRatio
        trainingSessionSummary.trainingSetsNumber = trainingSetsNumber
        trainingSessionSummary.testSetsNumber = testSetsNumber
        trainingSessionSummary.pid = pid
        trainingSessionSummary.loadedLinesNumber = loadedLinesNumber
        trainingSessionSummary.errorMessage = errorMessage
        trainingSessionSummary.progressRecordsNumber = progressRecordsNumber
        trainingSessionSummary.meanDifferentialErrors = meanDifferentialErrors
        trainingSessionSummary.errorElementsNumbers = errorElementsNumbers
        trainingSessionSummary.resets = resets
        trainingSessionSummary.testScore = testScore
        trainingSessionSummary.comments = comments
        # return
        return trainingSessionSummary
    pass
pass