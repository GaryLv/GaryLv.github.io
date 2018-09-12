---
layout: post
title:  "Building A Simple Blockchain with Go"
subtitle:   ""
date:   2018-09-10
author: Run.D.Guan
header-img: "img/grass.jpg"
category: Blockchain
tags:
    - Blockchain
    - Go
---

前文介绍了点区块链的基础知识，话说"最好"的学习方法就是*learning by doing*，所以本节就用Go语言来构建个简单的图书馆区块链，内容参考自文末的博客。该区块链上将记录图书借阅情况，整理流程如下：
1. 添加一本书的信息
2. 将该书的借阅信息加入区块中
3. 将区块加到区块链中

这只是简单的示例，所有的信息将存储在内存中，服务起来之后就是初始状态。

![](https://blockchain-jp.com/wp-content/uploads/2018/04/94716618dd7b2339e0bc797c93396611-790x450.png)

### Blocks
前面介绍过区块记录着有价值的信息，如交易记录和系统相关的如时间戳、上一个区块的哈希值等。根据这个大体规则这里简单定义下区块的数据结构，内容`Data`就是书籍的借阅信息，`Pos`为区块号，`Timestamp`为创建的该区块的时间戳，`Hash`为该区块的哈希值，`PrevHash`为上一区块的哈希值。

```golang
type Block struct {
	Pos       int
	Timestamp string
	Hash      string
	PrevHash  string
	Data      BookCheckout
}

type BookCheckout struct {
	BookID       string `json:"book_id"`
	User         string `json:"user"`
	CheckoutDate string `json:"checkout_date"`
	IsGenesis    bool   `json:"is_genesis"`
}

type Book struct {
	ID          string `json:"id"`
	Title       string `json:"title"`
	Author      string `json:"author"`
	PublishDate string `json:"publish_date"`
	ISBN        string `json:"isbn"`
}
```

### Hashing and Generating Blocks
对整个区块计算哈希值，这里简单的将区块头部和内容以字符串形式拼接在一起，然后通过`SHA-256`方法来计算区块的哈希值。

```go
func (b *Block) generateHash() {
  // get string val of the Data
  bytes, _ := json.Marshal(b.Data)
  // concatenate the dataset
  data := string(b.Pos) + b.Timestamp + string(bytes) + b.PrevHash
  hash := sha256.New()
  hash.Write([]byte(data))
  b.Hash = hex.EncodeToString(hash.Sum(nil))
}
```

有了借阅信息，又能够计算区块的哈希值，这样就能创建新区块了，下面通过函数`CreateBlock`来创建个新区块

```golang
func CreateBlock(prevBlock *Block, checkoutItem BookCheckout) *Block {
  block := &Block{}
  block.Pos = prevBlock.Pos + 1
  block.Timestamp = time.Now().String()
  block.Data = checkoutItem
  block.PrevHash = prevBlock.Hash
  block.generateHash()

  return block
}
```

函数`CreateBlock`创建区块需要两个参数，一个是上一个区块的索引，另一个是要添加的借阅信息，这里为了简化就直接把数据都加入其中并为对其校验。






















### Reference
* [https://www.codementor.io/codehakase/building-a-simple-blockchain-with-go-k7crur06v](https://www.codementor.io/codehakase/building-a-simple-blockchain-with-go-k7crur06v)
* [https://blockchain-jp.com/tech/2011](https://blockchain-jp.com/tech/2011)
