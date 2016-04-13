---
layout: post
title:  "Linear Regression"
date:   2016-02-06
author: Run.D.Guan
header-img: "img/post-bg-2015.jpg"
category: Machine-learning
tags:
    - Supervised-Learning
    - Regression
---

### 线性回归背景

>回归分析是对客观事物数量依存关系的分析，是处理多个变量之间相互关系的一种数理统计方法．线性回归是通过线性预测函数来建模，其模型参数由数据估计出来。

线性回归应用范围很广，主要应用可以划归为如下两类：

* 如果目标是预测，线性回归可以通过观察数据集 $y$ 和 $X$ 的值来拟合出预测模型。之后对新增的数据 $X$ 就可以预测出对应的 $y$ 值。
* 给定变量 $y$ 和一系列与 $y$ 相关的变量 $X_1, \dots, X_p$，线性回归可以计算出各变量 $X_j$ 与 $y$ 之间的关系程度。

### 理论模型

设定 $x^{(i)}$ 为输入变量，也可称为输入特征；而 $y^{(i)}$ 称作输出或目标函数。有着 $n$ 个训练样本的数据集记作 $\\{(x^{(i)},y^{(i)}); i=1,\dots,n\\}$，上角标 $i$ 为训练集的索引值。线性回归的任务（有监督学习）是根据已有的训练集数据，学习出一个函数 $h:X\rightarrow y$，使得 $h(x)$ 对于相应的 $y$ 有较好的预测能力，描述如下式

$$
\begin{aligned}
h_\theta(x)=\theta_0+\theta_1x_1+\dots + \theta_px_p
\end{aligned}
$$

其中 $\theta_i$ 是线性函数 $X$ 映射到 $y$ 的参数（也被称为权重），$p$ 是维度。在没有歧义的情况下 $h_\theta (x)$ 简写为 $h(x)$。为了简化标记，令 $x_0=1$，因此

$$
h(x)=\sum_{j=0}^{p}\theta_jx_j=\theta^Tx
$$

那么对于一组给定的训练集，我们如何选取参数 $\theta$ 呢？一种合理的想法是让 $h(x)$ 尽可能的接近于 $y$，这里我们定义**目标函数**：

$$
    J(\theta)=\frac{1}{2n}\sum_{i=1}^{n} \left( h_\theta(x^{(i)})-y^{(i)} \right) ^2
$$

如果最小化 $J(\theta)$，我们可以得到对该数据集拟合程度最好的模型参数 $\theta$。

### 梯度下降法
要最小化目标函数就要引入优化算法，这里介绍简单好用的梯度下降法。梯度下降法的思想是以初始猜想 $\theta$ 为起点，把当前位置负梯度方向作为搜索方向，因为该方向为当前位置的最快下降方向，所以也被称为是“最速下降法”。迭代过程如下

$$
\theta_j:=\theta_j-\alpha\dfrac{\partial}{\partial \theta_j}J(\theta)
$$

其中 $\alpha$ 为学习率。为了应用该算法，我们需要计算公式右侧的偏微分项，为方便起见假设我们只有一个训练样本 $(x,y)$ ，这样可以得出

$$
\begin{aligned}
    \dfrac{\partial}{\partial \theta_j}J(\theta)&=\frac{\partial}{\partial \theta_j}\dfrac{1}{2}(h(x)-y)^2 \\
        &= 2\cdot \frac{1}{2}(h(x)-y)\cdot \frac{\partial}{\partial \theta_j}(h(x)-y) \\
        &= (h(x)-y)\cdot\dfrac{\partial}{\partial \theta_j}\left( \sum\nolimits_{i=0}^{p}\theta_ix_i-y\right) \\
        &= (h(x)-y)x_j
\end{aligned}
$$

对上式进行扩展，有两种方式来对多个样本进行推导

* **批量梯度下降法**

$
\begin{aligned}
\qquad \qquad
\text{Repeat until convergence} \\{  \\
\end{aligned}
$

$ \qquad \qquad \qquad
\theta_j:=\theta_j-\alpha\sum_{i=1}^{n}(h(x^{(i)})-y^{(i)})x_j^{(i)} \qquad(\text{for every }j)
$

$\qquad \qquad \\}$

* **随机梯度下降法**

$\qquad \qquad \text{Loop} \\{$

$\qquad \qquad \qquad \text{for } i=1 \text{ to } m \\{ $

$\qquad \qquad \qquad \qquad \theta_j:=\theta_j-\alpha(h(x^{(i)})-y^{(i)})x_j^{(i)} \qquad(\text{for every }j) $

$\qquad \qquad \qquad  \\}$

$\qquad \qquad \\}$

通常情况下随机梯度下降会收敛的更快，但可能不会收敛到最小值处而是在其附近震荡。当数据量很大时，更推荐随机梯度下降法。

### Example
下面用一个单变量线性回归的例子来解释说明上面的理论知识。数据在[这里](https://www.coursera.org/learn/machine-learning/programming/8f3qT/linear-regression)，代表着不同城市的人口数与在该地区开餐馆的收益情况，我们的任务是如果给定了一个城市的人口数量，我们可以预测出相应的收益。首先先看看数据是什么样，这样对理解问题很有帮助。

![visual](http://7xqutp.com1.z0.glb.clouddn.com/figure_10.png?imageView/2/w/500/q/90)

可以看出单变量线性回归可以解决该问题，即根据当前数据集拟合 $y = \theta_0+\theta_1x$ 方程。我们定义cost function，即均方误差和

```python
    def computeCost(x, y, theta):
        totalError = 0
        m = len(y)
        for i in range(0, m):
            totalError += (y[i] - (theta[0] + theta[1]*x[i])) ** 2
        return totalError / (2 * m)
```

观察一下cost function，它的取极小值点就是我们要求的参数值。
![cost](http://7xqutp.com1.z0.glb.clouddn.com/CostF.png?imageView/2/w/500/q/90)

针对该问题，批量梯度下降法的公式可以直接表述为

$$
\theta_0  := \theta_0 - \alpha \dfrac{1}{n}\sum_{i=1}^{n}(h_\theta(x^{(i)})-y^{(i)}) \\
 \theta_1 := \theta_1 - \alpha \dfrac{1}{n}\sum_{i=1}^{n}(h_\theta(x^{(i)})-y^{(i)})\cdot x^{(i)}_1
$$

每一步都会更新 $\theta_0$ 和 $\theta_1$使得目标函数一点点减少，代码如下

```python
    def gradientDescent(x, y, theta, alpha, num_iters):
        n = len(y);
        J_history = []
        for iters in range(num_iters):
            gradient = [0, 0]
            for i in range(n):
                gradient[0] += (theta[0] + theta[1]*x[i] - y[i])
                gradient[1] += (theta[0] + theta[1]*x[i] - y[i]) * x[i]
            theta[0] -= alpha/n*gradient[0]
            theta[1] -= alpha/n*gradient[1]
            J_history.append(computeCost(x, y, theta))
        return [theta, J_history]    
```

经过迭代之后可以求得相应的模型参数，将该结果可视化如下图所示
![result](http://7xqutp.com1.z0.glb.clouddn.com/rg2.png?imageView/2/w/500/q/90)

**scikit-learn实现**
对一些典型的问题可以直接调用库来实现，既省时间又可保证正确性。scikit-learn是一款非常好的开源的Python机器学习库，这里我们应用scikit-learn里的函数来解决该问题

```python
    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn import datasets, linear_model

    x = []; y = []
    f = open('ex1data1.txt')
    for line in f.readlines():
        lineArr = line.split(',')
        x.append([float(lineArr[0])])
        y.append([float(lineArr[1])])

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(x, y)

    # Plot outputs
    plt.scatter(x, y,  color='red')
    plt.plot(x, regr.predict(x), color='blue', linewidth=3)
```

![sk_result](http://7xqutp.com1.z0.glb.clouddn.com/figure_s1.png?imageView/2/w/500/q/90)

上面只是直观的查看结果，如需以后的计算还需知晓模型的参数。输出模型参数如下

```python
print('Interception: %f' % regr.intercept_)
print('Coefficient: ' + repr(regr.coef_))
```
结果如果如下：

    Interception: -3.895781
    Coefficient: array([ 1.19303364])

可见scikit-learn的功能与便捷~推荐一个可视化库Seaborn，Matplotlib是Python主要的绘图库。但是它本身就很复杂，你的图经过大量的调整才能变精致。Seaborn本质上使用Matplotlib作为核心库。先来看效果吧

![sns_result](http://7xqutp.com1.z0.glb.clouddn.com/figure_sns1.png?imageView/2/w/500/q/90)

ggplot2的风格，带上95%置信区间，还不错吧，这其实就一行代码

```python
    from pandas import DataFrame
    import seaborn as sns
    # 省去读入数据，和第一个程序段相同
    data = {'population': x, 'profit': y}
    frame = DataFrame(data)
    sns.jointplot( "population" , "profit" , frame, kind = 'reg')
```

### 概率解释

这里从概率的角度解释下为什么cost function长那个模样，虽然最小二乘的形式似乎是那么的自然，但从中心极限定理等概率角度出发，便可以对其作出合理的解释，有种这些知识点居然还有这等联系的感觉。

假设目标变量和输入变量的关系如下

$$
    y^{(i)}=\theta^Tx^{(i)}+\epsilon^{(i)}
$$

其中 $\epsilon^{(i)}$ 为误差项，代表模型中没有考虑的因素以及随机噪声。更深入地，假设 $\epsilon^{(i)}$ 是独立同分布的（**IID**），服从均值为0，方差为某定值 $\sigma^2$ 的高斯分布，所以 $\epsilon^{(i)}$ 的概率密度函数为

$$
    p(\epsilon^{(i)})=\dfrac{1}{\sqrt{2\pi}\sigma}\exp\left(-\dfrac{(\epsilon^{(i)})^2}{2\sigma^2}\right)
$$

因此

$$
    p(y^{(i)}|x^{(i)};\theta)=\dfrac{1}{\sqrt{2\pi}\sigma}\exp\left(-\dfrac{(y^{(i)}-\theta^Tx^{(i)})^2}{2\sigma^2}\right)
$$

上式表示在给定 $x^{(i)}$ 和参数 $\theta$ 条件下， $y^{(i)}$ 的分布。模型的最终目标是希望在全部样本上预测最准，也就是概率积最大，这个概率积就是似然函数（在 $\epsilon^{(i)}$'s 相互独立的假设条件下），表示如下

$$
\begin{aligned}
    L(\theta) &=\prod_{i-1}^{n}p(y^{(i)}|x^{(i)};\theta) \\
    &= \prod_{i=1}^{n}\dfrac{1}{\sqrt{2\pi}\sigma}\exp\left(-\dfrac{(y^{(i)}-\theta^Tx^{(i)})^2}{2\sigma^2}\right)
\end{aligned}
$$

对其取对数可得

$$
\begin{aligned}
    \mathcal{L}(\theta) &= \log L(\theta) \\
        &= \log \prod_{i=1}^{n}\dfrac{1}{\sqrt{2\pi}\sigma}\exp\left( -\dfrac{(y^{(i)}-\theta^Tx^{(i)})^2}{2\sigma^2}\right) \\
        &= \sum_{i=1}^{n} \log \dfrac{1}{\sqrt{2\pi}\sigma}\exp\left( -\dfrac{(y^{(i)}-\theta^Tx^{(i)})^2}{2\sigma^2}\right) \\
        &= n\log \dfrac{1}{\sqrt{2\pi}\sigma} -\dfrac{1}{2\sigma^2}\sum_{i=1}^{n}(y^{(i)}-\theta^Tx^{(i)})^2
\end{aligned}
$$

因此，最大化 $\mathcal{L}$ ，就是最小化

$$
    \frac{1}{2}\sum_{i=1}^{n}(y^{(i)}-\theta^Tx^{(i)})^2
$$

可以看出经过最大似然估计推导出来的待优化的目标函数与 cost function是等价的。其实在概率模型中，目标函数的原函数（或对偶函数）极小化（或极大化）与极大似然估计等价，这是一个带有普遍性的结论。

**总结：**在这里简单介绍了线性回归，以及用于计算参数的梯度下降法，并用Python实现了单变量线性回归，同时引入scikit-learn库，方便的计算出模型参数并可视化拟合结果，最后以概率角度解读了线性回归的损失函数。

### Reference

- [https://en.wikipedia.org/wiki/Linear_regression](https://en.wikipedia.org/wiki/Linear_regression)
- [http://cs229.stanford.edu/materials.html](http://cs229.stanford.edu/materials.html)
- [https://spin.atomicobject.com/2014/06/24/gradient-descent-linear-regression/](https://spin.atomicobject.com/2014/06/24/gradient-descent-linear-regression/)
- [http://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares](http://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares)
- [http://www.tuicool.com/articles/7NzaEvq](http://www.tuicool.com/articles/7NzaEvq)
- [http://www.52caml.com/head_first_ml/ml-chapter1-regression-family/](http://www.52caml.com/head_first_ml/ml-chapter1-regression-family/)
