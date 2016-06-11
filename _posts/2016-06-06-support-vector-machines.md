---
layout: post
title:  "Support Vector Machines"
subtitle:   ""
date:   2016-06-06
author: Run.D.Guan
header-img: "img/beij_meitu_1.jpg"
category: Machine-learning
tags:
    - Supervised-Learning
    - Classification
---

提及支持向量机 (SVM)，即使还不清楚其具体数学推导过程，也听说过SVM是通过找到一个最大不同类别之间间隔的超平面来进行分类的；或是当前线性不可分，SVM通过核技术将数据从低维映射到高维空间，从而数据线性可分。这也正是SVM的特点和能力所在，下面我们就来探讨下如何得到我们的SVM Classifier。

### Hard-margin

#### Hyper-plane and Margin

首先我们选取一个相对简单的情况 一 线性可分，假定我们已经有了训练数据集 $D=\\{(\mathbf{x}_1,y_1), (\mathbf{x}_2, y_2),\dots, (\mathbf{x}_n, y_n)\\},\quad  y_i\in\\{-1,+1\\}$ 如图1所示

![demo](http://7xqutp.com1.z0.glb.clouddn.com/svm0.png?imageView/2/w/550/q/100)

我们要做的就是找到那么一个超平面，使得离不同类别的样本最远，因为这样该分类器的鲁棒性最好，即使数据有噪声也不会轻易跑到另一类中去。设划分超平面方程为

$$ \mathbf{w}^T\mathbf{x}+b=0$$

要最大化间隔，就需要先把间隔表示出来。设正样本任意点 $(\mathbf{x}_i, y_i)$ 到超平面的距离为 $\gamma_i$，则该点在超平面的投影点的坐标为

$$\mathbf{x}=\mathbf{x}_i-\gamma_i\dfrac{\mathbf{w}}{||\mathbf{w}||}$$

将其带入超平面方程中，求解 $\gamma_i$ 得

$$
\gamma_i=\dfrac{\mathbf{w}^T\mathbf{x}_i+b}{||\mathbf{w}||}
$$

上面是针对正样本的，更一般的样本点到超平面的距离为

$$
\gamma _i=\dfrac{y_i(\mathbf{w}^T\mathbf{x}_i+b)}{||\mathbf{w}||}
$$

实际有效用的里超平面最近的点，是它卡住了超平面的位置，所以设全局几何间隔

$$
\gamma =\min_{i=1,2,\dots,n}\gamma_i
$$

我们希望至少对某个 $\rho$ 满足

$$
\gamma=\dfrac{y(\mathbf{w}^T\mathbf{x}+b)}{||\mathbf{w}||}\geq \rho
$$

并期望最大化 $\rho$。但同时缩放 $\mathbf{w}$ 和 $b$ 会得到无限多个解。为了能够得到唯一的解，这里限定 $\rho\vert\vert \mathbf{w}\vert\vert=1$，这样为了最大化间隔，就可以最小化 $\vert\vert \mathbf{w}\vert\vert$，同时为了数学计算方便，即最小化 $1/2\vert\vert \mathbf{w}\vert\vert^2$。于是我们得到了支持向量机的基本型

$$
\begin{aligned}
&\min_{\mathbf{w},b} \quad\dfrac{1}{2}||\mathbf{w}||^2 \\
&s.t. \quad y_i(\mathbf{w}^T\mathbf{x}_i+b)\geq 1, \qquad i=1,2,\dots,n.
\end{aligned}
$$

其中使得限制条件等式成立的点被称为支撑向量（support vector），支撑向量到超平面的距离为 $1/\vert\vert \mathbf{w}\vert\vert$，因此几何间隔为 $2/\vert\vert \mathbf{w}\vert\vert$。

#### Dual Problem

上面的基本型是凸二次规划问题，已经可以直接用最优化方法求解，但是我们可以通过拉格朗日对偶来更有效的解决该问题。根据本科所学的工科数学分析中条件极值[拉格朗日乘数法](https://en.wikipedia.org/wiki/Lagrange_multiplier)的知识可知，定义拉格朗日函数为

$$
\mathcal{L}(\mathbf{w},b,\mathbf{\alpha}) = \dfrac{1}{2}||\mathbf{w}||^2+\sum_{i=1}^{n}\alpha_i(1-y_i(\mathbf{w}^T\mathbf{x}_i+b))
$$

该非约束问题为求解 $\min_{\mathbf{w},b}\max_{\mathbf{\alpha}:\mathbf{\alpha}\geq0}\mathcal{L}(\mathbf{w},b,\mathbf{\alpha})$  。令 $\mathcal{L}(\mathbf{w},b,\mathbf{\alpha})$ 对 $\mathbf{w}$ 和 $b$ 的偏导为零可得

$$
\begin{aligned}
&\dfrac{\partial\mathcal{L}}{\partial \mathbf{w}}=0\quad \Rightarrow \quad \mathbf{w}=\sum_{i=1}^{n}\alpha_iy_i\mathbf{x}_i \\
&\dfrac{\partial\mathcal{L}}{\partial \mathbf{b}}=0\quad \Rightarrow \quad 0=\sum_{i=1}^{n}\alpha_iy_i
\end{aligned}
$$

将它们带入 $\mathcal{L}(\mathbf{w},b,\mathbf{\alpha})$ 即可消去 $\mathbf{w}$ 和 $b$，得到对偶问题为

$$
\begin{aligned}
\max_{\mathbf{\alpha}} \sum_{i=1}^{n}\alpha_i-\dfrac{1}{2}\sum_{i=1}^{n}\sum_{j=1}^{n}\alpha_i\alpha_jy_iy_j\mathbf{x}_i^T\mathbf{x}_j \\
\end{aligned}
$$

$$
\begin{aligned}
s.t. \quad &\sum_{i=1}^{n}\alpha_iy_i=0 \qquad\qquad\qquad\qquad\\
&\alpha_i\geq0,\qquad i=1,2,\dots,n.
\end{aligned}
$$

这个对偶问题可以这么形象理解一下，比如两个圆碗，底座相对上下放置，上面碗的最小值就是下面碗的最大值。更严格的有下面的数学关系

$$
d^*=\max_{\alpha:\alpha\geq=0}\min_{\mathbf{w},b}\mathcal{L}(\mathbf{w},b,\mathbf{\alpha}) \le \min_{\mathbf{w},b}\max_{\mathbf{\alpha}:\mathbf{\alpha}\geq0}\mathcal{L}(\mathbf{w},b,\mathbf{\alpha}) = p^*
$$

其中 $p^* \text{和 } d^*$ 分别为原问题（primal problem）和对偶问题（dual problem）的解，这里的特殊条件下，二者相等。

注意到SVM基本型的不等式约束，因此上述过程满足KKT条件，即

$$
\begin{cases}
		\alpha_i\geq 0  \\
		y_i(\mathbf{w}^T\mathbf{x}_i+b)-1\geq 0  \\
		\alpha_i(1-y_i(\mathbf{w}^T\mathbf{x}_i+b)) =0
\end{cases}
$$

可以看出，为满足KKT条件，要么 $\alpha_i=0$，要么$1-y_i(\mathbf{w}^T\mathbf{x}_i+b)=0$

* 若 $\alpha_i=0$ ，则在求解 $\mathbf{w}=\sum_{i=1}^{n}\alpha_iy_i\mathbf{x}_i$ 中不会起任何作用；
* 若 $\alpha_i>0$ ，则 $y_i(\mathbf{w}^T\mathbf{x}_i+b)=1$ ，其对应的样本点位于最大间隔边界上，即支撑向量。

这样体现了支撑向量的作用，分割平面的确定只与支撑向量有关。

![](http://7xqutp.com1.z0.glb.clouddn.com/svm_demo1.png?imageView/2/w/450/q/90)

上面说了一堆性质，对SVM有了一定的认识，可是还是不知道怎么解啊，下面就简单了解下如何求解该对偶问题的过程。对偶问题可以表述成如下的形式

$$
\max_{\alpha}\alpha^Te-\dfrac{1}{2}\alpha^TS\alpha
$$

其中 $e$ 为单位向量  $S=(y_i\mathbf{x}_i^T)(y_j\mathbf{x}_j)$ ，可以看出这是个二次规划问题，但该问题的规模依赖于样本大小，所以在实际任务中会造成很大开销。

为了避开这个障碍，根据问题本身的特性提出了SMO算法。SMO算法主要思路是固定其他参数，每次只通过一个参数求出其极值，以此类推，于是我们就得出了 $\alpha$，进而得到           $\mathbf{w}=\sum_{i=1}^{n}\alpha_iy_i\mathbf{x}_i$，带入到约束条件中，对所有支撑向量 $(\mathbf{x}_s,y_s)$ 都满足

$$
y_s(\sum_{i\in S}\alpha_iy_i\mathbf{x}_i^T\mathbf{x}_s+b)=1
$$

其中 $S$ 为支撑向量集合，两边同时乘以 $y_s$ 得

$$
\sum_{i\in S}\alpha_iy_i\mathbf{x}_i^T\mathbf{x}_s+b=y_s
$$

对任意一个支撑向量就可以求出一个 $b$ 来，为了数值稳定起见，我们通过所有支撑向量求出 $b$ 值，然后取平均。

$$
b=\dfrac{1}{|S|}\sum_{s\in S}\left(y_s-\sum_{i\in S}\alpha_iy_i\mathbf{x}_i^T\mathbf{x}_s\right)
$$

### Kernel

#### Feature Mapping

上面是关于线性可分的，如果像下面的这种非线性情况就需要将样本映射到高维空间去，然后在新空间使用线性模型。

![Nonlinear](http://7xqutp.com1.z0.glb.clouddn.com/kernel0.png?imageView/2/w/450/q/90)

假如我们选用一个radial basis function --- $r=\exp(-(x_1^2+x_2^2))$，则样本从空间 $\mathbf{x}=[x_1, x_2]^T$ 映射到 $\phi(\mathbf{x})=[x_1, x_2, r]^T$ 上去， $\phi$ 代表了 feature mapping， 效果如下所示

![map](http://7xqutp.com1.z0.glb.clouddn.com/kernel1.png?imageView/2/w/500/q/100)

显然在新的空间里线性可分，代码在[这里](https://github.com/GaryLv/GaryLv.github.io/blob/master/codes/Support%20Vector%20Machines/MappingDemo.py)。幸运的是，如果原始空间是有限维的，即属性有限，那么一定存在一个高维特征空间使样本可分。

有了 $\phi$ 以后，在特征空间的划分超平面变为为

$$
\mathbf{w}^T\phi(\mathbf{x})+b=0
$$

类似的，可以得到目标函数

$$
\begin{aligned}
&\min_{\mathbf{w},b} \quad\dfrac{1}{2}||\mathbf{w}||^2 \\
&s.t. \quad y_i(\mathbf{w}^T\phi(\mathbf{x}_i)+b)\geq 1, \qquad i=1,2,\dots,n.
\end{aligned}
$$

其对偶问题为

$$
\begin{aligned}
\max_{\mathbf{\alpha}} \sum_{i=1}^{n}\alpha_i-\dfrac{1}{2}\sum_{i=1}^{n}\sum_{j=1}^{n}\alpha_i\alpha_jy_iy_j\phi(\mathbf{x})_i^T\phi(\mathbf{x}_j) \\
\end{aligned}
$$

$$
\begin{aligned}
s.t. \quad &\sum_{i=1}^{n}\alpha_iy_i=0 \qquad\qquad\qquad\qquad\qquad\quad\\
&\alpha_i\geq0,\qquad i=1,2,\dots,n.
\end{aligned}
$$

因此求解过程只是变成了涉及计算 $\phi(\mathbf{x}_i)^T\phi(\mathbf{x}_j)$，即样本 $\mathbf{x}_i$ 与 $\mathbf{x}_j$ 映射到特征空间的内积。

#### Kernel Trick
由上可见mapping思想的强力功效，但稍一想想，感觉起码会有两个问题，一是面对一个新的问题，我怎么知道选取什么样的映射；二是我一顿把样本往高维映射，高维度会造成计算困难。对第一个问题我们后面介绍几种常见的核函数，这里先讨论下第二个问题。

设想一个函数满足

$$
K(\mathbf{X}_i, \mathbf{X}_j)=\left\langle \phi(\mathbf{X}_i), \phi(\mathbf{X}_j)  \right\rangle=\phi(\mathbf{X}_i)^T\phi(\mathbf{X}_j)
$$

看起来就是换了表示形式，那这个函数 $K(\cdot, \cdot)$ 有什么用呢。它的作用为不必将样本映射到特征空间去再做点积，而直接使用在原空间中函数 $K(\cdot, \cdot)$ 计算的结果。这就是**核技巧**，函数 $K(\cdot, \cdot)$ 被称为**核函数**。是否还是有疑问呢，它俩就相等吗？或是核函数怎么就降低了计算量的？下面我们通过NG课件里的一个例子来看看。

考虑一组三维数据的一种映射

$$
\phi(\mathbf{X})=\left[ \begin{matrix}
   x_1x_1  \\
   x_1x_2 \\
   x_1x_3  \\
   x_2x_1  \\
   x_2x_2  \\
   x_2x_3  \\
   x_3x_1  \\
   x_3x_2  \\
   x_3x_3 \\
   \sqrt{2c}x_1  \\
   \sqrt{2c}x_2  \\
   \sqrt{2c}x_3  \\
   c  \\
\end{matrix} \right]
$$

这个mapping看起来要麻烦一些了，然而其对应的核函数却极其简单

$$
\begin{aligned}
K(\mathbf{X}, \mathbf{Z})&=(\mathbf{X}^T\mathbf{Z}+c)^2 \\
&=\sum_{i,j=1}^{n}(x_ix_j)(z_iz_j)+\sum_{i=1}^{n}(\sqrt{2c}x_i)(\sqrt{2c}z_j)+c^2\\ &= \phi(\mathbf{X})^T\phi(\mathbf{Z})
\end{aligned}
$$

在此例中，只需将二者点乘后加 $c$ 求平方即可，而无需先做映射再求点积。所以我们也可以不用知道 $\phi(\cdot)$ 的具体形式。

#### Kernel Function
