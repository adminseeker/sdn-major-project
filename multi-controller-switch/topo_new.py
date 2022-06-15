
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController
import time
import redis
import pickle

r=redis.Redis(host="127.0.0.1",port=6379)



class SingleSwitchTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1', protocols='OpenFlow13', failMode='secure')
        s2 = self.addSwitch('s2', protocols='OpenFlow13', failMode='secure')
        s3 = self.addSwitch('s3', protocols='OpenFlow13', failMode='secure')
        s4 = self.addSwitch('s4', protocols='OpenFlow13', failMode='secure')
        s5 = self.addSwitch('s5', protocols='OpenFlow13', failMode='secure')
        s6 = self.addSwitch('s6', protocols='OpenFlow13', failMode='secure')
        s7 = self.addSwitch('s7', protocols='OpenFlow13', failMode='secure')
        s8 = self.addSwitch('s8', protocols='OpenFlow13', failMode='secure')
        s9 = self.addSwitch('s9', protocols='OpenFlow13', failMode='secure')
        s10 = self.addSwitch('s10', protocols='OpenFlow13', failMode='secure')
        s11 = self.addSwitch('s11', protocols='OpenFlow13', failMode='secure')
        s12 = self.addSwitch('s12', protocols='OpenFlow13', failMode='secure')
        s13 = self.addSwitch('s13', protocols='OpenFlow13', failMode='secure')
        s14 = self.addSwitch('s14', protocols='OpenFlow13', failMode='secure')
        s15 = self.addSwitch('s15', protocols='OpenFlow13', failMode='secure')
      
        
 

        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="192.168.1.1/24")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="192.168.1.2/24")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="192.168.1.3/24")
        h4 = self.addHost('h4', mac="00:00:00:00:00:04", ip="192.168.1.4/24")
        h5 = self.addHost('h5', mac="00:00:00:00:00:05", ip="192.168.1.5/24")
        h6 = self.addHost('h6', mac="00:00:00:00:00:06", ip="192.168.1.6/24")
        h7 = self.addHost('h7', mac="00:00:00:00:00:07", ip="192.168.1.7/24")
        h8 = self.addHost('h8', mac="00:00:00:00:00:08", ip="192.168.1.8/24")
        h9 = self.addHost('h9', mac="00:00:00:00:00:09", ip="192.168.1.9/24")

        
        
        
        
        self.addLink(s12,s13,1,2,bw=30)
        self.addLink(s13,s14,1,2,bw=30)
        self.addLink(s14,s15,1,2,bw=30)
        self.addLink(s12,s1,2,1,bw=30)
        self.addLink(s12,s2,3,1,bw=30)
        self.addLink(s12,s3,4,1,bw=30)
        self.addLink(s13,s10,3,1,bw=30)
        self.addLink(s13,s11,4,1,bw=30)
        self.addLink(s10,s4,2,1,bw=30)
        self.addLink(s10,s5,3,1,bw=30)
        self.addLink(s11,s6,2,1,bw=30)
        self.addLink(s11,s7,3,1,bw=30)
        self.addLink(s15,s8,3,1,bw=30)
        self.addLink(s15,s9,4,1,bw=30)
  
        
        
        # self.addLink(s6,s7,2,1,bw=30)
        
        
        self.addLink(h1,s1,1,2)
        self.addLink(h2,s2,1,2)
        self.addLink(h3,s3,1,2)
        self.addLink(h4,s4,1,2)
        self.addLink(h5,s5,1,2)
        self.addLink(h6,s6,1,2)
        self.addLink(h7,s7,1,2)
        self.addLink(h8,s8,1,2)
        self.addLink(h9,s9,1,2)
        
       



if __name__ == '__main__':
    setLogLevel('info')
    topo = SingleSwitchTopo()
    c1 = RemoteController('c1', ip='127.0.0.1',port=6633)
    c2 = RemoteController('c2', ip='127.0.0.1',port=6634)
    c3 = RemoteController('c3', ip='127.0.0.1',port=6635)
    net = Mininet(topo=topo, controller=[c1,c2,c3])
    net.start()
    
    h1=net.get('h1')
    h2=net.get('h2')
    h3=net.get('h3')
    h4=net.get('h4')
    h5=net.get('h5')
    h6=net.get('h6')
    h7=net.get('h7')
    h8=net.get('h8')
    h9=net.get('h9')
    # h10=net.get('h10')
    # h11=net.get('h11')
    # h12=net.get('h12')
    # h4=net.get('h4')
    # time.sleep(5)
    

    #set start_time
    # r.set("start_time",pickle.dumps(time.time()))


    # h10.cmd('ping 192.168.1.1 &')
    # h11.cmd('ping 192.168.1.4 &')
    # h12.cmd('ping 192.168.1.7 &')

    #h5.cmd('ping 192.168.1.8 &')
    #h6.cmd('ping 192.168.1.9 &')
    
  

    # h1.cmd('arp -s 192.168.1.2 00:00:00:00:00:02')
    # h1.cmd('arp -s 192.168.1.3 00:00:00:00:00:03')
    # h1.cmd('arp -s 192.168.1.4 00:00:00:00:00:04')
    # h2.cmd('arp -s 192.168.1.3 00:00:00:00:00:03')
    # h2.cmd('arp -s 192.168.1.4 00:00:00:00:00:04')
    # h2.cmd('arp -s 192.168.1.1 00:00:00:00:00:01')
    # h3.cmd('arp -s 192.168.1.4 00:00:00:00:00:04')
    # h3.cmd('arp -s 192.168.1.1 00:00:00:00:00:01')
    # h3.cmd('arp -s 192.168.1.2 00:00:00:00:00:02')
    # h4.cmd('arp -s 192.168.1.1 00:00:00:00:00:01')
    # h4.cmd('arp -s 192.168.1.2 00:00:00:00:00:02')
    # h4.cmd('arp -s 192.168.1.3 00:00:00:00:00:03')
   
    #sleep(5)
    #print("Topology is up, lets ping")
    #net.pingAll()
    CLI(net)
    net.stop()