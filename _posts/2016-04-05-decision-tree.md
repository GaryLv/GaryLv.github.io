---
layout: post
title: Decision Tree
subtitle: ''
date: 2016-04-05T00:00:00.000Z
author: Run.D.Guan
header-img: img/post-macha.jpg
category: Machine-learning
tags:
  - Supervised-Learning
  - Classification
---

### Preface
决策树是我认识中最符合人直观思维的机器学习算法了，当我们判断一个问题时，我们就会寻求一些criteria一步步来分析该问题，最终得出结论。比如对于要不要出去玩网球如此"纠结"的问题，我们可以考虑如下的决定因素：天气看起来怎么样、温度怎么样、湿度如何以及有没有风（这个例子中显然缺少一个关键因素--有没有写完作业啊，果然老外不太考虑这些）。那么思考的过程可以形成如下的一棵决策树

![tree](http://7xqutp.com1.z0.glb.clouddn.com/dt2.PNG)

很符合自然的思考过程吧，下面描述下该决策树：

 * 每个结点测试一个属性（如天气、温度啊）
 * 结点的每条分支都是从该属性选取的值（对于天气结点就是Sunny、Overcast和Rain了）
 * 每个叶子结点就是预测的输出 $C_i$

决策树学习的目的是为了产生一棵泛化能力强，即处理未见示例能力强的决策树，其基本流程遵循如下递归策略

>**输入：** 训练集 $D=\\{(x_1,y_1),(x_2,y_2),\dots, (x_m,y_m)\\}$ ，属性值 $A=\\{a_1,a_2,\dots,a_d\\}$  
设 $D_t$ 是与结点 $t$ 相关联的训练集   
>1.  **if** $D_t$ 中样本都属于同一类 $C_i$，  **then** 将 $t$ 标记为叶子结点；**return**  
>2.  **if** $A=\varnothing$， **then** 将 $t$ 标记为叶子结点；其类别标记为 $D_t$ 中样本数最多的类；**return**  
>3.  从 $A$ 选取一个最优属性测试条件，将样本划分为较小的子集。对测试条件的每个输出创建一个子结点，并根据测试结果将样本分布到子结点中。 **then** 对每个子节点递归调用该算法。

无论哪种决策树算法，流程基本都是上述的过程，关键就在于如何选取所谓的最优属性测试条件。决策树构建算法主要有**ID3**，**C4.5**和**CART**。

### 划分选择

决策树的学习过程，我们希望每次划分出的分支尽可能属于同一类别，即结点的“纯度”越来越高。考察下面以哪种属性作为分类条件更好呢？

![](http://7xqutp.com1.z0.glb.clouddn.com/attri.png?imageView/2/w/600/q/100)

#### 信息增益
信息熵（information entropy）是度量样本集合纯度最常用的一种指标，样本集合纯度越低（即系统越混乱），信息熵越高，反之则低。假定当前样本集合 $D$ 中第 $i$ 类样本所占的比例为 $p_i (i=1,2,\dots,n)$，则 $D$ 的信息熵定义为

$$
    H(D)=-\sum_{i=1}^{n}p_i\log_2p_i
$$

编码样本集合 $i$ 需要分配的最少二进制位数为 $-\log_2p_i$，所以 $H(D)$ 描述了从 $D$ 中随机选取样本编码的位数的期望。数假设只分为两类(+,-)，熵的$1/2$ 随+类概率 $P_+$ 变化如下图，

![](http://7xqutp.com1.z0.glb.clouddn.com/dt1.PNG?imageView/2/w/490/q/90)

基尼系数后面会介绍，而分类误差率为 $1-\max(p_+,1-p_+)$，而且它总不会大于0.5，因为如果本来猜想的概率低，那么反着猜就好啦。  
我们回到上面的选分类属性的问题上来，既然信息熵表示样本集合的纯度，那么当以某一属性分类后，样本集合的整体信息熵减小的越多，说明分类效果越好。因此定义信息增益（information gain）

$$
\text{Gain}(D,a)=H(D)-\sum_{v=1}^{V}\dfrac{\vert D^v\vert}{\vert D\vert}H(D^v)
$$

其中离散属性值 $a$ 有 $V$ 个可能的取值 $\\{a^1,a^2,\dots,a^V\\}$, 因此划分为 $V$ 个分支结点，计算每个结点 $D^v$ 的信息熵，并赋予权重 $\vert D^v\vert /\vert D\vert$，即样本数越多的分支结点的影响力越大。

于是，计算根结点的信息熵为

$$
    H(D)=-\sum_{i=1}^{n}p_i\log_2p_i=-\left(\frac{29}{64}\log_2 \frac{29}{64}+\frac{35}{64}\log_2\frac{35}{64}\right)=0.994
$$

计算信息熵代码如下

```python
    def entropy(class_probabilities):
        """given a list of class probabilities, compute the entropy"""
        return sum(-p * math.log(p, 2)
                   for p in class_probabilities if p) # ignore zero probabilities
```
以属性 $a_i$ 分类后得到的2个分支结点的信息熵为

$$
\begin{aligned}
        H(D^1)=-\left(\frac{21}{26}\log_2 \frac{21}{26}+\frac{5}{26}\log_2\frac{5}{26}\right)=0.706 \\
        H(D^2)=-\left(\frac{8}{38}\log_2 \frac{8}{38}+\frac{30}{38}\log_2\frac{30}{38}\right)=0.742
\end{aligned}
$$

计算属性 $a_i$ 的信息增益为

$$
\begin{aligned}
        \text{Gain}(D,a_1)&=H(D)-\sum_{v=1}^{2}\dfrac{\vert D^v\vert}{\vert D\vert}H(D^v) \\
        &=0.994-\left(\dfrac{26}{64}\times 0.706+ \dfrac{38}{64}\times 0.742 \right)\\
        &=0.267
\end{aligned}
$$

同理可知 $\text{Gain}(D,a_2)=0.122$，所以选取属性 $a_1$ 更合适。选取最大的信息增益属性作为划分依据，这就是著名的**ID3**决策树学习算法。

#### 增益率

信息增益准则存在一个问题，他偏向于取值数目较多的属性。一个极端的例子是如果属性是样本的编号，那他的分支数等于样本总数，且直接对应每个样本的分类标签，此时信息增益最大，但这样划分毫无意义。所以为了解决**ID3**算法的泛化能力不足的缺点，**C4.5**算法提出了使用增益率（gain ratio）作为最优划分指标，其定义为

$$
    \text{GainRatio}=(D,a)=\dfrac{\text{Gain}(D,a)}{\text{IV}(a)}
$$

其中

$$
    \text{IV}(a)=-\sum_{v=1}^{V}\dfrac{\vert D^v\vert}{\vert D\vert}\log_2\dfrac{\vert D^v\vert}{\vert D\vert}
$$

称为属性 $a$ 的固有值。属性 $a$ 的可能取值数目越多，则 $\text{IV}(a)$ 的值通常越大。需要注意的是，增益率准则对可取值数目较少的属性有所偏好，因此**C4.5**算法并不是直接选择增益率最大的候选划分属性，而是采用了一个启发式思想：先从候选划分属性中找出信息增益高于平均水平的属性，再选择增益率最高的。

#### 基尼指数
CART[^key]决策树使用基尼指数（Gini index）来选择划分属性，数据集 $D$ 的纯度可用基尼值来度量：

$$
    \text{Gini}(D)=\sum_{i=1}^{n}p_i(1-p_i)=1-\sum_{i=1}^{n}p_i^2
$$

直观来说，$\text{Gain}(D)$ 反映了从数据集 $D$ 中随机抽取两个样本不一致的概率。因此 $\text{Gain}(D)$ 越小，则数据集 $D$ 纯度越高。

数据集以属性 $a$ 分类后对应的基尼指数定义为

$$
    \text{Gini}(D,a)=\sum_{v=1}^{n}\dfrac{\vert D^v\vert}{\vert D\vert}\text{Gini}(D^v)
$$

于是，选取基尼指数最小的属性作为划分属性。

#### 剪枝处理
为避免决策树算法的过拟合，可以采用剪枝来应对。剪枝（pruning）基本策略分为预剪枝和后剪枝。
<dl>
  <dt>预剪枝</dt>
  <dd>在决策树生成过程中，对每个结点在划分前先进行估计，若当前结点的划分不能带来决策树泛化能力的提升，则停止划分并将当前结点标记为叶子结点。</dd><br>
  <dt>后剪枝</dt>
  <dd>先从训练集生成一棵完整的树，然后自底向上地对非叶子结点进行考察，若该结点对应的子树替换为叶子结点能带来泛化能力的提升，则将该子树替换为叶子结点。</dd>
</dl>
后剪枝技术倾向于产生更好的结果，后剪枝是根据完全增长的决策树做出的剪枝决策，先剪枝可能过早终止决策树的生长。然而对于后剪枝，当子树被剪掉以后，生长完全决策树额外的计算就被浪费掉了。

### 测试用例

#### scikit-learn实现decision tree classification

还是使用Iris数据集，通过如下代码即可构建出决策树来

```python
from sklearn.datasets import load_iris
from sklearn import tree

iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)
```

虽然这里 `DecisionTreeClassifier()` 用的默认参数，还是有两个参数(`criterion` 和 `max_depth`) 需要介绍一下。`criterion` 即为衡量分类质量的标准，默认为 `criterion='gini'`，还有 `'entropy'` 来表征信息增益。 `max_depth` 为决策树的最大层数，默认为None。经过训练之后，模型可以用来预测样本，二分类输出标签为[-1,1]，多分类输出标签为[0,...,K-1]

```python
>>> clf.predict(iris.data[:1,:])
array([0])
```

或者观察样本属于各类的概率，其值为训练样本在同一类叶子结点下的所占的百分比

```python
>>> clf.predict_proba(iris.data[:1, :])
array([[ 1.,  0.,  0.]])
```
我们可以用`export_graphviz`方法把树状图导出[Graphviz](http://www.graphviz.org/Download.php)格式文件

```python
with open("iris.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f,
                             feature_names=iris.feature_names,
                             class_names=iris.target_names,
                             filled=True, rounded=True,
                             special_characters=True)
```
将生成的 `iris.dot` 文件导入`Graphviz`（需安装）中，另存为`png`等图形格式即可，效果如下：
![iris](http://7xqutp.com1.z0.glb.clouddn.com/iris.png)

选取Iris中每两对特征作为学习对象，其分类边界如下，代码参考[这里](http://scikit-learn.org/stable/auto_examples/tree/plot_iris.html#example-tree-plot-iris-py)
![dt](http://7xqutp.com1.z0.glb.clouddn.com/dt.png)

[^key]: Classification and Regression Tree 的缩写，可用于分类和回归

### Reference
* Pang-Ning Tan, M. Steinbach, Vipin Kumar著, 范明, 范宏建等译.数据挖掘导论[M].人民邮电出版社.
* 周志华.机器学习[M].清华大学出版社.
* M. Mitchell著, 曾华军, 张银奎等译. 机器学习[M]. 机械工业出版社.
* [http://scikit-learn.org/stable/modules/tree.html](http://scikit-learn.org/stable/modules/tree.html)
