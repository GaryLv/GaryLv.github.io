---
layout: post
title: Virtual Machines Cluster Quick Build and Automation Deployment
date: 2017-04-23
author: Run.D.Guan
header-img: img/post-bg-mah.jpg
category: Linux Basic
tags:
  - Cluster Deployment
---

本文如何简单快速部署虚拟机集群，网络配置以及在主服务器中通过`shell`脚本自动化部署从服务器中的软件。作为以后大数据开发的集群基础。

### CentOS 6.8虚拟机集群安装配置

我们的目标是建立一个主服务器，以Desktop版本安装，另外四台从服务器以mini版安装，具体来讲是先安装一台mini版，并通过它克隆出其他三台，以达到节约时间和磁盘空间的目的。

具体的虚拟机安装过程不再赘述，现假设已安装好CentOS Desktop版一台，和mini版一台。

#### 网络配置

这里我们采用虚拟机的NAT网络连接方式，直接点说该方式既可以使虚拟机之间相互通信又能很方便地使它们通过本地主机上网。NAT(Network Address Translation, 网络地址转换), 把在内部网络中使用的IP地址转换成外部网络中使用的IP地址，把不可路由的IP地址转化成可路由的IP地址，对外部网络隐蔽内部网。NAT通过将私有的VWnet网络地址转换成主机地址，当虚拟机发送请求要连接网络资源时就好像请求来自主机一样。NAT极大缓解了IP地址不足的问题。

![NAT](https://www.vmware.com/support/ws55/doc/img/nat_1.png)

在WMware中，虚拟机通过主机的IP地址来接入网络资源，主机上的虚拟网卡连接到虚拟交换机VMnet8上。

#### 配置局域网段与网关

在WMware菜单栏编辑中，点击虚拟网络编辑器，配置NAT网络连接如下图所示，这里我们选取192.168.200.0局域网段。

![vm](http://7xqutp.com1.z0.glb.clouddn.com/net1.png)

点击NAT设置，设置网关信息，该虚拟网关用于将虚拟机路由到外网。

#### 设置物理主机虚拟网络参数

在物理主机网络连接中设置VMware Network Adapter VMnet8虚拟网卡的属性

![net2](http://7xqutp.com1.z0.glb.clouddn.com/net2.png)

#### 设置虚拟机网络参数

进入到Desktop版CentOS中，采用编辑配置文件方式的非图形化方法配置静态网络参数

```
vi /etc/sysconfig/network-scripts/ifcfg-eth0
```

![net3](http://7xqutp.com1.z0.glb.clouddn.com/net3.png)

主要参数`IPADDR`、`NETMASK`、`GATEWAY`和`DNS`,其中网关关系到能否正常上外网，DNS用于域名解析否则会ping外网域名时会显示no such host。修改完成后将网络服务重启

```
[root@master ~]# service network restart
Shutting down interface eth0:                              [  OK  ]
Shutting down loopback interface:                          [  OK  ]
Bringing up loopback interface:                            [  OK  ]
Bringing up interface eth0:  Determining if ip address 192.168.200.100 is already in use for device eth0...
RTNETLINK answers: File exists                             [  OK  ]
```

测试网络配置是否成功

![net4](http://7xqutp.com1.z0.glb.clouddn.com/net4.png)

可见网络配置已经成功。之后mini版的可按同样步骤进行，只是`IPADDR`设置为192.168.200.101。为方便以后各台服务器互相通信，将各台服务器的IP地址与主机名对应起来

```
[root@master ~]# vi /etc/hosts

127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

192.168.200.100 master
192.168.200.101 mini1
192.168.200.102 mini2
192.168.200.103 mini3
```

这样就可以通过主机名代替冗杂的IP地址了，测试从Desktop版到mini版的通信状况

![net5](http://7xqutp.com1.z0.glb.clouddn.com/net5.png)

#### 虚拟机克隆

此时我们只有一台Desktop版和一台mini版，还需要另外三台mini版，所以可以通过虚拟机克隆的方法迅速得到另外三台mini版。在VMware中右键mini1虚拟机，点击管理下的克隆，按提示顺序进行。其中克隆方法要选择创建完整克隆。克隆好的虚拟机还需配置网络，尤其网卡等问题。

##### 克隆虚拟机网络配置

刚克隆完成的虚拟会出现没有eth0的问题，因此修改网络配置，删掉`UUID`和`HWADDR`，并修改好静态`IPADDR`

```
vi /etc/sysconfig/network-scripts/ifcfg-eth0
```

之后可以简单删除如下文件，重启后会自动生成所需的eth0信息。或是进入修改将eth1改成eth0，将原有的eth0删除

```
rm -rf 　/etc/udev/rules.d/70-persistent-net.rules
```

reboot便完成了虚拟机的克隆，重复操作步骤便可完成其他mini版虚拟机的克隆。

#### 自动化部署软件--以JDK为例

本小节介绍如何通过在主服务器上实现集群的软件自动化部署。这里以JDK为例，首先在主服务器上搭建httpd web服务器，将JDK上传上去，其他从服务器都可以通过该服务器将JDK下载到本机。然后主服务器设置与从服务器的ssh免密登陆，将自动化部署的shell脚本发送到各台服务器上，并执行安装配置脚本，实现自动化集群部署的一个demo。

首先安装httpd服务器

```
yum install httpd
```

开启httpd服务器

    service httpd start

将JDK复制到`/var/www/html/software`下，其中`software`子目录需要自己创建，这时我们登陆到服务器上

![httpd](http://7xqutp.com1.z0.glb.clouddn.com/httpd.png)

可以看到JDK已经挂载上去了，这样其他机器就可以通过`wget`命令下载JDK了。

配置免密登陆需要先在主服务器上生成公钥私钥对

    ssh-keygen -t rsa

这样便可将本机的公钥发送到对方机器(`ssh-copy-id`)以实现ssh免密登陆。现直接来看运行的脚本代码`boot.sh`

```shell
#!/bin/bash

SERVERS="mini1 mini2 mini3 mini4"
PASSWORD=123456
BASE_SERVER=master

auto_ssh_copy_id() {
    expect -c "set timeout -1;
        spawn ssh-copy-id $1;
        expect {
            *(yes/no)* {send -- yes\r;exp_continue;}
            *assword:* {send -- $2\r;exp_continue;}
            eof        {exit 0;}
        }";
}

ssh_copy_id_to_all() {
    for SERVER in $SERVERS
    do
        auto_ssh_copy_id $SERVER $PASSWORD
    done
}

ssh_copy_id_to_all


for SERVER in $SERVERS
do
    scp install_everyone.sh root@$SERVER:/root
    ssh root@$SERVER /root/install_everyone.sh
done
```

其中ssh_copy_id_to_all实现了遍历每个从服务器，并配置好ssh免密登陆。子函数auto_ssh_copy_id实现了将主服务器的公钥传给从服务器，并在expect中模拟系统提示人机交互，省去了手动输入密码等的麻烦。代码最后是通过scp命令将下载配置脚本`install_everyone.sh`发送到没台从服务器中，并ssh登陆运行该脚本。`install_everyone.sh`实现了下载JDK并解压同时配置环境变量的过程，代码如下

```shell
#!/bin/bash

BASE_SERVER=master
yum install -y wget
wget $BASE_SERVER/software/jdk-7u45-linux-x64.tar.gz
tar -zxvf jdk-7u45-linux-x64.tar.gz -C /usr/local
cat >> /etc/profile << EOF
export JAVA_HOME=/usr/local/jdk1.7.0_45
export PATH=\$PATH:\$JAVA_HOME/bin
EOF
source /etc/profile
```

需要注意的是由于从服务器安装的是mini版本，并未安装scp命令，它从属于openssh-clients.x86_64

    yum install -y openssh-clients.x86_64

同时还需安装expect语言

    yum install expect

同时也将expect依赖的tcl安装好了。

此时运行脚本的障碍已经铲除了，准备运行脚本，首先在主服务器上添加这两个脚本的运行权限

    chmod +x install_everyone.sh boot.sh

在当前目录运行

    ./boot.sh

便开始了自动化部署 :grinning:

在其中一台mini版的机器上测试JDK安装情况，在Terminal中输入java

![net6](http://7xqutp.com1.z0.glb.clouddn.com/net6.png)

看来JDK安装成功了，本节工作顺利结束~
