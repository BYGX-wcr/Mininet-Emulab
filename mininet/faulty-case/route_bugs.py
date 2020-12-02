#!/usr/bin/python
"""
This is a simple example to emulate a common network fault, random packet drops on some switch.
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.nodelib import LinuxBridge
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.config import Subnet
setLogLevel('info')

net = Containernet(controller=Controller)
info('*** Adding docker containers\n')
d1 = net.addDocker('d1', dimage="ubuntu:trusty_v2")
d2 = net.addDocker('d2', dimage="ubuntu:trusty_v2")
d3 = net.addDocker('d3', dimage="ubuntu:trusty_v2")
d4 = net.addDocker('d4', dimage="ubuntu:trusty_v2")
info('*** Adding switches\n')
s1 = net.addDocker('s1', dimage="ubuntu:trusty_v2")
s2 = net.addDocker('s2', dimage="ubuntu:trusty_v2")
b1 = net.addSwitch('b1', cls=LinuxBridge)
b2 = net.addSwitch('b2', cls=LinuxBridge)
info('*** Adding subnets\n')
snet1 = Subnet(ipStr="10.0.0.0", prefixLen=24)
snet2 = Subnet(ipStr="10.1.0.0", prefixLen=24)
snet3 = Subnet(ipStr="10.2.0.0", prefixLen=24)
info('*** Creating links\n')
net.addLink(s2, s1, ip1=snet3.allocateIPAddr(), ip2=snet3.allocateIPAddr())
net.addLink(s1, b1, ip1=snet1.allocateIPAddr())
net.addLink(d1, b1, ip1=snet1.allocateIPAddr())
net.addLink(d2, b1, ip1=snet1.allocateIPAddr())
net.addLink(b2, s2, ip2=snet2.allocateIPAddr())
net.addLink(b2, d3, ip2=snet2.allocateIPAddr())
net.addLink(b2, d4, ip2=snet2.allocateIPAddr())
info('*** Starting network\n')
net.start()
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
