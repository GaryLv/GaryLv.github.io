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
今天我们来体验一下在以太坊上构建一个投票DApp，最后的效果如下，每个投票人有两个参选人可选择投票，投票之后每个参选人票数加1，每个投票人只能投票一次。
![](http://7xqutp.com1.z0.glb.clouddn.com/elec1.png)

那这个DApp有什么不同之处呢，这里从区块链的基础特点和以太坊的特点两个角度简单阐述一下。

#### 区块链技术的所能解决的问题
如果只是传统地新建在web上的投票系统，它将面临下面的问题
- 数据库的数据会被更改，数据可能被计数多次或是直接被删掉
- 在web服务器上的代码可以随时被更改

但对于一个投票系统，我们希望它数据不可被篡改，且每个人只能投票一次。如果我们将应用部署到区块链上会有什么不同呢？区块链本身就是网络与数据库的集合体，数据和代码在整个网络共享，所有的交易信息将成为公共账本，网络中的所有节点将保证数据没有被篡改。

#### 以太坊的特色技术
以太坊是一个有智能合约功能的公共区块链平台。如果拿智能手机打个比方，以太坊就是手机里的操作系统，智能合约就是上面搭载的应用。有了以太坊，开发者就可以直接开发自己的区块链应用而不太需要关心区块链的底层系统。以太坊作为一个**可编程区块链**的核心是以太坊虚拟机（EVM）。每个以太坊节点都运行着EVM，EVM是一个图灵完备的虚拟机，这意味着通过它可以实现各种复杂的逻辑。用户在以太坊网络中发布或者调用的智能合约就是运行在EVM上的。

### 冒烟测试
要构建一个dApp涉及到的依赖较多，为了保证dApp的功能首先要测试下工程在初始化构建时候的功能性，下面就要进行前期工程的测试了。
#### 依赖安装
为了构建dApp，需要先安装些涉及到的依赖
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

这样我们就可以部署我们的智能合约了，需要注意的是下面的命令不能在windows cmd中执行，这里是在git bash中执行的

    $ truffle migrate

部署成功结果如下，只是里面有个过时写法的提醒，此时我们已经将智能合约部署到本地的以太坊区块链中了
![](http://7xqutp.com1.z0.glb.clouddn.com/migrate.png)

我们可以在控制台中跟智能合约交互，进入控制台的命令如下

    $ truffle console

我们来获取一个智能合约的实例，并来看看是否有我们定义的参选人，获取实例命令如下：

    Election.deployed().then(function(instance) { app = instance })

验证结果如下，可以看到应用的地址和正确的参选人的名字，证明我们的工程能够正确执行

![](http://7xqutp.com1.z0.glb.clouddn.com/smoketest1.png)

### 参选人
接下来就真正进入到代码功能实现中来了，首先当然要给参选人建模，并把他组成一个数组。下面的代码中可以看到通过`Solidity Struct`来对参选人建模，并通过`mapping`来存储成数组，并定义一个记录参选人个数的变量candidatesCount（因为在Solidity中没办法确定mapping的变量个数，所以多出来个计数器）。

```solidity
contract Election {
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    mapping(uint => Candidate) public candidates;
    uint public candidatesCount;
}
```

接下来定义函数来向mapping中添加参选人

    function addCandidate (string _name) private {
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

这里我们仅仅只新建两个参选人，添加合约的构造函数如下

    function Election () public {
        addCandidate("Candidate 1");
        addCandidate("Candidate 2");
    }

下面需要重新部署合约，因为这是部署在区块链上的，如果智能合约修改，重新部署，之前的所有记录都会消失，重新开始添加区块，所以在一个智能合约下，数据是不可变的。部署合约命令如下

    $ truffle migrate --reset

#### 测试
智能合约可是非常严肃的，上线之后要是出问题是很严重的，所以前期我们要做好自测工作。在test，目录下新建election.js，通过Mocha测试框架和Chai断言库来编写我们的测试用例。

```javascript
var Election = artifacts.require("./Election.sol");

contract("Election", function(accounts) {
  var electionInstance;

  it("initializes with two candidates", function() {
    return Election.deployed().then(function(instance) {
      return instance.candidatesCount();
    }).then(function(count) {
      assert.equal(count, 2);
    });
  });

  it("it initializes the candidates with the correct values", function() {
    return Election.deployed().then(function(instance) {
      electionInstance = instance;
      return electionInstance.candidates(1);
    }).then(function(candidate) {
      assert.equal(candidate[0], 1, "contains the correct id");
      assert.equal(candidate[1], "Candidate 1", "contains the correct name");
      assert.equal(candidate[2], 0, "contains the correct votes count");
      return electionInstance.candidates(2);
    }).then(function(candidate) {
      assert.equal(candidate[0], 2, "contains the correct id");
      assert.equal(candidate[1], "Candidate 2", "contains the correct name");
      assert.equal(candidate[2], 0, "contains the correct votes count");
    });
  });
});
```

首先获取到合约并赋值给一个变量，接下来我们调用`contract`函数，并将所有的测试用例写入回调函数中。这个回调函数会提供账户变量"accounts"，它是由Ganache提供的代表在区块链上所有的账户。第一个测试用例校验参选人的个数为2，第二个测试用例校验每个参选人的信息是否正确。现在通过下面的命令来执行测试脚本

    $ truffle test

![](http://7xqutp.com1.z0.glb.clouddn.com/truffletest.png)

看到了两个测试用例都通过的提示。

#### 客户端应用
现在可以将客户端的前台界面写一下，这里只需将Truffle Pet Shop自动生成的index.html修改下成文章最开始展示那样，代码参看[这里](https://github.com/dappuniversity/election/blob/master/src/index.html)。接下来替换app.js中的代码

```javascript
App = {
  web3Provider: null,
  contracts: {},
  account: '0x0',

  init: function() {
    return App.initWeb3();
  },

  initWeb3: function() {
    if (typeof web3 !== 'undefined') {
      // If a web3 instance is already provided by Meta Mask.
      App.web3Provider = web3.currentProvider;
      web3 = new Web3(web3.currentProvider);
    } else {
      // Specify default instance if no web3 instance provided
      App.web3Provider = new Web3.providers.HttpProvider('http://localhost:7545');
      web3 = new Web3(App.web3Provider);
    }
    return App.initContract();
  },

  initContract: function() {
    $.getJSON("Election.json", function(election) {
      // Instantiate a new truffle contract from the artifact
      App.contracts.Election = TruffleContract(election);
      // Connect provider to interact with contract
      App.contracts.Election.setProvider(App.web3Provider);

      return App.render();
    });
  },

  render: function() {
    var electionInstance;
    var loader = $("#loader");
    var content = $("#content");

    loader.show();
    content.hide();

    // Load account data
    web3.eth.getCoinbase(function(err, account) {
      if (err === null) {
        App.account = account;
        $("#accountAddress").html("Your Account: " + account);
      }
    });

    // Load contract data
    App.contracts.Election.deployed().then(function(instance) {
      electionInstance = instance;
      return electionInstance.candidatesCount();
    }).then(function(candidatesCount) {
      var candidatesResults = $("#candidatesResults");
      candidatesResults.empty();

      for (var i = 1; i <= candidatesCount; i++) {
        electionInstance.candidates(i).then(function(candidate) {
          var id = candidate[0];
          var name = candidate[1];
          var voteCount = candidate[2];

          // Render candidate Result
          var candidateTemplate = "<tr><th>" + id + "</th><td>" + name + "</td><td>" + voteCount + "</td></tr>"
          candidatesResults.append(candidateTemplate);
        });
      }

      loader.hide();
      content.show();
    }).catch(function(error) {
      console.warn(error);
    });
  }
};

$(function() {
  $(window).load(function() {
    App.init();
  });
});
```

上面代码主要做了这么几件事：
1. 创建web3：web3.js是一个JavaScript库，通过RPC调用与本地节点通信，这里通过`initWeb3`函数来配置web3
2. 初始化合约
3. 渲染函数：渲染函数将智能合约中的数据展示在页面上

重新部署合约后要启动服务器，命令如下

    $ npm run dev

这会自动打开浏览器以显示客户端的样子，不过客户端会只显示Loading，这是因为我们还没有登录到区块链中。这里我们首先需要通过MetaMask连接本地RPC，端口号在truffle.js配置文件中。

![](http://7xqutp.com1.z0.glb.clouddn.com/customrpc.png)

同时还要将自己本地的账户关联起来，本地的账户就在Ganache中，选择一个账户，点击它后面的小钥匙标签获取它的私钥，将其导入MetaMask中

![](http://7xqutp.com1.z0.glb.clouddn.com/importacc.png)
![](http://7xqutp.com1.z0.glb.clouddn.com/accmeta.png)

此时我们可以看到已经关联到相应的账户，地址和账户里的eth也都对应。刷新页面发现已经能正常显示投票界面了。

![](http://7xqutp.com1.z0.glb.clouddn.com/elec2.png)

### 投票
最后我们加入投票人，这里每个账户只能投一票，智能合约将记录这一切。

    contract Election {
      // ...
      // Store accounts that have voted
      mapping(address => bool) public voters;

      // ...
      function vote (uint _candidateId) public {
          // require that they haven't voted before
          require(!voters[msg.sender]);
          // require a valid candidate
          require(_candidateId > 0 && _candidateId <= candidatesCount);
          // record that voter has voted
          voters[msg.sender] = true;
          // update candidate vote Count
          candidates[_candidateId].voteCount ++;
      }
    }

这里通过通过全局变量"msg.sender"获取账户，对未投票的标记为已投票并给它投票的参选人票数加1。

接下来完善下投票界面，加上投票人选择参选人的功能，并可提交，在index.html加入

```html
<form onSubmit="App.castVote()">
  <div class="form-group">
    <label for="candidatesSelect">Select Candidate</label>
    <select class="form-control" id="candidatesSelect">
    </select>
  </div>
  <button type="submit" class="btn btn-primary">Vote</button>
  <hr />
</form>
```

最后更新下app.js文件，首先查询表单中的参选人，当我们调用智能合约中的投票函数时，我们将参选人id传递过去，该调用过程是异步的。此时我们在一个账户下选择一个参选人进行投票，会出现交易消耗gas的提示，选择SUBMIT，我们的投票信息就记录在区块链上了。

![](http://7xqutp.com1.z0.glb.clouddn.com/confirmtx.png)

总体过程只是为了上手体验一下，好多细节都没有涉及到，同时对于该投票dApp还有好多功能可以完善，比如设定计时器，跟实际选举过程一样，投票是有时间限制的，同时还可以当计时时间到了之后宣布获胜者，对于投票人可以设定哪些人可以投票哪些人不具有投票权等等。总之通过这个demo感受了下基于以太坊的dApp开发风格，之后再补充下基础知识再来开发。

### Reference
* [The Ultimate Ethereum Dapp Tutorial ](http://www.dappuniversity.com/articles/the-ultimate-ethereum-dapp-tutorial)
* 闫莺，郑凯，郭众鑫. 以太坊技术详解与实战[M]. 机械工业出版社, 2018.
