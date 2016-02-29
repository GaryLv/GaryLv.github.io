---
layout: post
title:  "Logistic Regression"
subtitle:   ""
date:   2016-02-21
author: Run.D.Guan
header-img: "img/post-bg-miui6.jpg"
category: Machine-learning
tags:
    - Supervised-Learning
    - Classification
---

我们这回来谈论下分类问题，跟回归问题不同，它的输出是离散值，以表征属于哪一类，而不同于回归的输出连续域的值。那如何判定属于哪一类呢，可以通过概率来给出结果。对于简单的二分类问题，如果属于正类的概率 $P_+$ 大于负类的概率 $ P_-=1-P_+$，那么可以断定它属于正类，输出1，反之则输出0。

首先从几何角度来理解下将输入空间分成两类，假设只有两个输入变量，且边界函数如下

$$
    \theta_0+\theta_1x_1+\theta_2x_2
$$

现有一个坐标点 $(a,b)$，代入边界函数中得到输出值 $\theta_0+\theta_1a+\theta_2b$。假设 $(a,b)$ 处于正类，那么计算结果值域为 $(0,\infty)$。且数值结果越大，代表该点离边界越远，也就说明它属于正类的概率越大。因此，$P_+\in (0.5,1]$。既然我们已经有了输出值在 $(-\infty, \infty)$ 区间，那怎么映射到 $P_+$ 的 $[0,1]$ 区间内呢，答案是**几率函数（odds）**。

### **Introduction**

$P(X)$ 为事件$X$发生的概率，几率（$OR(X)$）定义为 $P(X)/(1-P(X)$，即事件发生概率比上没有发生的概率。现在已经从 $P(X)$ 的 $0$ 到 $1$ 转变成 $OR(X)$ 的从 $0$ 到 $\infty$ 。现在还没有达边界函数值从 $-\infty$ 到 $\infty$，这时对 $OR(X)$ 取对数，叫做log-odds function。因此 $\log(OR(X))$ 变成了从 $-\infty$ 到 $\infty$ 的了，也就是说可以<u>用log-odds function来代表边界函数的代入值</u>。在二维的例子中，给定一点 $(a,b)$，下面就是Logistic regression的计算步骤

**step 1.** 计算边界函数值（即log-odds function），$\theta_0+\theta_1a+\theta_2b$，简记为 $t$。

**step 2.** 计算几率（Odds Ratio），$OR_+=e^t$。

**step 3.** 已知 $OR_+$ 后，根据几率和概率的关系计算 $P_+=\dfrac{OR_+}{1+OR_+}$。

因此，结合上面几步我们可以得到

$$
P_+=\dfrac{e^t}{1+e^t}
$$

该式的右侧就是**logistic function**。下面的工作就是如何确定边界函数的参数啦。

### **Logistic regression**

这里我们的**hypotheses** $h_\theta(x)$ 形式如下

$$
    h_\theta(x)=g(\theta^Tx)=\dfrac{1}{1+e^{-\theta^Tx}}
$$

其中 $\theta^Tx=\theta_0+\sum\nolimits_{j=1}^{p}\theta_jx_j$，$g(z)$ 表达式如下

$$
g(z)=\dfrac{1}{1+e^{-z}}
$$

它就是 **logistic function** 或称作 **sigmoid function**。如下是 $g(z)$ 的曲线图
      ![lg](http://7xqutp.com1.z0.glb.clouddn.com/lg.png?imageView/2/w/450/q/90)

先来考察下这个 sigmoid function 有什么有用的性质:

$\bullet \quad  g(-z) = 1-g(z)$

$\bullet \quad  g'(z) = g(z)(1-g(z))$

其中 $g'(z)$ 推导如下

$$
\begin{aligned}
        g'(z) &= \dfrac{d}{dz}\dfrac{1}{1+e^{-z}} \\
        &= \dfrac{1}{(1+e^{-z})^2}(e^{-z}) \\
        &= \dfrac{1}{1+e^{-z}}\cdot\left( 1-\dfrac{1}{1+e^{-z}}\right)  \\
        &= g(z)(1-g(z))
\end{aligned}
$$

一个样本可以理解为发生的一次事件，样本生成的过程即事件发生的过程。对于0/1分类问题来讲，产生的结果有两种可能，符合伯努利试验的概率假设。因此，我们可以说样本的生成过程即为伯努利试验过程，产生的结果（0/1）服从伯努利分布。这里我们假设结果为1的概率为 $h_\theta(x)$，结果为0的概率为 $1−h_\theta(x)$。

假设

$$
\begin{aligned}
    P(y=1|x;\theta)&=h_\theta(x) \\
    P(y=0|x;\theta)&=1-h_\theta(x)
\end{aligned}
$$

注意到可以将二者合并成

$$
    P(y|x;\theta)=(h_\theta(x))^y(1-h_\theta(x))^{1-y}
$$

假设有着$n$个独立的训练样本，参数的似然函数为

$$
\begin{aligned}
    L(\theta)&=P(\mathbf{y}|X;\theta) \\
    &=\prod_{i=1}^{n}P(y^{(i)}|x^{(i)};\theta) \\
    &=\prod_{i=1}^{n}(h_\theta(x^{(i)}))^{y^{(i)}}(1-h_\theta(x^{(i)}))^{1-y^{(i)}}
\end{aligned}
$$

和之前一样，最大化log似然函数更方便计算

$$
\begin{aligned}
    \mathcal{L}(\theta) &= \log L(\theta) \\
    &= \sum_{i=1}^{n}y^{(i)}\log h(x^{(i)})+(1-y^{(i)})\log(1-h(x^{(i)}))
\end{aligned}
$$

和线性回归类似，这里我们也用梯度下降法来最大化似然函数，向量化表示为 $\theta:=\theta+\alpha\nabla_\theta\mathcal{L}(\theta)$。（加号表征是求解最大化问题）首先对一个样本 $(x,y)$ 来推导随机梯度下降法：

$$
\begin{aligned}
        \dfrac{\partial}{\partial \theta_j}\mathcal{L}(\theta) &= \left( y\dfrac{1}{g(\theta^Tx)}-(1-y)\dfrac{1}{1-g(\theta^Tx)}\right) \dfrac{\partial}{\partial \theta_j}g(\theta^Tx) \\
        &=\left( y\dfrac{1}{g(\theta^Tx)}-(1-y)\dfrac{1}{1-g(\theta^Tx)}\right) g(\theta^Tx)(1-g(\theta^Tx))\dfrac{\partial}{\partial\theta_j}\theta^Tx \\
            &= \left( y(1-g(\theta^Tx))-(1-y)g(\theta^Tx)\right) x_j \\
            &= (y-h_\theta(x))x_j
\end{aligned}
$$

上式用到了性质 $g'(z) = g(z)(1-g(z))$，因此随机梯度下降法的迭代步骤如下

$$
    \theta_j:=\theta_j+\alpha\left(y^{(i)}-h_\theta(x^{(i)})\right)x_j^{(i)}
$$

其中 $\alpha$ 表示学习率。该学习规律与线性回归具有相同的形式。线性回归是根据高斯分布和极大似然估计推导出来的，而logistic regression是由伯努利分布和极大似然估计推导出来的，把能推导成类似形式的称为指数族分布。

### **Example 1** -- 线性边界分类

第一例是[《机器学习实战》](https://www.manning.com/books/machine-learning-in-action#downloads)第五章的仿真数据。首先当然还是先观察下数据
![raw](http://7xqutp.com1.z0.glb.clouddn.com/lg1.png?imageView/2/w/500/q/90)

可以直观的感觉到可以通过一条直线将其分成两类。根据随机梯度下降的迭代公式，Python代码如下

```python
def logistic_regression(data, label, alpha = 0.001):    
    n, m = np.shape(data)
    w = np.ones(m)
    for times in range(1000):
        for i in range(n):
            h = 1.0/(1+np.exp(-sum(data[i]*w)))
            w += alpha * (label[i] - h) * data[i]
    return w
```

这也就是logistic regression的核心部分，根据计算出的参数就可得到边界方程 $w_0+w_1x_1+w_2x_2=0$，由此做出分类结果图如下

![c](http://7xqutp.com1.z0.glb.clouddn.com/lg2.png?imageView/2/w/500/q/90)

分类结果还是不错的，可以对其进行其他应用。

### **Example 2** -- Nonlinear decision boundary
下面来做一个非线性分类边界的问题，问题背景是这样的：工厂生产的芯片有两种测量标准，我们要根据这两种测量标准判断芯片是否质量合格。数据源于[Andrew Ng的课程](https://www.coursera.org/learn/machine-learning/programming/ixFof/logistic-regression)。首先我们还是先来观察下数据
![non](http://7xqutp.com1.z0.glb.clouddn.com/non1.png?imageView/2/w/500/q/90)
可以看出边界是个圆弧形，这时要对自身那两个属性值( $x_1, x_2$ )做下多项式变换以应对非线性边界。这里我们来点狠的，让多项式最高幂次为6，这样的好处是 --- 可以练习下[正则化](https://en.wikipedia.org/wiki/Regularization_(mathematics)) -.-! 这时属性向量如下：

$$
\text{mapFeature}(x)=\begin{bmatrix}
                        1 \\
                        x_1 \\
                        x_2 \\
                        x_1^2 \\
                        x_1x_2 \\
                        x_2^2 \\
                        x_1^3 \\
                        \vdots \\
                        x_1x_2^5 \\
                        x_2^6
                    \end{bmatrix}
$$

与以往上来拿着样本的属性值就用不同，这回要做多项式特征，代码如下：

```python
def feature_set(d, e):     # e为最高幂次和，且默认d[0]=1
    features = [1]
    for n in range(1, e+1):
        for i in range(n+1):
            features.append(pow(d[1],n-i) * pow(d[2],i))
    return features
```

这里有个问题就需要思考一下了，好像之前讲的线性回归和现在的logistic regression都是线性模型，现在弄了一堆特征乘在了一起，是不是说明LR就是非线性模型了呢？嗯。。不是的，它还是线性模型。因为线不线性看的是你模型参数（这里的 $\theta$ ）是不是线性的，它没有做任何的非线性变换，所以是线性的。 那些属性值乘来乘去，好像非线性很高，其实乘完了不就是一个数值而已，不影响模型的线性度。其实LR是一种广义的线性回归。

那么根据梯度下降法，计算模型参数过程如下（带正则化项 $\lambda$ ）

```python
def logistic_regression(data, label, alpha = 0.01, lamda = 0.001):   
    n, m = np.shape(data)
    w = np.zeros(m)
    for times in range(1000):
        gradient = np.zeros(m);
        for i in range(n):
            gradient += (label[i] - 1.0/(1+np.exp(-sum(w*data[i]))))* data[i]
        w = w + alpha * gradient  + lamda*w
    return w
```

计算出参数后，根据 $h_\theta(x)=g(\theta^Tx)=0$ ，就可做出分界面来，其中 $g(\cdot)$ 为sigmoid函数，结果可视化如下
![nb](http://7xqutp.com1.z0.glb.clouddn.com/non2.png?imageView/2/w/500/q/90)

分类结果还是不错的，这个正则化项要是小的话，结果就是边界曲线很弯曲，普适性差；正则化项大了的话就是精度低，会有好多错误的分类结果。

### **Example 3** -- Multi-classification with scikit-learn
这里我们采用的数据是著名的[Iris Data Set](http://archive.ics.uci.edu/ml/datasets/Iris)，Iris是以鸢尾花的特征作为数据来源，数据集包含150个数据集，分为3类（Iris setosa, Iris virginica and Iris versicolor），每类50个数据，每个数据包含4个属性，为萼片和花瓣的长度和宽度。为突出LR的分类结果，简化其他过程，这里我们只选取花瓣的长度和宽度这两种属性。

```python
from sklearn import datasets
iris = datasets.load_iris()
X = iris.data[:, [2, 3]]# 只选出 petal length 和 petal width 两个属性
y = iris.target
print('Class labels: ', np.unique(y))
```

将数据集分成训练集和测试集，并将数据标准化。

```python
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
# 标准化features
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)
```

采用LR训练数据，可视化分类结果，其中LR的参数C是正则化项（定义为 $C=1/ \lambda$），越大代表正则化强度越低。

```python
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(C = 1000.0, random_state = 0)
lr.fit(X_train_std, y_train)

X_combined_std = np.vstack((X_train_std, X_test_std))
y_combined = np.hstack((y_train, y_test))
plot_decision_regions(X_combined_std, y_combined, classifier=lr)
```

![iris](http://7xqutp.com1.z0.glb.clouddn.com/lgsk.png?imageView/2/w/500/q/90)

代码的完整版可以在[这里](https://github.com/GaryLv/GaryLv.github.io/blob/master/codes/LRsk.py)查看。对于一组数据，可通过类似 `lr.predict_proba(X_test_std[0,:])` 代码输出值来判断分类结果，如该输出为

    [[  2.05743774e-11   6.31620264e-02   9.36837974e-01]]

属于最后一类的概率最大，所以它可以被划归为class 2。

### Reference
* [https://codesachin.wordpress.com/2015/08/16/logistic-regression-for-dummies/](https://codesachin.wordpress.com/2015/08/16/logistic-regression-for-dummies/)
* [http://www.52caml.com/head_first_ml/ml-chapter1-regression-family/](http://www.52caml.com/head_first_ml/ml-chapter1-regression-family/)
* [https://www.coursera.org/learn/machine-learning](https://www.coursera.org/learn/machine-learning)
*  S. Raschka, Python Machine Learning, Packt Publishing, 2015.
