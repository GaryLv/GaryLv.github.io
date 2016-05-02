# -*- coding: utf-8 -*-
"""
knn分类iris的前两个属性，并可视化分类结果
"""
from sklearn.datasets import load_iris
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
iris = load_iris()
# X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data, iris.target, test_size=0.4, random_state=1)
X_train = iris.data[:, :2]
y_train = iris.target

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

# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

x_min, x_max = X_train[:, 0].min()-1, X_train[:, 0].max()+1
y_min, y_max = X_train[:, 1].min()-1, X_train[:, 1].max()+1
h = 0.2
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h)) 
X_test = np.c_[xx.ravel(), yy.ravel()]

prediction = []
for i in range(len(X_test)):
    # print('Classifying test instance number ' + str(i) +':')
    neighbours = get_neighbours(X_test[i], X_train, y_train, 5)
    majority_vote = get_majority(neighbours)
    prediction.append(majority_vote)
#  
prediction = np.array(prediction).reshape(xx.shape)
plt.figure()
plt.pcolormesh(xx, yy, prediction, cmap=cmap_light)
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cmap_bold)
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.show()
