---
layout: post
title:  "Why is Bitcoin"
subtitle:   ""
date:   2018-08-18
author: Run.D.Guan
header-img: "img/bc-wallpaper.jpg"
category: Blockchain
tags:
    - Blockchain
    - Bitcoin
---
> Sorry to be a wet blanket. But, writing a description of Bitcoin for general audiences is bloody hard. There's nothing to relate it to. &emsp;&emsp;- Satoshi Nakamoto, July 5, 2010

### 探寻起源
比特币逐渐被世人接受必然有它的价值所在，它诞生的背景决定了它要解决当前金融体系哪些弊端，首先来看看当时甚至现在依旧存在的问题
- **隐私问题** -- 数字世界的发展给人类带来了前所未有的便利，与此同时却带来了用户隐私很难保密，民主社会国家的民众对此表示担忧，尤其对于极客们更是对此深恶痛绝。
- **货币超发** -- 政府总是有超发货币的倾向来扩大投资以保证经济增速保持在预期水平，还可以充实自己，但会导致民众的财富缩水。直接导火索是2008年美国金融危机，美国政府开始给自己印钞票，民众的钱缩水，物价上涨。比特币的创始人（或组织）中本聪看不下去了，后来发明出比特币。
- **中心化的被攻击风险** -- 当前金融系统基本都是中心化的模式，中心化有中心化明显优势，如信用背书，但记账圈是在他们手里，账本是集中管理的，当它遭遇黑客攻陷后损失是毁灭的。

基于以上以及其他现实存在的问题，中本聪于2008年发表论文[《比特币：一种点对点的电子现金系统》](https://bitcoin.org/bitcoin.pdf)，文中介绍了一种通过点对点的方式在线从一端转移到另一端而不经过任何金融机构的电子现金，宣告了比特币的诞生，其中用到的核心创新技术就是区块链。下面来看看比特币的运行流程，再来分析一下它解决了之前数字货币解决不了的问题，最后总结下比特币的价值。

### 比特币运行流程
比特币用户在电脑上运行比特币客户端软件，这样的电脑称为一个节点（node）。大量节点电脑互相连接，形成一张像蜘蛛网一样的P2P（点对点）网络。

![](http://bitcoinromania.ro/wp-content/uploads/2016/07/bitcoin-peer-to-peer.png)

当张三想要通过A账号转账1比特币给李四的B账号时，
1. 张三向周围节点广播转账交易要求：A账号转账1比特币给B账号，并用A账号的私钥签名。（A账号的私钥可简单理解为A账号的密码，只要知道A账号的私钥就能使用A账号上的比特币）
2. 张三周围的节点通过A账号的公钥检查交易签名的真伪，并且检查张三的A账号是否有足够余额。
3. 检查通过后，节点往自己的账本上写：A账号向B账号转账1比特币元，并修改余额：A账号余额=3比特币-1比特币=2比特币，B账号余额=2比特币+1比特币=3比特币。
4. 节点把这个交易广播给周围的节点，一传十十传百，直到所有节点都收到这笔交易。

![](http://blogs.thomsonreuters.com/answerson/wp-content/uploads/sites/3/2016/01/infographic-how-blockchain-works.jpg)

比特币的去中心化公开账本称为区块链。





### 比特币解决的技术问题
#### 分布式共识
#### 双花问题

### 比特币的价值

### Reference
* [What is Cryptocurrency: Everything You Need To Know](https://blockgeeks.com/guides/what-is-cryptocurrency/)
* [比特币创造的价值在哪](https://www.zhihu.com/question/21418402/answer/71274765)
* 《区块链技术驱动金融》
