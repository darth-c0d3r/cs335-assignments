import util
import numpy as np
import sys
import random

PRINT = True

###### DON'T CHANGE THE SEEDS ##########
random.seed(42)
np.random.seed(42)

def small_classify(y):
    classifier, data = y
    return classifier.classify(data)

class AdaBoostClassifier:
    """
    AdaBoost classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    
    """

    def __init__( self, legalLabels, max_iterations, weak_classifier, boosting_iterations):
        self.legalLabels = legalLabels
        self.boosting_iterations = boosting_iterations
        self.classifiers = [weak_classifier(legalLabels, max_iterations) for _ in range(self.boosting_iterations)]
        self.alphas = [0]*self.boosting_iterations

    def train( self, trainingData, trainingLabels):
        """
        The training loop trains weak learners with weights sequentially. 
        The self.classifiers are updated in each iteration and also the self.alphas 
        """
        
        self.features = trainingData[0].keys()
        # "*** YOUR CODE HERE ***"

        # this code can be written more efficiently using numpy
        # not done using that because we are using util.Counter() class or normal python lists

        sample_weights = [1.0/len(trainingData)] * len(trainingData)
        for i in range(self.boosting_iterations):
            self.classifiers[i].train(trainingData, trainingLabels, sample_weights)
            error = 0.0
            for j in range(len(trainingData)):
                if self.classifiers[i].classify([trainingData[j]])[0] != trainingLabels[j]:
                    error += sample_weights[j]
            for j in range(len(trainingData)):
                if self.classifiers[i].classify([trainingData[j]])[0] == trainingLabels[j]:
                    sample_weights[j] *= error / (1.0-error)

            # normalize sample_weights
            total = sum(sample_weights)
            for j in range(len(sample_weights)):
                sample_weights[j] /= total

            self.alphas[i] = np.log((1.0-error)/error)

        # util.raiseNotDefined()

    def classify( self, data):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label. This is done by taking a polling over the weak classifiers already trained.
        See the assignment description for details.

        Recall that a datum is a util.counter.

        The function should return a list of labels where each label should be one of legaLabels.
        """

        # "*** YOUR CODE HERE ***"

        guesses = []
        
        for datum in data:
            guess = 0
            for i in range(self.boosting_iterations):
                guess += self.alphas[i] * self.classifiers[i].classify([datum])[0]
            guess = np.sign(guess)
            if guess == 0:
                guess = np.random.choice(self.classifiers[0].legalLabels)
            guesses.append(guess)
        return guesses


        # util.raiseNotDefined()