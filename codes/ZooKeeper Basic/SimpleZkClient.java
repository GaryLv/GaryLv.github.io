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
				// �յ��¼�֪ͨ��Ļص��������¼�����ģ��
				System.out.println(event.getType() + "---" + event.getPath());
				try {
					// ��Ӧ�¼����������
					zkClient.getChildren("/", true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	
	// �������ݽڵ�
	@Test
	public void create() throws Exception {
		String node = zkClient.create("/eclipse3", "hello".getBytes(), Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
	}
	
	// �жϽڵ��Ƿ����
	@Test
	public void isExist() throws Exception {
		Stat stat = zkClient.exists("/eclipse", false);
		System.out.println(stat == null? "not exist" : "exist");
	}
	
	// ��ȡ�ӽڵ�
	@Test
	public void getChildren() throws Exception {
		List<String> children = zkClient.getChildren("/", true);
		for (String child : children) {
			System.out.println(child);
		}
		// ���ֳ���ʼ�մ��ڼ���״̬
		Thread.sleep(Long.MAX_VALUE);
	}
	
	// ��ȡznode����
	@Test
	public void getData() throws Exception {
		byte[] data = zkClient.getData("/eclipse", false, null);
		System.out.println(new String(data));
	}
	
	// ɾ��znode
	@Test
	public void deleteData() throws Exception {
		zkClient.delete("/eclipse", -1);
	}
	
	// �޸�znode����
	@Test
	public void updateData() throws Exception {
		zkClient.setData("/eclipse2", "data changed".getBytes(), -1);
		byte[] data = zkClient.getData("/eclipse2", false, null);
		System.out.println(new String(data));
	}
	
	
	
	
	
	
	
	
	
	

}
