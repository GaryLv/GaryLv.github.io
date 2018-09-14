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

### Creating the Blockchain
创建`Block`的list来构建我们最核心的数据结构`Blockchain`，并写个函数来实现把区块加到区块链中

```go
// Blockchain is an ordered list of blocks
type Blockchain struct {
  blocks []*Block
}

// BlockChain is a global variable that'll return the mutated Blockchain struct
var BlockChain *Blockchain

// AddBlock adds a Block to a Blockchain
func (bc *Blockchain) AddBlock (data BookCheckout) {
  prevBlock := bc.blocks[len(bc.blocks)-1]
  block := CreateBlock(prevBlock, data)
  bc.blocks = append(bc.blocks, block)
}
```

区块链需要有头部区块作为起始点，即创世区块（Genesis Block），这里创建创世区块并将其作为区块链的头节点。

```go
func GenesisBlock() *Block {
  return CreateBlock(&Block{}, BookCheckout{IsGenesis: true})
}

func NewBlockchain() *Blockchain {
  return &Blockchain{[]*Block{GenesisBlock()}}
}
```

函数`NewBlockchain`将会在程序运行时调用，以此来创建一个新的区块链，只存于内存中。

### Validation
添加区块时需要校验下区块的内容有没有被修改，要是校验不过的话可是不能加入到区块链中的。当然这里只是简单的校验，比如要是里面连它的哈希值也被修改好了这里可是没办法搞了╮(╯▽╰)╭

```go
func validBlock(block, prevBlock *Block) bool {
  // Confirm the hashes
  if prevBlock.Hash != block.PrevHash {
    return false
  }
  // confirm the block's hash is valid
  if !block.validateHash(block.Hash) {
    return false
  }
  // Check the position to confirm its been incremented
  if prevBlock.Pos+1 != block.Pos {
    return false
  }
  return true
}

func (b *Block) validateHash(hash string) bool {
  b.generateHash()
  if b.Hash != hash {
    return false
  }
  return true
}
```

这样添加区块的函数就更新为这样了

```go
func (bc *Blockchain) AddBlock(data BookCheckout) {
	preBlock := bc.blocks[len(bc.blocks)-1]
	block := CreateBlock(preBlock, data)
	if validBlock(block, preBlock) {
		bc.blocks = append(bc.blocks, block)
	}
}
```

### Web Server
至此区块链的结构和基本功能已经构建完毕，下面来创建个web server来跟区块链通讯以测试其功能。在程序中的main函数创建个web server并注册跟区块链通讯的路由，这里用的是`Gorilla Mux`。

```go
func main() {
  r := mux.NewRouter()
  r.HandleFunc("/", getBlockchain).Methods("GET")
  r.HandleFunc("/", writeBlock).Methods("POST")
  r.HandleFunc("/new", newBook).Methods("POST")

  log.Println("Listening on port 3000")

  log.Fatal(http.ListenAndServe(":3000", r))
}
```

函数`getBlockchain`将区块链以JSON格式返回回来

```go
func getBlockchain(w http.ResponseWriter, r *http.Request) {
  jbytes, err := json.MarshalIndent(BlockChain.blocks, "", " ")
  if err != nil {
    w.WriteHeader(http.StatusInternalServerError)
    json.NewEncoder(w).Encode(err)
    return
  }
  // write JSON string
  io.WriteString(w, string(jbytes))
}
```

函数`writeBlock`通过传来的数据来添加一个区块

```go
func writeBlock(w http.ResponseWriter, r *http.Request) {
  var checkoutItem BookCheckout
  if err := json.NewDecoder(r.Body).Decode(&checkoutItem); err != nil {
    w.WriteHeader(http.StatusInternalServerError)
    log.Printf("could not write Block: %v", err)
    w.Write([]byte("could not write block"))
    return
  }
  // create block
  BlockChain.AddBlock(checkoutItem)
  resp, err := json.MarshalIndent(checkoutItem, "", " ")
  if err != nil {
    w.WriteHeader(http.StatusInternalServerError)
    log.Printf("could not marshal payload: %v", err)
    w.Write([]byte("could not write block"))
    return
  }
  w.WriteHeader(http.StatusOK)
  w.Write(resp)
}
```

函数`newBook`创建一个新的`Book`并生成它对应的ID，并应用到加入的区块时。

```go
func newBook(w http.ResponseWriter, r *http.Request) {
  var book Book
  if err := json.NewDecoder(r.Body).Decode(&book); err != nil {
    w.WriteHeader(http.StatusInternalServerError)
    log.Printf("could not create: %v", err)
    w.Write([]byte("could not create new Book"))
    return
  }

  h := md5.New()
  io.WriteString(h, book.ISBN+book.PublishDate)
  book.ID = fmt.Sprintf("%x", h.Sum(nil))

  // send back payload
  resp, err := json.MarshalIndent(book, "", " ")
  if err != nil {
    w.WriteHeader(http.StatusInternalServerError)
    log.Printf("could not marshal payload: %v", err)
    w.Write([]byte("could not save book data"))
    return
  }
  w.WriteHeader(http.StatusOK)
  w.Write(resp)
}
```

代码部分就完成了，来用Postman测试下功能首先查询下当前区块链的信息，此时只有创世区块

![](http://7xqutp.com1.z0.glb.clouddn.com/getbc.png)

下面添加本书，这样即可获得书的ID添加到借阅信息中，添加书的结果如下

![](http://7xqutp.com1.z0.glb.clouddn.com/newbook.png)

最后添加借阅信息到区块中并加入到区块链中

![](http://7xqutp.com1.z0.glb.clouddn.com/writeblock.png)

再查下这回区块链中的内容

![](http://7xqutp.com1.z0.glb.clouddn.com/getbc2.png)

发现我们的借阅信息已经加入到了区块链中了 :smiley: </br>
至此我们就实现了一个简单用于存错图书馆借阅信息的区块链，大致了解了下区块链数据结构的实现以及操作方法，以后慢慢往上加入新的内容。

### Reference
* [https://www.codementor.io/codehakase/building-a-simple-blockchain-with-go-k7crur06v](https://www.codementor.io/codehakase/building-a-simple-blockchain-with-go-k7crur06v)
* [https://blockchain-jp.com/tech/2011](https://blockchain-jp.com/tech/2011)
