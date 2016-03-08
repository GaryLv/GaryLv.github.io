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

朴素贝叶斯是一种分类方法，他计算量小可以用于实时决策，同时适合多分类问题。算法的性质决定了他广泛应用于文本分类，垃圾过滤，情感分析以及推荐系统等。根据名称就知道他的数学背景是贝叶斯理论，我们肯定是先要弄明白贝叶斯理论了。贝叶斯这套东西很神奇啊，他会给人莫名的一种靠谱的感觉，就觉得这东西说的有道理。统计学上还有贝叶斯学派和概率学派之争，唉，贵圈真乱~[这里](http://mp.weixin.qq.com/s?__biz=MzAxMzU5MTQ5MA==&mid=207004374&idx=1&sn=91f6220fb70ba87ba267d6d0a1fd8855#rd)有小短文一篇，讲了下二者的区别。下面就开始介绍贝叶斯定理啦。

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

* $$P(C_k|\mathbf{x})$$ 为给定观测 $\mathbf{x}$ 后，类的后验概率（posterior probability）
* $P(C_k)$ 为类 $C_k$ 的先验概率（prior probability）
* $$P(\mathbf{x}|C_k)$$ 为给定类的似然值（class likelihood）
* $P(\mathbf{x})$ 为证据（evidence）

为将误差最小化，贝叶斯分类器选择具有最大后验概率的类，即

$$
\text{选择 }C_i \text{ 如果 } P(C_i|\mathbf{x})=\underset{k}{\max }\,P({C_k}|\mathbf{x})
$$


### Reference

* [https://en.wikipedia.org/wiki/Bayes%27_theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem)
* [http://www.analyticsvidhya.com/blog/2015/09/naive-bayes-explained/](http://www.analyticsvidhya.com/blog/2015/09/naive-bayes-explained/)
