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
setLogLevel('info')

net = Containernet(controller=Controller)
info('*** Adding docker containers\n')
d1 = net.addDocker('d1', ip='10.0.0.1', dimage="ubuntu:trusty_v2")
d2 = net.addDocker('d2', ip='10.0.0.2', dimage="ubuntu:trusty_v2")
d3 = net.addDocker('d3', ip='11.0.0.1', dimage="ubuntu:trusty_v2")
d4 = net.addDocker('d4', ip='11.0.0.2', dimage="ubuntu:trusty_v2")
info('*** Adding switches\n')
s1 = net.addDocker('s1', ip='12.0.0.1', dimage="ubuntu:trusty_v2")
s1.cmd("sysctl net.ipv4.ip_forward=1")
s2 = net.addDocker('s2', ip='12.0.0.2', dimage="ubuntu:trusty_v2")
s2.cmd("sysctl net.ipv4.ip_forward=1")
b1 = net.addSwitch('b1', cls=LinuxBridge)
b2 = net.addSwitch('b2', cls=LinuxBridge)
info('*** Creating links\n')
net.addLink(s2, s1)
net.addLink(s1, b1)
net.addLink(d1, b1)
net.addLink(b1, d2)
net.addLink(b2, s2)
net.addLink(b2, d3)
net.addLink(b2, d4)
info('*** Starting network\n')
net.start()
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()
