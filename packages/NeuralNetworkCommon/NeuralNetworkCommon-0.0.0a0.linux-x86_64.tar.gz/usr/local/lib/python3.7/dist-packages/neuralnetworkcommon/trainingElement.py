# coding=utf-8
# import
from pythoncommontools.objectUtil.POPO import POPO
# training element
class TrainingElement(POPO):
    # constructors
    @staticmethod
    def constructFromAttributes(input,expectedOutput):
        # initialize training element
        trainingElement = TrainingElement()
        # add attributs
        trainingElement.input=input
        trainingElement.expectedOutput=expectedOutput
        # return
        return trainingElement
    pass
