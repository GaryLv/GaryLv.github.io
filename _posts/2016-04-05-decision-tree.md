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

决策树是我认识中最符合人直观思维的机器学习算法了，当我们判断一个问题时，我们就会寻求一些criteria一步步来分析该问题，最终得出结论。比如对于要不要出去玩网球如此"纠结"的问题，我们可以考虑如下的决定因素：天气看起来怎么样、温度怎么样、湿度如何以及有没有风（这个例子中显然缺少一个关键因素--有没有写完作业啊，果然老外不太考虑这些）。那么思考的过程可以形成如下的一棵决策树

![tree](http://7xqutp.com1.z0.glb.clouddn.com/dt2.PNG)

很符合自然的思考过程吧，下面描述下该决策树：
 * 每个结点测试一个属性（如天气、温度啊）
 * 结点的每条分支都是从该属性选取的值（对于天气结点就是Sunny、Overcast和Rain了）
 * 每个叶子结点就是预测的输出 $C_i$ 
