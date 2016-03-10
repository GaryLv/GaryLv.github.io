---
layout: post
title:  "Naive Bayes"
date:   2016-03-07
author: Run.D.Guan
header-img: "img/post-star1.jpg"
category: Machine-learning
tags:
    - Supervised-Learning
    - Classification
---

朴素贝叶斯是一种分类方法，计算量小可以用于实时决策，同时适合多分类问题。算法的性质决定了他广泛应用于文本分类，垃圾过滤，情感分析以及推荐系统等。根据名称就知道他的数学背景是贝叶斯理论，我们肯定是先要弄明白贝叶斯理论了。贝叶斯这套东西很神奇啊，他会给人莫名的一种靠谱的感觉，就觉得这东西说的有道理。统计学上还有贝叶斯学派和概率学派之争，唉，贵圈真乱~[这里](http://mp.weixin.qq.com/s?__biz=MzAxMzU5MTQ5MA==&mid=207004374&idx=1&sn=91f6220fb70ba87ba267d6d0a1fd8855#rd)有小短文一篇，讲了下二者的区别。下面就开始介绍贝叶斯定理啦。

### 贝叶斯定理
贝叶斯定理数学表达式如下：

$$
    P(A|B)=\dfrac{P(B|A)P(A)}{P(B)}
$$

其中
 $$P(B)=\sum_{i=1}^{n}P(B \bigcap A_i)=\sum_{i=1}^{n}P(B|A_i)P(A_i)$$
 <br>贝叶斯定理证明也很简单，将上式的分母乘到左侧，可以看出左右都等于联合概率 $P(A,B)$ ，得证。

下面通过一个经典检测吸毒的例子来理解下贝叶斯定理：假设一个常规的检测结果的敏感度与可靠度均为99%，也就是说，当被检者吸毒时，每次检测呈阳性（+）的概率为99%。而被检者不吸毒时，每次检测呈阴性（-）的概率为99%。假设该群体有0.5%的人确实吸毒了，如果从这些个体中随机抽出一个人检测为阳性，那他真的吸毒的概率是多少呢？

$$
\begin{align*}
    P(\text{User}|+) &= \dfrac{P(+|\text{User})P(\text{User})}{P(+|\text{User})P(\text{User})+P(+|\text{Non-user})P(\text{Non-user})} \\
    &= \dfrac{0.99\times 0.005}{0.99\times 0.005 + 0.01 \times 0.995} \\
    &\approx 33.2\%
\end{align*}
$$

结果还是不太符合人的直观感受的，吸毒测试看似已经很准确了，在检测出为阳性后这个人却只有33%的概率是真的吸毒了。原因就在于非吸毒者群体数量太大了，所以即使以很小的概率检测为伪阳性，人数还是相对真正吸毒的人多，所以从整体检测结果为阳性的人来说，真正吸毒的人占比就少了。贝叶斯公式很好的解释了该现象。

### 朴素贝叶斯分类器
现在我们考虑的是分类问题，设样本的特征向量 $\mathbf{x}=(x_1, x_2, \ldots, x_D)$，要将其分到类 $C_k$ 中，现重写贝叶斯公式如下：

$$
\begin{align*}
P(C_k|\mathbf{x}) &=\dfrac{P(\mathbf{x}|C_k)P(C_k)}{P(\mathbf{x})}\\
&\propto P(\mathbf{x}|C_k)P(C_k)
\end{align*}
$$

其中，

* $P(C_{k} \vert \mathbf{x})$ 为给定观测 $\mathbf{x}$ 后，类 $C_k$ 的后验概率（posterior probability）
* $P(C_k)$ 为类 $C_k$ 的先验概率（prior probability）
* $P(\mathbf{x}\vert C_{k})$ 为给定类的似然值（class likelihood）
* $P(\mathbf{x})$ 为证据（evidence）

为将误差最小化，贝叶斯分类器选择具有最大后验概率的类，即

$$
\text{选择 }C_i \text{ 如果 } P(C_i|\mathbf{x})=\underset{k}{\max }\,P({C_k}|\mathbf{x})
$$

现在知道怎么来分类了，就差计算了，但是似然值为联合概率密度函数，它可不好求，根据概率链式法则，它的计算过程如下：

$$
\begin{align*}
    P(\mathbf{x}|C_k) &=P(x_1,x_2,\ldots,x_D|C_k) \\
    &=P(x_1|x_2,\ldots,x_D,C_k)P(x_2|x_3,\ldots,x_D,C_k)\ldots P(x_{D-1}|x_D,C_k)P(x_D|C_k)
\end{align*}
$$

这时我们要上大招了，那就是**朴素贝叶斯假设**。假设 $\mathbf{x}$ 中各属性之间条件独立，即

$$
\begin{align*}
    P(x_1|x_2,\ldots,x_D,C_k)=P(x_1|C_k) \\
    P(x_2|x_3,\ldots,x_D,C_k)=P(x_2|C_k)
\end{align*}
$$

因此，似然值计算就简化为：

$$
    P(\mathbf{x}|C_k)\simeq P(x_1|C_k)P(x_2|,C_k)\ldots P(x_D|C_k)=\prod_{d=1}^{D}P(x_d|C_k)
$$

这样只需计算每个属性的条件概率就可以了。其实这是个很强的假设条件，现实中很难保证各变量之间能做到相互独立，也正是因为这个“要求”很高的条件，该方法前面被加上了朴素二字。

#### 朴素贝叶斯分类器举例

能通过手头计算对理解算法是很有帮助的，[这里](http://www.inf.ed.ac.uk/teaching/courses/inf2b/learnnotes/inf2b-learn06-notes-nup.pdf)有个不错的例子，但是它缺少2种情形，所以这里就不展开讨论它了，不过它还是值得一看的。我选取了《数据挖掘导论》里预测一个贷款人是否会拖欠还款的例子。假定训练集有如下属性：有房，婚姻状况和年收入。拖欠还款的贷款者属于类Y，还清贷款的属于类N。训练集如下表所示

![table](http://7xqutp.com1.z0.glb.clouddn.com/tableNY.png)

给定以测试记录 $\mathbf{x}$ = (有房=N，婚姻状况=已婚，年收入=120k)，预测他是否会拖欠贷款。<br>
改成频率表如下

![table1](http://7xqutp.com1.z0.glb.clouddn.com/tableNY2.png)

但年收入是连续变量，可以假设连续变量服从某种概率分布，然后利用训练数据估计分布的参数。高斯分布通常被用来表示连续属性的类条件概率分布。其实计算出来的是概率密度函数，我们应该计算相应区间的条件概率（很小区间的积分），不过该区间长度为常量，从结果看可以不去理会。因此得到年收入的条件概率分布为：

$$
\begin{align*}
    \text{如果类=N：} \quad & \text{样本均值}=100 \\
    & \text{样本方差}=2975 \\
    \text{如果类=Y：} \quad  & \text{样本均值}=90 \\
    & \text{样本方差}=25 \\
\end{align*}
$$

另外是否拖欠的先验概率为 $P(Y)=0.3$，$P(N)=0.7$。因为evidence都为 $P(\mathbf{x})$，不改变相对大小，因此可以忽略它，上公式计算后验概率得：

$$
\begin{align*}
    P(N|\mathbf{x})=P(\mathbf{x}|N)\times P(N) &= P(有房=N|N)\times P(婚姻状况=已婚|N)\times P(年收入=120k|N) \times P(N) \\
    &=4/7\times 4/7\times 0.0072 \times 7/10=0.0016
\end{align*}
$$

$$
\begin{align*}
    P(Y|\mathbf{x})=P(\mathbf{x}|Y)\times P(Y) &= P(有房=N|Y)\times P(婚姻状况=已婚|Y)\times P(年收入=120k|Y) \times P(Y) \\
    &=1\times 0\times 1.2\times10^{-9} \times 3/10=0
\end{align*}
$$

由于 $P(N|\mathbf{x})>P(Y|\mathbf{x})$，所以该样本应该被分到不拖欠类N。<br>
不过这里出现了一个潜在的问题，如果一个属性的类条件概率等于0，则整个类的后验概率就等于0，这在样本少的时候很容易发生。解决方法有拉普拉斯平滑和M估计等，可参看[这里1,](http://blog.csdn.net/cyningsun/article/details/8765536)[2](https://book.douban.com/subject/5377669/)。

#### 生成模型和判别模型

这里稍稍做做升华，与之前的知识联系联系。这篇[博客](http://www.cnblogs.com/jerrylead/archive/2011/03/05/1971903.html)关于这两种模型有很形象的解释，借鉴如下：比如说要确定一只羊是山羊还是绵羊，用判别模型的方法是先从历史数据中学习到模型，然后通过提取这只羊的特征来预测出这只羊是山羊的概率，是绵羊的概率。换一种思路，我们可以根据山羊的特征首先学习出一个山羊模型，然后根据绵羊的特征学习出一个绵羊模型。然后从这只羊中提取特征，放到山羊模型中看概率是多少，再放到绵羊模型中看概率是多少，哪个大就是哪个。形式化表示为求 $p(x\vert c)$（也包括 $p(c)$ )，$c$ 是模型结果，$x$ 是特征。之前提到的回归模型是判别模型，也就是根据特征值来求结果的概率。形式化表示为 $p(c\vert x;\theta)$ ，在参数 $\theta$ 确定的情况下，求解条件概率 $p(c\vert x)$ 。通俗的解释为在给定特征后预测结果出现的概率。利用贝叶斯公式可以发现两种模型的统一性：

$$
    P(c|x)=\dfrac{P(x|c)P(c)}{P(x)}
$$

由于我们关注的是 $c$ 的离散值结果中哪个概率大（比如山羊概率和绵羊概率哪个大），而并不是关心具体的概率，因此 $p(x)$ 可以忽略掉。由 $p(x\vert c)\times p(c)=p(x,c)$ 可知，因此有时称判别模型求的是条件概率，生成模型求的是联合概率。

### Reference

* [https://en.wikipedia.org/wiki/Bayes%27_theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem)
* [http://www.analyticsvidhya.com/blog/2015/09/naive-bayes-explained/](http://www.analyticsvidhya.com/blog/2015/09/naive-bayes-explained/)
* Pang-Ning Tan, M. Steinbach, Vipin Kumar著，范明，范宏建等译.数据挖掘导论[M].人民邮电出版社.
