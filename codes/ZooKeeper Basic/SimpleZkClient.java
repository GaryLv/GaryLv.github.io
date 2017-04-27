package io.github.garylv.zk;

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
