# -*- coding: utf-8 -*-
"""
LR 非线性边界分类
"""

import numpy as np
import matplotlib.pyplot as plt

def loadDataSet():
    x = []; y = []; 
    fr = open('ex2data2.txt')
    for line in fr.readlines():
        lineArr = line.strip().split(',')
        x.append([1.0, float(lineArr[0]), float(lineArr[1])])
        y.append(float(lineArr[2]))
    return x, y

def feature_set(d, e):     # e为最高幂次和，且默认d[0]=1
    features = [1]
    for n in range(1, e+1):
        for i in range(n+1):
            features.append(pow(d[1],n-i) * pow(d[2],i))
    return features

def logistic_regression(data, label, alpha = 0.01, lamda = 0.001):    
    n, m = np.shape(data)
    w = np.zeros(m)
    for times in range(1000):
        gradient = np.zeros(m);
        for i in range(n):
            gradient += (label[i] - 1.0/(1+np.exp(-sum(w*data[i]))))* data[i]
        w = w + alpha * gradient  + lamda*w
    return w

    
if __name__ == '__main__':
    scores, result = loadDataSet()
    scores = np.array(scores)
    n = np.shape(scores)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(result[i]) == 1:
            xcord1.append(scores[i,1]); ycord1.append(scores[i,2])
        else:
            xcord2.append(scores[i,1]); ycord2.append(scores[i,2])
                   
    plt.figure()
    plt.scatter(xcord1, ycord1, s = 90, c = 'b', marker = '+')
    plt.scatter(xcord2, ycord2, s = 60, c = 'r', alpha = 0.6)
    plt.legend(['Accepted', 'Rejected'])
    plt.xlim([-1.1, 1.5])
    plt.ylim([-0.95, 1.3])
    
    data = []; e = 6
    for i in range(n):
        features = feature_set(scores[i], e)
        data.append(features)
    
    w = logistic_regression(np.array(data), result, 0.001, 0.001) 
    xx = np.arange(-1, 1.5, 0.01)
    yy = np.arange(-0.8, 1.2, 0.01)
    X, Y = np.meshgrid(xx, yy)
    Z = np.zeros([len(xx), len(yy)])
    for i in range(len(xx)):
        for j in range(len(yy)):
            Z[i,j] = sum(feature_set([1.0, xx[i], yy[j]], e) * w)
    
    cs = plt.contour(xx, yy, Z.T, [0], colors = 'g', linewidths = 2)
    
