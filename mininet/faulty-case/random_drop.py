#!/usr/bin/python
"""
This is a simple example to emulate a common network fault, random packet drops on some switch.
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
d1 = net.addDocker('d1', ip='10.0.0.251', dimage="ubuntu:trusty")
d2 = net.addDocker('d2', ip='10.0.0.252', dimage="ubuntu:trusty")
d3 = net.addDocker('d3', ip='10.0.0.253', dimage="ubuntu:trusty")
d4 = net.addDocker('d4', ip='10.0.0.254', dimage="ubuntu:trusty")
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')
info('*** Creating links\n')
net.addLink(d1, s1)
net.addLink(d3, s1)
# net.addLink(s1, s3, cls=TCLink, loss=30)
net.addLink(s1, s3)
s1.cmd("tc qdisc add dev s1-eth3 root netem loss 30%")
net.addLink(s2, s3)
net.addLink(s2, d2)
net.addLink(s2, d4)
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
net.ping([d1, d2])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
