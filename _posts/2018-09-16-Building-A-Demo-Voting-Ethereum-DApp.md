---
layout: post
title:  "Building A Demo Voting Ethereum DApp"
subtitle:   ""
date:   2018-09-16
author: Run.D.Guan
header-img: "img/Arches.jpg"
category: Blockchain
tags:
    - Blockchain
    - DApp
---

### 引言
今天我们来体验一下在以太坊上构建一个投票DApp，
// todo the final dapp display
那这个DApp有什么不同之处呢，这里从区块链的基础特点和以太坊的特点两个角度简单阐述一下。

#### 区块链技术的所能解决的问题
如果只是传统地新建在web上的投票系统，它将面临下面的问题
- 数据库的数据会被更改，数据可能被计数多次或是直接被删掉
- 在web服务器上的代码可以随时被更改

但对于一个投票系统，我们希望它数据不可被篡改，且每个人只能投票一次。如果我们将应用部署到区块链上会有什么不同呢？区块链本身就是网络与数据库的集合体，数据和代码在整个网络共享，所有的交易信息将成为公共账本，网络中的所有节点将保证数据没有被篡改。

#### 以太坊的特色技术
以太坊是一个有智能合约功能的公共区块链平台。如果拿智能手机打个比方，以太坊就是手机里的操作系统，智能合约就是上面搭载的应用。有了以太坊，开发者就可以直接开发自己的区块链应用而不太需要关心区块链的底层系统。以太坊作为一个**可编程区块链**的核心是以太坊虚拟机（EVM）。每个以太坊节点都运行着EVM，EVM是一个图灵完备的虚拟机，这意味着通过它可以实现各种复杂的逻辑。用户在以太坊网络中发布或者调用的智能合约就是运行在EVM上的。

### 冒烟测试
#### 依赖安装
为了构建dApp，需要先安装些依赖
##### NPM
首先要安装的依赖就是NPM，可以通过Node.js来安装
##### Truffle Framework
Truffle Framework可以帮助我们在以太坊上构建去中心化应用。它提供给我们一套用Solidity开发智能合约的工具，并能进行测试和部署。安装命令如下

    $ npm install -g truffle

如果因为网络问题安装失败可以试试使用淘宝的镜像

    $ npm install -g cnpm --registry=https://registry.npm.taobao.org
    $ cnpm install -g truffle

##### Ganache
Ganache可以快速建立个人以太坊区块链，在上面我们可以跑测试用例，执行命令并检查状态，同时控制区块链的操作方式。
![](http://7xqutp.com1.z0.glb.clouddn.com/ganache.png)
Ganache初始会给我们10个以太坊账户，每个账户里有100个虚拟的以太币，不禁让人感叹要是真有这么多该多好。
##### Metamask
Metamask是个Chrome插件，它可以帮助我们连接到本地以太坊上并与智能合约交互。如果网络不好用可以去github上下载它的release包并解压，通过Chrome扩展程序中的“加载已解压的扩展程序”来安装。
##### Syntax Highlighting
当前大多数的IDE并为支持Solidity，所有我们要安装个语法高亮插件，这里我给idea装了IntelliJ-Solidity插件用于支持Solidity语法。
#### 项目构建
这里我们通过`Truffle box`快速构建项目，并采用`Pet Shop box`，安装命令如下

    $ truffle unbox pet-shop

这样我们可以得到如下结构的工程
![](http://7xqutp.com1.z0.glb.clouddn.com/fs.png)

简单介绍下各目录的用途
- **contracts**：放置开发者编写智能合约文件的地方，这里已经有个默认的Migration合约（Election.sol是我后加的，包括migrations目录下的2_deploy_contracts.js）来处理部署
- **migrations**：用来存放部署脚本
- **src**：开发客户端应用
- **test**：存放测试文件
- **truffle.js**：Truffle默认的配置文件
下面就可以写智能合约了，这里只是为了测试我们的工程是否正常，这里我们只构造一个参选人，在contracts目录下新建Election.sol

```solidity
pragma solidity ^0.4.24;

contract Election {
    string public candidate;

    function Election () public {
        candidate = "Candidate 1";
    }
}
```

接下来就要写部署脚本，脚本命令要按顺序来，这样Truffle知道该以怎样的顺序来执行它们。在migrations目录下创建2_deploy_contracts.js

```javascript
var Election = artifacts.require("./Election.sol");

module.exports = function(deployer) {
  deployer.deploy(Election);
};
```

这样我们就可以部署我们的智能合约了，需要注意的是下面的命令不能在windows cmd中执行，我是在git bash中执行的

    $ truffle migrate

部署成功结果如下，只是里面有个过时写法的提醒，此时我们已经将智能合约部署到本地的以太坊区块链中了
![](http://7xqutp.com1.z0.glb.clouddn.com/migrate.png)

我们可以在控制台中跟智能合约交互，进入控制台的命令如下

    $ truffle console

我们来获取一个智能合约的实例，并来看看是否有我们定义的参选人，获取实例命令如下：

    Election.deployed().then(function(instance) { app = instance })

验证结果如下，可以看到应用的地址和正确的参选人的名字，证明我们的工程能够正确执行

![](http://7xqutp.com1.z0.glb.clouddn.com/smoketest1.png)
