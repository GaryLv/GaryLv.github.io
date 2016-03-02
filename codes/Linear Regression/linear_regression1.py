# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

matplotlib.rcParams['text.usetex'] = True
# matplotlib.rcParams['text.latex.unicode'] = True
from mpl_toolkits.mplot3d import Axes3D

def computeCost(x, y, theta):
    totalError = 0
    m = len(y)
    for i in range(0, m):
        totalError += (y[i] - (theta[0] + theta[1]*x[i])) ** 2
    return totalError / (2 * m)
    
    
def gradientDescent(x, y, theta, alpha, num_iters):
    m = len(y);
    J_history = []
    for iters in range(num_iters):
        gradient = [0, 0]
        for i in range(m):
            #print(theta[0] )#+ theta[1]*x[i] - y[i]
            gradient[0] += (theta[0] + theta[1]*x[i] - y[i])
            gradient[1] += (theta[0] + theta[1]*x[i] - y[i]) * x[i]
        theta[0] -= alpha/m*gradient[0]
        theta[1] -= alpha/m*gradient[1]
        J_history.append(computeCost(x, y, theta)) 
    return [theta, J_history]

if __name__ == '__main__':
    x = []; y = []
    f = open('ex1data1.txt')
    for line in f.readlines():
        lineArr = line.split(',')
        x.append(float(lineArr[0]))
        y.append(float(lineArr[1]))
    
    theta = [0, 0]
    alpha = 0.01
    iterations = 1500
    [theta, J] = gradientDescent(x, y, theta, alpha, iterations)
    xl = np.linspace(5, 23, 20)
    yl = theta[0] + xl * theta[1]
    plt.plot(x, y, 'r.')
    plt.plot(xl, yl, 'b')
    plt.xlabel('Population')
    plt.ylabel('Profit')
    
    fig = plt.figure(2)
    ax = fig.gca(projection = '3d')
    X = np.arange(-10, 5, 0.2)
    Y = np.arange(-1, 3, 0.02)
    X, Y = np.meshgrid(X, Y)
    Z = computeCost(x, y, [X, Y])
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0.3)
    ax.contour(X, Y, Z, zdir='z', offset=0, cmap=cm.coolwarm)
    # plt.rc('text', usetex=True)
    ax.set_xlabel(r'\theta_0')
    ax.set_ylabel(r'\theta_1')
    ax.set_zlabel(r'J(\theta_0,\theta_1)')
