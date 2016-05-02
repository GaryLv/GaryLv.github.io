# -*- coding: utf-8 -*-

from sklearn.metrics import classification_report, accuracy_score
from sklearn.datasets import load_iris
from sklearn import cross_validation
from collections import Counter
import numpy as np

iris = load_iris()
X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data, iris.target, test_size=0.4, random_state=1)

def get_distance(test_instance, training_set):
    # test_instance is the data point we want to evaluate, and training_set is the original dataset
    dataSize = training_set.shape[0]    
    diffs_squared = (np.tile(test_instance, (dataSize, 1)) - training_set) ** 2
    return np.sqrt(np.sum(diffs_squared, axis=1))

def get_neighbours(test_instance, training_set, labels, k):
    # return first k nearest neighbor
    distances = get_distance(test_instance, training_set)
    sortedIndex = distances.argsort()
    sortedNeighours = labels[sortedIndex]
    return sortedNeighours[:k]
    
def get_majority(neighbours):
    count = Counter(neighbours)
    return count.most_common()[0][0]
    
prediction = []
for i in range(len(X_test)):
    # print('Classifying test instance number ' + str(i) +':')
    neighbours = get_neighbours(X_test[i], X_train, y_train, 5)
    majority_vote = get_majority(neighbours)
    prediction.append(majority_vote)
    print('Predicted labe=' + str(majority_vote) + ', Acually label=' + str(y_test[i]))
    
print('\nThe overall accuracy of the model is: ' + str(accuracy_score(y_test, prediction)) + '\n')
report = classification_report(y_test, prediction, target_names = iris.target_names)
print('A detailed classification report:\n' + report)