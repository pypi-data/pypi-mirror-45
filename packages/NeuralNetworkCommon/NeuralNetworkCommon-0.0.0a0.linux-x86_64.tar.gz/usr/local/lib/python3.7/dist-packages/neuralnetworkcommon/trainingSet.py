# coding=utf-8
# import
from pythoncommontools.objectUtil.POPO import POPO
# training set
class TrainingSet(POPO):
    # constructors
    @staticmethod
    def constructFromAttributes(id,trainingElements,workspaceId=None,comments=''):
        # initialize training set
        trainingSet = TrainingSet()
        # add attributs
        trainingSet.id=id
        trainingSet.workspaceId = workspaceId
        trainingSet.trainingElements=trainingElements
        trainingSet.comments=comments
        # return
        return trainingSet
    pass
# training set summary
class TrainingSetSummary(POPO):
    # constructors
    @staticmethod
    def constructFromAttributes(workspaceId,trainingElementsNumber,comments=''):
        # initialize training set summary
        trainingSetSummary = TrainingSetSummary()
        # add attributs
        trainingSetSummary.workspaceId = workspaceId
        trainingSetSummary.trainingElementsNumber=trainingElementsNumber
        trainingSetSummary.comments=comments
        # return
        return trainingSetSummary
    pass
pass
