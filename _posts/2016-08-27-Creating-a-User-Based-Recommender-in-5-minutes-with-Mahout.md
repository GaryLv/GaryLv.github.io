---
layout: post
title: Creating a User-Based Recommender in 5 minutes with Mahout
date: 2016-08-27
author: Run.D.Guan
header-img: img/post-bg-mah.jpg
category: Hadoop
tags:
  - Mahout
  - Recommender System
---

### What is Apache Mahout?

> The Apache Mahout™ project's goal is to build an environment for quickly creating scalable performant machine learning applications.

### Prerequisites

本文基本遵循`Mahout`官网上 RECOMMENDATIONS 下的 [Creating a User-Based Recommender in 5 minutes](http://mahout.apache.org/users/recommender/userbased-5-minutes.html)所写，并加入更多的注解以解释how to quickly build a Recommender System with Mahout。

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

下面是创建所需的数据集，`Mahout`的 Recommender 需要 users 和 items 作为输入，最简单的形式就是 *userID, itemID, value*，用来表示 user 对 item 的打分（如电影评分）。在本例中，简单创建如下形式的数据（完整数据见Reference链接），并命名为"dataset.csv"。

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

现在可以开始创建我们的 first recommender 啦。新建一个类命名为*SampleRecommender*，并添加main方法。首先我们要做的是从文件中加载数据。`Mahout`的 recommender 使用`DataModel`的接口来处理数据，代码如下（我的dataset.csv在root目录下）

```java
DataModel model = new FileDataModel(new File("/root/dataset.csv"));
```

这里我们要创建的是一个 user-based recommender，其思路是当我们想推荐物品给一特定的用户时，先看看和他有相同品味的用户，然后将他们喜欢的物品再推荐给他。为了找到相似的用户，我们需要描述他们之间的相关程度，有好几种可以采用的方法，这里我们采用很实用的[Pearson product-moment correlation coefficient](https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient)。在`Mahout`中，实现如下：

```java
UserSimilarity similarity = new PearsonCorrelationSimilarity(model);
```

接下来就要定义出哪些是相似的用户了，这里简单起见，把相似的大于0.1的都作为相似用户，该功能由`ThresholdUserNeighborhood`实现

```java
UserNeighborhood neighborhood = new ThresholdUserNeighborhood(0.1, similarity, model);
```

现在我们已经具备了构建最简单的推荐系统的要素了，在`Mahout`中可以通过如下方式快速构建recommender

```java
UserBasedRecommender recommender = new GenericUserBasedRecommender(model, neighborhood, similarity);
```

构建好recommender之后就可以进行推荐了，假如我们要给*userID* 2推荐3个items，就可以这样子做

```java
List<RecommendedItem> recommendations = recommender.recommend(2, 3);
for (RecommendedItem recommenndation : recommendations)
	System.out.println(recommenndation);
```

得到的输出结果为

    RecommendedItem[item:12, value:4.8328104]
    RecommendedItem[item:13, value:4.6656213]
    RecommendedItem[item:14, value:4.331242]

可以看到结果是按 value 排序的，value 越大，越是适用于推荐给该用户的物品。

是时候总结一下`Mahout`的推荐过程了。`Mahout`是由多个组件混搭而成的，而非单一的推荐引擎，其各个组件的组合可以定制，从而针对特定应用提供理想的推荐。通常包括如下的组件：

* 数据模型，由`DataModel`实现
* 用户间的相似性度量，由`UserSimilarity`实现
* 用户邻域的定义，由`UserNeighborhood`实现
* 推荐引擎，由一个`Recommender`实现（此处为`GenericUserBasedRecommender`）

要想推荐得更好更快，就必然需要经历一个漫长的试验和调优过程。

上面是分步解释的过程，为了有更主体的概况，把所有的代码贴在下面，尤其还要注意导包不要导错了。

```java
import java.io.File;
import java.io.IOException;
import java.util.List;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.ThresholdUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.UserBasedRecommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;

public class SampleRecommender {

	public static void main(String[] args) throws IOException, TasteException {
		DataModel model = new FileDataModel(new File("/root/dataset.csv"));
		UserSimilarity similarity = new PearsonCorrelationSimilarity(model);
		UserNeighborhood neighborhood = new ThresholdUserNeighborhood(0.1, similarity, model);
		UserBasedRecommender recommender = new GenericUserBasedRecommender(model, neighborhood, similarity);
		List<RecommendedItem> recommendations = recommender.recommend(2, 3);
		for (RecommendedItem recommenndation : recommendations)
			System.out.println(recommenndation);
	}
}
```

### Evaluation

构建出一个推荐系统之后就会想这个推荐系统是否能比较准确的给出期望的推荐。但不幸的是，要想知道推荐系统的优异只能在现实中做A/B test。

鉴于我们手头的数据，因为相当于有 label，因此我们可以做 **hold-out** test。把数据分成两份 -- 训练集和测试集。为了测试我们的 recommender，新建一个类 EvaluateRecommender，并包含 main 方法，为直观起见，所有代码如下：

```java
import java.io.File;
import java.io.IOException;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.eval.RecommenderBuilder;
import org.apache.mahout.cf.taste.eval.RecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.eval.AverageAbsoluteDifferenceRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;

public class EvaluateRecommender {
	public static void main(String[] args) throws IOException, TasteException {
		// TODO Auto-generated method stub
		DataModel model = new FileDataModel(new File("/root/dataset.csv"));
		RecommenderEvaluator evaluator = new AverageAbsoluteDifferenceRecommenderEvaluator();
		RecommenderBuilder builder = new RecommenderBuilder() {
			public Recommender buildRecommender(DataModel dataModel) throws TasteException {
				UserSimilarity similarity = new PearsonCorrelationSimilarity(dataModel);
				UserNeighborhood neighborhood = new NearestNUserNeighborhood(2, similarity, dataModel);
				return new GenericUserBasedRecommender(dataModel, neighborhood, similarity);
			}
		};
		double result = evaluator.evaluate(builder, null, model, 0.9, 1.0);
		System.out.println(result);
	}
}
```

其中在`RecommenderBuilder`接口上使用匿名内部类来构建我们的 user-based recommender。为了检测预测值与真实评分的差异，我们采用了`AverageAbsoluteDifferenceRecommenderEvaluator`，其得到的结果意味着估计值与实际值的偏差。`evaluate`方法中0.9代表训练集的百分比，后面的1.0代表用于构建推荐系统的数据量所占总数据量的百分比，当数据量很大又想快速评估的话，可以减小该值。

### Conclusion

至此我们已经构建出了一个简单的推荐系统，并能对它进行一定的评估。同时也熟悉了`Mahout`的一些基本概念。

### Reference

* [Creating a User-Based Recommender in 5 minutes](http://mahout.apache.org/users/recommender/userbased-5-minutes.html)
* Sean Owen, Robin Anil等著, 王斌, 韩冀中等译.Mahout 实战[M].人民邮电出版社.
