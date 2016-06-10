# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets.samples_generator import make_circles
from sklearn.svm import SVC    # "Support Vector Classifier"

def plot_svc_decision_function(clf, ax=None):
    """Plot the decision function for a 2D SVC"""
    if ax is None:
        ax = plt.gca()
    x = np.linspace(plt.xlim()[0], plt.xlim()[1], 30)
    y = np.linspace(plt.ylim()[0], plt.ylim()[1], 30)
    Y, X = np.meshgrid(y, x)
    P = np.zeros_like(X)
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            P[i, j] = clf.decision_function([xi, yj])
    # plot the margins
    ax.contour(X, Y, P, colors='k',
               levels=[-1, 0, 1], alpha=0.5,
               linestyles=['--', '-', '--'])


X, y = make_circles(100, factor=.1, noise=.1)

plt.scatter(X[:, 0], X[:, 1], c = y, s=80, cmap='coolwarm')

r = np.exp(-(X[:, 0] **2 + X[:, 1] **2))
# r = np.array(-(X[:, 0] **2 + X[:, 1] **2))
plt.figure(2)
ax = plt.gca(projection='3d')
ax.scatter3D(X[:, 0], X[:, 1], r, c=y, s=80, cmap='coolwarm')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('r')

clf = SVC(kernel='rbf')
clf.fit(X, y)

plt.figure(3)
plt.scatter(X[:, 0], X[:, 1], c=y, s=80, cmap='coolwarm')
plot_svc_decision_function(clf)
plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=200, facecolors='none')

