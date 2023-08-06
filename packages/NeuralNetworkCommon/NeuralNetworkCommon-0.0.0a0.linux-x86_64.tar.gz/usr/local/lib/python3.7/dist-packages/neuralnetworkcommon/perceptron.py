# coding=utf-8
# import
from numpy import exp, array
from pythoncommontools.objectUtil.POPO import POPO
from random import random
from copy import copy
# sigmoid
# TODO : create an abstract class for all future functions
# TODO : compute with spark each method
# TODO : add extra parameters : uncertainties, dilatation, offsets
class Sigmoid():
    @staticmethod
    def value(variables):
        arrayVariables = array(variables)
        #value = dilatations / (1 + exp(-array(arrayVariables) * uncertainties)) + offsets
        value = 1 / (1 + exp(-arrayVariables))
        return value
    @staticmethod
    # INFO : we compute the derivative from : value = sigmoïd(variables)
    def derivative(variables):
        arrayVariables = array(variables)
        #derivative = dilatations * uncertainties * arrayVariables * (1 - arrayVariables)
        derivative = variables * (1 - arrayVariables)
        return derivative
# training draft
class TrainingDraft():
    def __init__(self,input,output):
        self.input = input
        self.output = output
# layer
class Layer(POPO):
    # constructors
    '''
    TODO : add extras parameters (uncertainties/dilatations/offsets)
    all parameters should be randomized between some given ranges
    TODO : parallelize random array generation
    '''
    '''
    INFO : numpy arrays are not standrad object.
    they can not  transnsform attributs as map so they can not be easily transformed in JSON
    so we use a standard array for construction and will transforme it in numpy later
    '''
    @staticmethod
    def constructRandomFromDimensions(previousDimension, currentDimension):
        # initialize object
        layer = Layer()
        # random weights between -1/+1
        layer.weights = [[(random() - .5) * 2 for _ in range(previousDimension)] for _ in range(currentDimension)]
        # set biases to 0
        layer.biases = [0] * currentDimension
        # return
        return layer
    @staticmethod
    def constructFromAttributes(weights,biases):
        # initialize layer
        layer = Layer()
        # add attributs
        layer.weights=weights
        layer.biases=biases
        # return
        return layer
    def instanciateNormalize(self):
        normalizedLayer = copy(self)
        normalizedLayer.biases = [float(_) for _ in self.biases]
        normalizedLayer.weights = list()
        for lineIndex, weightsLine in enumerate(self.weights):
            normalizedLine = [float(_) for _ in weightsLine]
            normalizedLayer.weights.append(normalizedLine)
        return normalizedLayer
    pass
    # computation
    def passForward(self,input,training=False):
        # compute ouput
        # TODO : compute with spark 'weightsBiasInput'
        weightsBiasInput = array(self.weights).dot(array(input)) + array(self.biases)
        output = Sigmoid.value(weightsBiasInput)
        if training:
            self.trainingDraft = TrainingDraft(input, output)
        return output
    def differentialErrorOutput(self,expectedOutput):
        # TODO : compute with spark 'differentialError'
        differentialError = array(self.trainingDraft.output) - array(expectedOutput)
        return differentialError
    @staticmethod
    def differentialErrorHidden(previousDifferentielError,previousLayerWeights):
        # TODO : compute with spark 'differentialError'
        differentialErrors = array(previousDifferentielError) * array(previousLayerWeights)
        differentialError = sum(differentialErrors, 0)
        return differentialError
    def computeNewWeights(self,differentialErrorLayer):
        differentialOutputWeightsBiasInput = Sigmoid.derivative(array([self.trainingDraft.output]))
        # INFO : new differential error on layer will be used on next computation
        newDifferentialErrorWeightsBiases = (array(differentialErrorLayer) * differentialOutputWeightsBiasInput).T
        differentialErrorWeights = newDifferentialErrorWeightsBiases * array(self.trainingDraft.input)
        # TODO : optionaly correct oter metaparameters (offset, dilatation, ...)
        # INFO : old weights will be used on next computation
        oldWeights = self.weights
        # TODO : parametrize learning rate (here 0.5)
        self.weights = oldWeights - 0.5 * differentialErrorWeights
        return newDifferentialErrorWeightsBiases, oldWeights
    def computeNewBiases(self,differentialErrorWeightsBiases):
        # TODO : parametrize learning rate (here 0.5)
        newBiases = array(self.biases) - 0.5 * array(differentialErrorWeightsBiases).T
        # INFO : sometimes, new biases are like a 1*N matrix (and not just a N vector)
        if len(newBiases.shape)==2 and newBiases.shape[0]==1: newBiases=newBiases[0]
        self.biases = newBiases
    def passBackward(self,expectedOutput=None,differentialErrorWeightsBiasInput=None,previousLayerWeights=None):
        # TODO : compute with spark each parameter
        # TODO : parametrize learning rate (here 0.5)
        # TODO : add inertia
        # get differential error on layer regarding output or hidden one
        if expectedOutput :
            differentialErrorLayer = self.differentialErrorOutput(expectedOutput)
        else:
            differentialErrorLayer = self.differentialErrorHidden(differentialErrorWeightsBiasInput,previousLayerWeights)
        # compute new weights & biases
        newDifferentialErrorWeightsBiases, oldWeights = self.computeNewWeights(differentialErrorLayer)
        self.computeNewBiases(newDifferentialErrorWeightsBiases)
        # discard training draft
        del self.trainingDraft
        # return
        return newDifferentialErrorWeightsBiases, oldWeights
    pass
# perceptron
class Perceptron(POPO):
    # constructors
    @staticmethod
    def constructRandomFromDimensions(dimensions,workspaceId=None,comments=''):
        # initialize object
        perceptron = Perceptron()
        perceptron.workspaceId = workspaceId
        # create each layer
        perceptron.layers = [Layer.constructRandomFromDimensions(dimensions[index],dimensions[index+1]) for index in range(len(dimensions)-1)]
        # save comments
        perceptron.comments = comments
        # return
        return perceptron
    @staticmethod
    def constructFromAttributes(id,layers,workspaceId=None,comments=''):
        # initialize perceptron
        perceptron = Perceptron()
        # add attributs
        perceptron.id=id
        perceptron.workspaceId=workspaceId
        perceptron.layers=layers
        perceptron.comments=comments
        # return
        return perceptron
    # computing
    def passForward(self,input,training=False):
        # TODO : add a pipe to cascade passes (only if not training)
        # INFO : next input is actual output
        inputOutput = input
        for layer in self.layers:
            inputOutput = layer.passForward(inputOutput,training)
        return inputOutput
    def passBackward(self,expectedOutput):
        # pass on output
        layer = self.layers[-1]
        differentialErrorWeightsBiasInput, previousLayerWeights = layer.passBackward(expectedOutput=expectedOutput)
        # pass on hidden layers
        for hiddenLayerIndex in range(2, len(self.layers)+1):
            layer = self.layers[-hiddenLayerIndex]
            differentialErrorWeightsBiasInput, previousLayerWeights = layer.passBackward(differentialErrorWeightsBiasInput=differentialErrorWeightsBiasInput,previousLayerWeights=previousLayerWeights)
    def passForwardBackward(self,input,expectedOutput):
        # pass forward
        actualOutput = self.passForward(array(input),True)
        # compute total error
        outputError = ( ( array(expectedOutput) - array(actualOutput) ) ** 2 ) / 2
        totalError = sum(outputError)
        # pass backward
        self.passBackward(expectedOutput)
        # return
        return totalError
    pass
# layer summary
class LayerSummary():
    # constructors
    @staticmethod
    def constructFromAttributes(weightsDimensions,biasesDimension):
        # initialize layer summary
        layerSummary = LayerSummary()
        # add attributs
        layerSummary.weightsDimensions=weightsDimensions
        layerSummary.biasesDimension=biasesDimension
        # return
        return layerSummary
    pass
# perceptron summary
class PerceptronSummary(POPO):
    # constructors
    @staticmethod
    def constructFromAttributes(workspaceId,layersSummary,comments=''):
        # initialize perceptron summary
        perceptronSummary = PerceptronSummary()
        # add attributs
        perceptronSummary.workspaceId=workspaceId
        perceptronSummary.layersSummary=layersSummary
        perceptronSummary.comments=comments
        # return
        return perceptronSummary
    pass
pass
