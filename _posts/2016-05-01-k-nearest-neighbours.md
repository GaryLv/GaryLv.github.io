---
layout: post
title: k-Nearest Neighbors
date: 2016-05-01
author: Run.D.Guan
header-img: img/post-bg-os-metro.jpg
category: Machine-learning
tags:
  - Classification
---

### 简介
k-近邻算法思路简单清晰，同时拥有不错的分类效果，处理大规模的数据分类，尤其适用于样本分类边界不规则的情况，对异常值不敏感，无需数据输入假定等优点，被列入[十大数据挖掘算法](http://www.cs.uvm.edu/~icdm/algorithms/10Algorithms-08.pdf)之一。

kNN思路如下，拿到一组数据，计算它跟样本集中每组数据的相似性，找出前k组最相似的数据，看这k组数据中哪个类别出现的最多，哪个就是新数据的分类。相似性就可以用各种距离来定义，这里我们采用欧氏距离。怎么样，是不爆简单，下面盗个图来说明kNN算算法流程。
![](https://cambridgecoding.files.wordpress.com/2016/01/knn2.jpg)

### 实现
kNN算法步骤总结如下：

1. 计算当前点与已知类别数据集中的点的距离
2. 按距离递增的顺序排序，找出前k个点作为最近邻居集
3. 在最近邻居集合中选出出现频次最高的类别作为当前点的预测分类

根据上述步骤用python实现kNN算法如下：

#### 1. 计算欧式距离
```python
from sklearn.datasets import load_iris
from sklearn import cross_validation
import numpy as np

# 导入数据
iris = load_iris()
X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data, iris.target, test_size=0.4, random_state=1)

# 计算距离
def get_distance(test_instance, training_set):
    # test_instance is the data point we want to evaluate, and training_set is the original dataset
    dataSize = training_set.shape[0]    
    diffs_squared = (np.tile(test_instance, (dataSize, 1)) - training_set) ** 2
    return np.sqrt(np.sum(diffs_squared, axis=1))
```

#### 2. 根据距离排序结果找出最近的k个邻居
```python
def get_neighbours(test_instance, training_set, labels, k):
    # return first k nearest neighbor
    distances = get_distance(test_instance, training_set)
    sortedIndex = distances.argsort()
    sortedNeighours = labels[sortedIndex]
    return sortedNeighours[:k]
```

#### 3. 选出出现频次最高的类别作为预测分类
```python
from collections import Counter

def get_majority(neighbours):
    count = Counter(neighbours)
    return count.most_common()[0][0]
```

#### 4. 测试算法
```python
from sklearn.metrics import classification_report, accuracy_score

prediction = []
for i in range(len(X_test)):
    # print('Classifying test instance number ' + str(i) +':')
    neighbours = get_neighbours(X_test[i], X_train, y_train, 5)
    majority_vote = get_majority(neighbours)
    prediction.append(majority_vote)
    print('Predicted labe=' + str(majority_vote) + ', Acually label=' + str(y_test[i]))

print('\nThe overall accuracy of the model is: ' + str(accuracy_score(y_test, prediction)) + '\n')
report = classification_report(y_test, prediction, target_names = iris.target_names)
print('A detailed classification report:\n' + report)
```
结果如下

    The overall accuracy of the model is: 0.983333333333

  label | precision  | recall  | f1-score  |  support
--:|---:|---:|---:|--:
 setosa | 1.00  | 1.00  |  1.00 |  19
  versicolor| 0.95  | 1.00  |  0.98 |  21
  virginica| 1.00  | 0.95  |  0.97 |  20
  avg / total| 0.98  | 0.98  | 0.98  |  60

可以看出预测结果还不错，下面我们将结果分类结果可视化出来。为作图显示方便只选取`iris dataset`的前两个属性，代码在[这里](https://github.com/GaryLv/GaryLv.github.io/blob/master/codes/k-nearest%20neighbours/knn1.py)查看，其分类边界如下

![knn](http://7xqutp.com1.z0.glb.clouddn.com/knn.png)

### 总结
* kNN是一种lazy learning方法，它不去构建一个通用的模型，而是简单的把训练数据存储起来。因为没有假设函数形式，它也被称作非参数方法
* k的选取很多程度依赖于数据集，通常来讲更大的k可以抑制噪声，但会使得边界不是很明显
* 计算复杂度高，空间复杂度高

### Reference

* [https://blog.cambridgecoding.com/2016/01/16/machine-learning-under-the-hood-writing-your-own-k-nearest-neighbour-algorithm/](https://blog.cambridgecoding.com/2016/01/16/machine-learning-under-the-hood-writing-your-own-k-nearest-neighbour-algorithm/)
* [http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/](http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/)
* [http://scikit-learn.org/stable/modules/neighbors.html](http://scikit-learn.org/stable/modules/neighbors.html)
* P. Harrington著, 李锐, 李鹏等译. 机器学习实战[M]. 人们邮电出版社.
