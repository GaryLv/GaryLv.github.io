---
layout: post
title:  "Naive Bayes"
date:   2016-03-07
author: Run.D.Guan
header-img: "[](http://wallpapercave.com/wp/KKSGGBW.jpg)"
category: Machine-learning
tags:
    - Supervised-Learning
    - Classification
---

朴素贝叶斯是一种分类方法，他计算量小可以用于实时决策，同时适合多分类问题。算法的性质决定了他广泛应用于文本分类，垃圾过滤，情感分析以及推荐系统等。根据名称就知道他的数学背景是贝叶斯理论，我们肯定是先要弄明白贝叶斯理论了。贝叶斯这套东西很神奇啊，他会给人莫名的一种靠谱的感觉，就觉得这东西说的有道理。统计学上还有贝叶斯学派和概率学派之争，唉，贵圈真乱~[这里](http://mp.weixin.qq.com/s?__biz=MzAxMzU5MTQ5MA==&mid=207004374&idx=1&sn=91f6220fb70ba87ba267d6d0a1fd8855#rd)有小短文一篇，讲了下二者的区别。下面就开始介绍贝叶斯定理啦。

### 贝叶斯定理
