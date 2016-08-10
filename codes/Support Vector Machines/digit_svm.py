# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.datasets import load_digits
digits = load_digits()
digits.keys()

X = digits.data
y = digits.target
print(X.shape)
print(y.shape)

fig = plt.figure(figsize = (6, 6))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)

for i in range(64):
    ax = fig.add_subplot(8, 8, i+1, xticks=[], yticks=[])
    ax.imshow(digits.images[i], cmap=plt.cm.binary, interpolation='nearest')
    
    ax.text(0, 7, str(digits.target[i]))
  
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, random_state=0)  
for kernel in ['rbf', 'linear']:
    clf = SVC(kernel=kernel).fit(Xtrain, ytrain)
    ypred = clf.predict(Xtest)
    print("SVC: kernel = {0}".format(kernel))
    print(metrics.accuracy_score(ytest, ypred))
    plt.figure()
    plt.imshow(metrics.confusion_matrix(ypred, ytest),
               interpolation='nearest', cmap=plt.cm.binary)
    plt.colorbar()
    plt.xlabel("true label")
    plt.ylabel("predicted label")
    plt.title("SVC: kernel = {0}".format(kernel))