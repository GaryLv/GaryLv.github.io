---
layout: post
title: ZooKeeper Deployment, Applications and Java API
date: 2017-04-26
author: Run.D.Guan
header-img: img/Zhan44.jpg
category: Big Data Structure
tags:
  - ZooKeeper
---


### ZooKeeper Introduction


> **Apache ZooKeeper** 是分布式系统的基础构件。在设计分布式系统时，总是需要开发和部署用来协调整个集群的架构，这就是ZooKeeper需求来源。ZooKeeper是Apache基金会下的开源项目，用于维护和协调分布式集群。它以简单接口提供了例如命名服务、配置管理、同步以及集群管理等常用服务，减轻了用户编程的压力。

![](https://www.codenotfound.com/assets/images/logos/apache-zookeeper-logo.jpg)

Zookeeper 提供设计和开发的协调服务有:
- **Naming Service** -- A name service is a service that maps a name to some information associated with that name. A telephone directory is a name service that maps the name of a person to his/her telephone number. In the same way, a DNS service is a name service that maps a domain name to an IP address. In your distributed system, you may want to keep a track of which servers or services are up and running and look up their status by name. ZooKeeper exposes a simple interface to do that. A name service can also be extended to a group membership service by means of which you can obtain information pertaining to the group associated with the entity whose name is being looked up.
- **Locking** -- In every distributed system, there will be some shared resources and multiple services may need to access this. So to allow serialized access to this resource, a locking mechanism is required. Zookeeper provides this functionality.
- **Synchronization** -- Hand in hand with distributed mutexes is the need for synchronizing access to shared resources. Whether implementing a producer-consumer queue or a barrier, ZooKeeper provides for a simple interface to implement that.
- **Configuration Management** -- You can use ZooKeeper to centrally store and manage the configuration of your distributed system. This means that any new nodes joining will pick up the up-to-date centralized configuration from ZooKeeper as soon as they join the system. This also allows you to centrally change the state of your distributed system by changing the centralized configuration through one of the ZooKeeper clients.
- **Leader Election** -- Your distributed system may have to deal with the problem of nodes going down, and you may want to implement an automatic fail-over strategy. ZooKeeper provides off-the-shelf support for doing so via leader election.

ZooKeeper 作为分布式系统的协调服务外本身还是个分布式应用。ZooKeeper遵循简单的 client-server 模型，其中客户是接受服务的节点（i.e., machines），而服务器是提供服务的节点。一系列ZooKeeper服务器构成了ZooKeeper ensemble。在任意给定的时间，每个ZooKeeper客户端都连接到一个ZooKeeper服务器上，每个ZooKeeper服务器在同一时间可以处理大量的客户端连接。每个客户端周期性地给跟它连接的服务器端发送pings来告知它是alive并connected。ZooKeeper服务器对此回应一个确认以表示服务器也是alive的。当在确定的时间内客户端没有收到服务器的确认信息，客户端便连接另外一个服务器了，显而易见地客户端会话转移到新的ZooKeeper服务器。

下图描述了ZooKeeper的 client-server 结构。
![ ](https://www.ibm.com/developerworks/library/bd-zookeeper/fig01.png)

ZooKeeper有由znodes组成的文件数据模型，可以把znodes想象成UNIX类系统的文件，只是它们可以有子节点。还可以把它们当做自带数据的目录，每个目录就叫做znodes。下图展示ZooKeeper的数据模型和分层命名空间
![](https://zookeeper.apache.org/doc/trunk/images/zknamespace.jpg)

znode的层次结构存储在ZooKeeper服务器中，这使得可扩展并快速响应客户端的读请求。每个znode的默认存储数据空间为1MB，因此即使ZooKeeper表现出类文件系统层级结构，但不能当作普通文件系统来用。相应地，它只能作为给分布式应用程序提供可靠性，可用性和协调性所需少量数据的存储机制。

当一个客户端请求读取特定znode的内容时，读操作只发生在客户端连接的服务器上。但当写操作想要成功完成的话，则需要ZooKeeper ensemble中严格意义上大多数节点都是可用的。当ZooKeeper服务器上线后，从ensemble中选取一个节点作为leader。当客户端提出写请求时，与之连接的服务器将该请求发送给leader，leader再把这个读请求发送给ensemble中所有的节点。当严格意义上的大多数节点（也称为quorum）成功响应了该读操作，则此次读操作成功执行。

构成一个高可用性和可靠性系统需要奇数台ZooKeeper服务器，这样才有实现当近一半 $((n-1)/2)$ 服务器挂掉之后，ZooKeeper服务还能正常运行。分布式系统中的节点可作为ZooKeeper ensemble的客户端，并且每个ZooKeeper服务器能处理大量的客户端节点。因此3,5,7是ZooKeeper ensemble常用的服务器节点个数。这里我们只部署3台ZooKeeper服务器。

### ZooKeeper 配置与部署

本文采用的集群配置环境见[上篇博文](http://garylv.github.io/linux%20basic/2017/04/23/Virtual-Machines-Cluster-Quick-Build-and-Automation-Deployment/)。因为ZooKeeper服务器是运行在JVM上的，所以需先安装JDK，我们的三台mini版服务器已经配置好了。首先在[官网](http://www.apache.org/dyn/closer.cgi/zookeeper/)上下载ZooKeeper3.4.9，解压到`/root/apps`目录下

    tar -zxvf zookeeper-3.4.9.tar.gz -C /root/apps/

进入ZooKeeper配置目录，将`zoo_sample.cfg`修改为`zoo.cfg`
![cfg](http://7xqutp.com1.z0.glb.clouddn.com/cfg.png)

配置文件，注意dataDir项，需要指定改路径用来存储与ZooKeeper服务器相关的声明。
![vicfg](http://7xqutp.com1.z0.glb.clouddn.com/vicfg.png)
并在该配置文件最下方添加如下服务器信息。

    server.1=mini1:2888:3888
    server.2=mini2:2888:3888
    server.3=mini3:2888:3888

保存后退出即可。需要说明的是，在该配置文件中，tickTime为心跳时间2s，初始同步时限为10个心跳时间，发送请求和接受响应为5个心跳时间。端口号2181是ZooKeeper客户端用来连接ZooKeeper服务器的，端口号2888用来ZooKeeper服务器之间通讯的，端口号3888用来leader选举的。这三个端口需要始终开放，因此这里我们把防火墙关掉。

在dataDir目录下创建`myid`文件，写入编号1,。同理在mini2虚拟机上写入2，mini3中写入3。

![zk1](http://7xqutp.com1.z0.glb.clouddn.com/zk1.png)

这样一台ZooKeeper服务器就配置好了，下面通过`scp`命令将ZooKeeper传到mini2和mini3上

![zk2](http://7xqutp.com1.z0.glb.clouddn.com/zk2.png)

然后进行同样的配置操作，下面便可以启动ZooKeeper服务器了。

### ZooKeeper Command Line Interface

在三台虚拟机上分别启动ZooKeeper服务器

    bin/zkServer.sh start

查看mini1 ZooKeeper服务器状态
![status](http://7xqutp.com1.z0.glb.clouddn.com/status.PNG)

可见mini1上的ZooKeeper服务器是follower，但mini2上的ZooKeeper是leader，mini3上的也是follower。

可以在任意一台ZooKeeper服务器上启动一台客户端，这里直接在mini1上运行

    bin/zkCli.sh

当然也可以在启动时直接选择服务器，如`bin/zkCli.sh server mini2:2181`

首先我们来查看下CLI客户端的命令
```
[zk: localhost:2181(CONNECTED) 0] help
ZooKeeper -server host:port cmd args
	connect host:port
	get path [watch]
	ls path [watch]
	set path data [version]
	rmr path
	delquota [-n|-b] path
	quit
	printwatches on|off
	create [-s] [-e] path data acl
	stat path [watch]
	close
	ls2 path [watch]
	history
	listquota path
	setAcl path acl
	getAcl path
	sync path
	redo cmdno
	addauth scheme auth
	delete path [version]
	setquota -n|-b val path
```

下面我们依次进行重要操作的讲解，首先是创建节点并查看节点信息
```
[zk: localhost:2181(CONNECTED) 2] create /mynode helloworld
Created /mynode
[zk: localhost:2181(CONNECTED) 3] get /mynode
helloworld
cZxid = 0x200000002
ctime = Tue Apr 25 20:29:11 CST 2017
mZxid = 0x200000002
mtime = Tue Apr 25 20:29:11 CST 2017
pZxid = 0x200000002
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 10
numChildren = 0
```

从znode中获取数据时，客户端也会返回属于znode的元数据，这里面比较重要的有znode创建和上次修改的时间（ctime和mtime），每次修改后数据的版本（dataversion），数据长度（dataLength），以及znode的子节点数（numChildren）。

观察根节点下的节点，有我们刚才创建的节点mynode
```
[zk: localhost:2181(CONNECTED) 4] ls /
[mynode, zookeeper]    
```

创建子节点
```
[zk: localhost:2181(CONNECTED) 5] create /mynode/childnode "data"
Created /mynode/childnode
[zk: localhost:2181(CONNECTED) 6] ls /mynode
[childnode]
```

删除节点
```
[zk: localhost:2181(CONNECTED) 11] rmr /mynode
[zk: localhost:2181(CONNECTED) 12] ls /
[zookeeper]
```

创建另一个节点
```
[zk: localhost:2181(CONNECTED) 15] create /mysecondnode hello
Created /mysecondnode
```

mini1上设置监听数据
```
[zk: localhost:2181(CONNECTED) 16] get /mysecondnode 1
hello
```

mini2上客户端修改数据
```
[zk: localhost:2181(CONNECTED) 0] ls /
[mysecondnode, zookeeper]
[zk: localhost:2181(CONNECTED) 1] set /mysecondnode hello2
cZxid = 0x200000006
ctime = Tue Apr 25 21:13:30 CST 2017
mZxid = 0x200000008
mtime = Tue Apr 25 21:29:37 CST 2017
pZxid = 0x200000006
cversion = 0
dataVersion = 1
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 6
numChildren = 0
```

mini1上收到监听结果
```
[zk: localhost:2181(CONNECTED) 17]
WATCHER::

WatchedEvent state:SyncConnected type:NodeDataChanged path:/mysecondnode

```

mini1上设置监听节点
```
[zk: localhost:2181(CONNECTED) 18] ls /mysecondnode 1
[]
```

mini2上客户端修改节点
```
[zk: localhost:2181(CONNECTED) 2] create /mysecondnode/child 0000
Created /mysecondnode/child
```

mini1监听结果
```
[zk: localhost:2181(CONNECTED) 19]
WATCHER::

WatchedEvent state:SyncConnected type:NodeChildrenChanged path:/mysecondnode

```

ZooKeeper的主要监听数据和节点的工作都已实现。以上我们通过ZooKeeper CLI客户端与ZooKeeper服务器进行交互，下面我们通过Java API来实现基本操作以及服务器上下线动态感知。

### ZooKeeper in Java
#### ZooKeeper Java API

为方便进行各项功能测试，这里采用单元测试模式进行开发，每项功能都由一个函数完成，函数功能由注释说明。

```Java
import java.util.List;

import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooDefs.Ids;
import org.junit.Before;
import org.junit.Test;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.data.Stat;

public class SimpleZkClient {

	private static final String connectString = "mini1:2181";
	private static final int sessionTimeout = 2000;	// 2s
	ZooKeeper zkClient=null;


	@Before
	public void init() throws Exception {
		zkClient = new ZooKeeper(connectString, sessionTimeout, new Watcher() {

			@Override
			public void process(WatchedEvent event) {
				// 收到事件通知后的回调函数，事件处理模块
				System.out.println(event.getType() + "---" + event.getPath());
				try {
					// 相应事件后继续监听
					zkClient.getChildren("/", true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	// 创造数据节点
	@Test
	public void create() throws Exception {
		String node = zkClient.create("/eclipse3", "hello".getBytes(), Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
	}

	// 判断节点是否存在
	@Test
	public void isExist() throws Exception {
		Stat stat = zkClient.exists("/eclipse", false);
		System.out.println(stat == null? "not exist" : "exist");
	}

	// 获取子节点
	@Test
	public void getChildren() throws Exception {
		List<String> children = zkClient.getChildren("/", true);
		for (String child : children) {
			System.out.println(child);
		}
		// 保持程序始终处于监听状态
		Thread.sleep(Long.MAX_VALUE);
	}

	// 获取znode数据
	@Test
	public void getData() throws Exception {
		byte[] data = zkClient.getData("/eclipse", false, null);
		System.out.println(new String(data));
	}

	// 删除znode
	@Test
	public void deleteData() throws Exception {
		zkClient.delete("/eclipse", -1);
	}

	// 修改znode数据
	@Test
	public void updateData() throws Exception {
		zkClient.setData("/eclipse2", "data changed".getBytes(), -1);
		byte[] data = zkClient.getData("/eclipse2", false, null);
		System.out.println(new String(data));
	}
}
```

当运行获取子节点函数`getChildren()`，Console显示如下输出信息，此时会监听子节点变化情况

```
None---null
eclipse3
mysecondnode
eclipse2
zookeeper
eclipse
```

当从CLI客户端增加节点
```
[zk: localhost:2181(CONNECTED) 22] create /addnode 123
Created /addnode
```

Console显示出子节点变化情况
```
None---null
eclipse3
mysecondnode
eclipse2
zookeeper
eclipse
NodeChildrenChanged---/
```

#### 服务器上下线动态感知

服务器会有动态上下线的情况，客户端需要能实时监测到服务器上下线的变化。服务器启动时就到ZooKeeper上注册信息建立临时序列节点，临时节点的目的在于如果服务器下线节点要即使删除。客户端启动时就去getChildren，获取当前在线服务器列表并注册监听，当有服务节点上下线事件时便会有通知，之后需要在`process()`中重新获取列表并注册监听，因为注册监听只能执行一次。

首先编写服务器端程序，逻辑功能为
- 获取ZooKeeper连接
- 向ZooKeeper集群注册服务器信息
- 启动业务功能

服务器端代码为
```Java
import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooDefs.Ids;
import org.apache.zookeeper.ZooKeeper;

public class DistributedServer {
	private static final String connectString = "mini1:2181,mini2:2181";
	private static final int sessionTimeout = 2000;
	private static final String parentNode = "/servers";

	private ZooKeeper zk = null;

	public void getConnect() throws Exception {
		zk = new ZooKeeper(connectString, sessionTimeout, new Watcher() {

			@Override
			public void process(WatchedEvent event) {
				try {
					zk.getChildren("/", true);
				} catch (Exception e) {
					e.printStackTrace();
				}

			}
		});
	}

	// 向zk集群注册服务信息
	public void registerServer(String hostname) throws Exception {
		String zkServ = zk.create(parentNode + "/" + hostname, hostname.getBytes(), Ids.OPEN_ACL_UNSAFE	, CreateMode.EPHEMERAL_SEQUENTIAL); // 临时节点
		System.out.println(hostname + " is noline.." + zkServ);
	}


	// 业务功能
	public void handleBussiness(String hostname) throws InterruptedException {
		System.out.println(hostname + " start working... ");
		Thread.sleep(Long.MAX_VALUE);
	}

	public static void main(String[] args) throws Exception {
		// 获取zk连接
		DistributedServer server = new DistributedServer();
		server.getConnect();

		// 向zk集群注册服务器信息
		server.registerServer(args[0]);

		// 启动业务功能
		server.handleBussiness(args[0]);
	}
}
```
从Run As -- Run Configuration中Auguments中提供主函数的参数，即服务器名称mini1。类似再次启动一个服务器mini2，服务器启动成功入下图所示

![online](http://7xqutp.com1.z0.glb.clouddn.com/online.jpg)

编写客户端程序，客户端程序逻辑为
- 获取ZooKeeper连接
- 获取servers的子节点信息并监听，从中获取服务器信息列表
- 业务线程启动

客户端代码如下
```Java
import java.util.ArrayList;
import java.util.List;

import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;

public class DistributedClient {
	private static final String connectString = "mini1:2181,mini2:2181";
	private static final int sessionTimeout = 2000;
	private static final String parentNode = "/servers";

	private volatile List<String> serverList;
	private ZooKeeper zk = null;

	// 创建连接到zk的客户端
	public void getConnect() throws Exception {
		zk = new ZooKeeper(connectString, sessionTimeout, new Watcher() {

			@Override
			public void process(WatchedEvent event) {
				// 收到事件通知后的回调函数（应该是我们自己的事件处理逻辑）
				try {
					//重新更新服务器列表，并注册监听
					getServerList();
				} catch (Exception e) {
					e.printStackTrace();
				}

			}
		});
	}

	// 获取服务器信息列表
	public void getServerList() throws Exception, InterruptedException {
		// 获取服务器子节点信息，并对父节点进行监听
		List<String> children = zk.getChildren(parentNode, true);

		// 创建一个局部list来存服务器信息
		List<String> servers = new ArrayList<>();
		for (String child : children) {
			byte[] data = zk.getData(parentNode + "/" + child, false, null);
			servers.add(new String(data));
		}
		// 把servers赋值给成员变量serverList，以提供给各业务线程使用
		serverList = servers;

		// print server list
		System.out.println(serverList);
	}


	//业务功能
	public void handleBussiness() throws InterruptedException {
		System.out.println("client is working...");
		Thread.sleep(Long.MAX_VALUE);
	}

	public static void main(String[] args) throws Exception {
		// 获取zk连接
		DistributedClient client = new DistributedClient();
		client.getConnect();

		// 获取servers的子节点信息并监听，从中获取服务器信息列表
		client.getServerList();

		// 业务线程启动
		client.handleBussiness();
	}
}
```

客户端提取服务器信息
```
[mini1, mini2]
client is working...
```

再次运行服务端程序，mini3服务器上线后
```
[mini3, mini1, mini2]
```
kill掉mini2，等待连接超时时间后，client端提示

    [mini3, mini1]

由此实现了服务器上下线动态感知的功能。

### Reference
* [https://zookeeper.apache.org/doc/trunk/zookeeperOver.html](https://zookeeper.apache.org/doc/trunk/zookeeperOver.html)
* [https://www.ibm.com/developerworks/library/bd-zookeeper/](https://www.ibm.com/developerworks/library/bd-zookeeper/)
* [https://www.tutorialspoint.com/zookeeper/zookeeper_api.htm](https://www.tutorialspoint.com/zookeeper/zookeeper_api.htm)
* Others web resources
