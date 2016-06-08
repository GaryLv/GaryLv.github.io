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

![demo](http://7xqutp.com1.z0.glb.clouddn.com/svm0.png "图1 间隔与超平面示意图")

我们要做的就是找到那么一个超平面，使得离不同类别的样本最远，因为这样该分类器的鲁棒性最好，即使数据有噪声也不会轻易跑到另一类中去。设划分超平面方程为

$$ \mathbf{w}^T\mathbf{x}+b=0$$

要最大化间隔，就需要先把间隔表示出来。设正样本任意点 $(\mathbf{x}^{(i)}, y^{(i)})$ 到超平面的距离为 $\gamma ^{(i)}$，则该点在超平面的投影点的坐标为

$$\mathbf{x}=\mathbf{x}^{(i)}-\gamma ^{(i)}\dfrac{\mathbf{w}}{||\mathbf{w}||}$$

将其带入超平面方程中，求解 $r^{(i)}$ 得

$$
\gamma ^{(i)}=\dfrac{\mathbf{w}^T\mathbf{x}^{(i)}+b}{||\mathbf{w}||}
$$

上面是针对正样本的，更一般的样本点到超平面的距离为

$$
\gamma ^{(i)}=\dfrac{y^{(i)}(\mathbf{w}^T\mathbf{x}^{(i)}+b)}{||\mathbf{w}||}
$$

实际有效用的里超平面最近的点，是它卡住了超平面的位置，所以设全局几何间隔

$$
\gamma =\min_{i=1,2,\dots,n}\gamma^{(i)}
$$

我们希望至少对某个 $\rho$ 满足

$$
\gamma=\dfrac{y(\mathbf{w}^T\mathbf{x}+b)}{||\mathbf{w}||}\geq \rho
$$

并期望最大化 $\rho$。但同时缩放 $\mathbf{w}$ 和 $b$ 会得到无限多个解。为了能够得到唯一的解，这里限定 $\rho\vert\vert \mathbf{w}\vert\vert=1$，这样为了最大化间隔，就可以最小化 $\vert\vert \mathbf{w}\vert\vert$，同时为了数学计算方便，即最小化 $1/2\vert\vert \mathbf{w}\vert\vert^2$。于是我们得到了支持向量机的基本型

$$
\begin{aligned}
&\min_{\mathbf{w},b} \quad\dfrac{1}{2}||\mathbf{w}||^2 \\
&s.t. \quad y^{(i)}(\mathbf{w}^T\mathbf{x}^{(i)}+b)\geq 1, \qquad i=1,2,\dots,n.
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
&\dfrac{\partial\mathcal{L}}{\partial \mathbf{w}}=0\quad \Rightarrow \quad \mathbf{w}=\sum_{i=0}^{n}\alpha_iy_i\mathbf{x}_i \\
&\dfrac{\partial\mathcal{L}}{\partial \mathbf{b}}=0\quad \Rightarrow \quad 0=\sum_{i=0}^{n}\alpha_iy_i
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
s.t. \quad &\sum_{i=0}^{n}\alpha_iy_i=0 \qquad\qquad\qquad\qquad\\
&\alpha_i\geq0,\qquad i=1,2,\dots,n.
\end{aligned}
$$

这个对偶问题可以这么形象理解一下，比如两个圆碗，底座相对上下放置，上面碗的最小值就是下面碗的最大值。更严格的有下面的数学关系

$$
d^*=\max_{\alpha:\alpha\geq=0}\min_{\mathbf{w},b}\mathcal{L}(\mathbf{w},b,\mathbf{\alpha}) \le \min_{\mathbf{w},b}\max_{\mathbf{\alpha}:\mathbf{\alpha}\geq0}\mathcal{L}(\mathbf{w},b,\mathbf{\alpha}) = p^*
$$

其中 $p^*$ 和 $d^*$ 分别为原问题（primal problem）和对偶问题（dual problem）的解，这里的特殊条件下，二者相等。
