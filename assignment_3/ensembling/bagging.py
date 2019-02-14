import util
import numpy as np
import sys
import random

PRINT = True

###### DON'T CHANGE THE SEEDS ##########
random.seed(42)
np.random.seed(42)

class BaggingClassifier:
    """
    Bagging classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    
    """

    def __init__( self, legalLabels, max_iterations, weak_classifier, ratio, num_classifiers):

        self.ratio = ratio
        self.num_classifiers = num_classifiers
        self.classifiers = [weak_classifier(legalLabels, max_iterations) for _ in range(self.num_classifiers)]

    def train( self, trainingData, trainingLabels):
        """
        The training loop samples from the data "num_classifiers" time. Size of each sample is
        specified by "ratio". So len(sample)/len(trainingData) should equal ratio. 
        """

        self.features = trainingData[0].keys()
        # "*** YOUR CODE HERE ***"

        for i in range(self.num_classifiers):
            sampleData = util.Counter()
            sampleLabels = util.Counter()
            for j in range(int(self.ratio * len(trainingData))):
                idx = random.randint(0, len(trainingData)-1)
                sampleData[j], sampleLabels[j] = trainingData[idx], trainingLabels[idx]
            self.classifiers[i].train(sampleData, sampleLabels)

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
            for i in range(self.num_classifiers):
                guess += self.classifiers[i].classify([datum])[0]
            guess = np.sign(guess)
            if guess == 0:
                guess = np.random.choice(self.classifiers[0].legalLabels)
            guesses.append(guess)
        return guesses

        # util.raiseNotDefined()
