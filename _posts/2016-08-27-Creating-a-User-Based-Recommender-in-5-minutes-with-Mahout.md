---
layout: post
title: Creating a User-Based Recommender in 5 minutes with Mahout
date: 2016-08-27
author: Run.D.Guan
header-img: img/post-bg-os-metro.jpg
category: Hadoop
tags:
  - Mahout
  - Recommender System
---

### What is Apache Mahout?

> The Apache Mahout™ project's goal is to build an environment for quickly creating scalable performant machine learning applications.

### Prerequisites

本文基本遵循`Mahout`官网上RECOMMENDATIONS下的Creating a User-Based Recommender in 5 minutes所写，并加入更多的注解以解释how to quickly build a Recommender System with Mahout。

配置好`Mahout`之后（我安装的版本为0.10.1），首先在`eclipse`中创建`maven project`，并在`pom.xml`中导入依赖如下

```xml
<dependencies>
	<dependency>
		<groupId> org.apache.mahout </groupId>
		<artifactId> mahout-mr </artifactId>
		<version> 0.10.0 </version>
	</dependency>
</dependencies>
```

下面是创建所需的数据集，`Mahout`的Recommender需要users和items作为输入，最简单的形式就是*userID, itemID, value*，用来表示user对item的打分（如电影评分）。在本例中，简单创建如下形式的数据（完整数据见Reference连接），并命名为"dataset.csv"。

    1,10,1.0
    1,11,2.0
    1,12,5.0
    1,13,5.0
    1,14,5.0
    1,15,4.0
    1,16,5.0
    1,17,1.0
    1,18,5.0
    2,10,1.0
    2,11,2.0
    2,15,5.0
    2,16,4.5
    2,17,1.0
    2,18,5.0
    3,11,2.5
    3,12,4.5
    3,13,4.0
    3,14,3.0
    3,15,3.5

### Creating a user-based recommender

现在可以开始创建我们的first recommender啦。新建一个类命名为*SampleRecommender*，并添加main方法。首先我们要做的是从文件中加载数据。`Mahout`的recommender使用`DataModel`的接口来处理数据，代码如下（我的dataset.csv在root目录下）

```java
DataModel model = new FileDataModel(new File("/root/dataset.csv"));
```

这里我们要创建的是一个user-based recommender，其思路是当我们想推荐物品给一特定的用户时，先看看和他有相同品味的用户，然后将他们喜欢的物品再推荐给他。为了找到相似的用户，我们需要描述他们之间的相关程度，有好几种可以采用的方法，这里我们采用很流行的Pearson product-moment correlation coefficient。在`Mahout`中，实现如下：

```java
UserSimilarity similarity = new PearsonCorrelationSimilarity(model);
```
