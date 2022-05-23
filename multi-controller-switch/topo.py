
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController
from time import sleep



class SingleSwitchTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1', protocols='OpenFlow13', failMode='secure')
        s2 = self.addSwitch('s2', protocols='OpenFlow13', failMode='secure')
        s3 = self.addSwitch('s3', protocols='OpenFlow13', failMode='secure')
        s4 = self.addSwitch('s4', protocols='OpenFlow13', failMode='secure')
 

        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="192.168.1.1/24")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="192.168.1.2/24")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="192.168.1.3/24")
        h4 = self.addHost('h4', mac="00:00:00:00:00:04", ip="192.168.1.4/24")
        
        
        self.addLink(s1,s2,1,3,bw=30)
        self.addLink(s2,s3,1,3,bw=30)
        self.addLink(s3,s4,1,3,bw=30)
        
        self.addLink(h1,s1,1,2)
        self.addLink(h2,s2,1,2)
        self.addLink(h3,s3,1,2)
        self.addLink(h4,s4,1,2)



if __name__ == '__main__':
    setLogLevel('info')
    topo = SingleSwitchTopo()
    c1 = RemoteController('c1', ip='127.0.0.1',port=6633)
    c2 = RemoteController('c2', ip='127.0.0.1',port=6634)
    net = Mininet(topo=topo, controller=[c1,c2])
    net.start()
    h1=net.get('h1')
    h2=net.get('h2')
    h3=net.get('h3')
    h4=net.get('h4')
  

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