#!/usr/bin/python
"""
This is a simple example to emulate a common network fault, random packet drops on some switch.
"""
from mininet.net import Containernet
import mininet.node
print(mininet.node.__file__)
from mininet.node import * #Controller, Docker, DockerRouter, DockerP4Router
from mininet.nodelib import LinuxBridge
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.config import Subnet
setLogLevel('info')

net = Containernet(controller=Controller)

info('*** Adding docker containers\n')

d1 = net.addDocker('d1', dimage="ubuntu:trusty_v1")
d2 = net.addDocker('d2', dimage="ubuntu:trusty_v1")
# d3 = net.addDocker('d3', dimage="ubuntu:trusty_v1")
# d4 = net.addDocker('d4', dimage="ubuntu:trusty_v1")

info('*** Adding switches\n')

s1 = net.addDocker('s1', cls=DockerP4Router, 
                         dimage="p4switch:v2",
                         json_path="/home/wcr/behavioral-model/mininet/simple_router.json", 
                         pcap_dump="/",
                         controller="~/nf-queue",
                         ospfd='yes')
# s2 = net.addDocker('s2', cls=DockerP4Router, 
#                          dimage="p4switch:v1", 
#                          json_path="/home/wcr/behavioral-model/mininet/simple_router.json", 
#                          pcap_dump="/",
#                          ospfd='yes')
# b1 = net.addSwitch('b1', cls=LinuxBridge)
# b2 = net.addSwitch('b2', cls=LinuxBridge)

info('*** Adding subnets\n')
snet1 = Subnet(ipStr="10.0.0.0", prefixLen=24)
snet2 = Subnet(ipStr="10.1.0.0", prefixLen=24)
snet3 = Subnet(ipStr="10.2.0.0", prefixLen=24)
snet4 = Subnet(ipStr="10.3.0.0", prefixLen=24)

info('*** Creating links\n')

# net.addLink(s2, s1, ip1=snet1.assignIpAddr("10.0.0.2"), ip2=snet1.assignIpAddr("10.0.0.1"))
net.addLink(s1, d1, ip1=snet2.assignIpAddr("10.1.0.1"), ip2=snet2.allocateIPAddr())
net.addLink(s1, d2, ip1=snet3.assignIpAddr("10.2.0.1"), ip2=snet3.allocateIPAddr())
# net.addLink(b2, s2, ip2=snet4.assignIpAddr("10.3.0.1"))
# net.addLink(b2, d3, ip2=snet4.allocateIPAddr())
# net.addLink(b2, d4, ip2=snet4.allocateIPAddr())

info('*** Configuring routes\n')
s1.addRoutingConfig("ospfd", "router ospf")
s1.addRoutingConfig("ospfd", "router-id 10.0.0.1")
s1.addRoutingConfig("ospfd", "network " + snet1.getNetworkPrefix() + " area 0")
s1.addRoutingConfig("ospfd", "network " + snet2.getNetworkPrefix() + " area 1")
s1.addRoutingConfig("ospfd", "network " + snet3.getNetworkPrefix() + " area 2")
s1.addRoutingConfig("ospfd", "log file tmp/quagga.log")
s1.start()

# s2.addRoutingConfig("ospfd", "router ospf")
# s2.addRoutingConfig("ospfd", "router-id 10.0.0.2")
# s2.addRoutingConfig("ospfd", "network " + snet1.getNetworkPrefix() + " area 0")
# s2.addRoutingConfig("ospfd", "network " + snet4.getNetworkPrefix() + " area 1")
# s2.addRoutingConfig("ospfd", "log file tmp/quagga.log")
# s2.start()

d1.setDefaultRoute("gw 10.1.0.1")
d2.setDefaultRoute("gw 10.2.0.1")
# d3.setDefaultRoute("gw 10.3.0.1")
# d4.setDefaultRoute("gw 10.3.0.1")

info('*** Starting network\n')

net.start()

info('*** Running CLI\n')

CLI(net)

info('*** Stopping network')

net.stop()
