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
from mininet.config import Subnet, NodeList
import os
setLogLevel('info')

net = Containernet(controller=Controller)
lengthOfRing = 3
nodes = NodeList()

info('*** Adding docker containers\n')

host_list = list()
for i in range(0, lengthOfRing * 2):
    new_host = net.addDocker('d{}'.format(i), dimage="ubuntu:trusty_v2")
    host_list.append(new_host)

admin_host = net.addDocker('admin', dimage="p4switch:v8")
host_list.append(admin_host)

info('*** Adding switches\n')

switch_list = list()
for i in range(0, lengthOfRing + 1):
    new_switch = net.addDocker('s{}'.format(i), cls=DockerP4Router, 
                         dimage="p4switch:v9",
                         json_path="/home/wcr/p4switch/ecmp_switch.json", 
                         pcap_dump="/tmp",
                         log_console=True,
                         log_level="info",
                         rt_mediator="/home/wcr/p4switch/rt_mediator.py",
                         ospfd='yes')
    switch_list.append(new_switch)
    new_switch.addRoutingConfig("ospfd", "router ospf")

info('*** Adding subnets\n')
snet_list = list()
for i in range(0, 100):
    new_snet = Subnet(ipStr="10.{}.0.0".format(i), prefixLen=24)
    snet_list.append(new_snet)

info('*** Creating links & Configure routes\n')

snet_counter = 0

# configure switch-switch links
for i in range(0, lengthOfRing):
    right = (i + 1) % lengthOfRing

    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    link = net.addLink(switch_list[i], switch_list[right], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_list[i], switch_list[right])

    # config routing, every router prefer the path in clockwise direction
    switch_list[i].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
    switch_list[right].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
    # switch_list[right].addRoutingConfig("ospfd", "interface {}".format(link.intf2))
    # switch_list[right].addRoutingConfig("ospfd", "ip ospf cost 100")
    # switch_list[right].addRoutingConfig("ospfd", "router ospf")

    nodes.addNode(switch_list[i].name, ip=ip1, nodeType="switch")
    nodes.addNode(switch_list[right].name, ip=ip2, nodeType="switch")
    nodes.addLink(switch_list[i].name, switch_list[right].name)

    snet_counter += 1

    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    link = net.addLink(switch_list[i], switch_list[lengthOfRing], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_list[i], switch_list[lengthOfRing])

    # config routing, every router prefer to neglect the paths via the central switch
    switch_list[i].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
    switch_list[lengthOfRing].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
    # switch_list[i].addRoutingConfig("ospfd", "interface {}".format(link.intf1))
    # switch_list[i].addRoutingConfig("ospfd", "ip ospf cost 200")
    # switch_list[i].addRoutingConfig("ospfd", "router ospf")
    # switch_list[lengthOfRing].addRoutingConfig("ospfd", "interface {}".format(link.intf2))
    # switch_list[lengthOfRing].addRoutingConfig("ospfd", "ip ospf cost 200")
    # switch_list[lengthOfRing].addRoutingConfig("ospfd", "router ospf")

    nodes.addNode(switch_list[lengthOfRing].name, ip=ip2, nodeType="switch")
    nodes.addLink(switch_list[i].name, switch_list[lengthOfRing].name)

    snet_counter += 1

# configure host-switch links
for i in range(0, lengthOfRing * 2):
    sid = int(i / 2)

    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    net.addLink(switch_list[sid], host_list[i], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_list[sid])
    switch_list[sid].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))

    host_list[i].setDefaultRoute("gw {}".format(ip1.split("/")[0]))

    nodes.addNode(host_list[i].name, ip=ip2, nodeType="host")
    nodes.addLink(switch_list[sid].name, host_list[i].name)

    snet_counter += 1

# configure the link between admin host
ip1 = snet_list[snet_counter].allocateIPAddr()
ip2 = snet_list[snet_counter].allocateIPAddr()
net.addLink(switch_list[lengthOfRing], admin_host, ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
snet_list[snet_counter].addNode(switch_list[lengthOfRing])
switch_list[lengthOfRing].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))

admin_host.setDefaultRoute("gw {}".format(ip1.split("/")[0]))

nodes.addNode(admin_host.name, ip=ip2, nodeType="host")
nodes.addLink(switch_list[lengthOfRing].name, admin_host.name)

snet_counter += 1

for snet in snet_list:
    snet.installSubnetTable()

info('*** Exp Setup\n')

nodes.writeFile("topo.txt")
os.system("docker cp /home/wcr/diagnosis-driver/driver.tar.bz mn.admin:/")
os.system("docker cp /home/wcr/Mininet-Emulab/topo.txt mn.admin:/")
os.system("docker cp /home/wcr/behavioral-model/tools/fault_injector.py mn.admin:/")
os.system("docker cp /home/wcr/diagnosis-driver/config_example_ring+.txt mn.admin:/")

info('*** Starting network\n')

for host in host_list:
    host.start()

for switch in switch_list:
    switch.addRoutingConfig("ospfd", "log file /tmp/quagga.log")
    switch.start()

net.start()

info('*** Running CLI\n')

CLI(net)

info('*** Stopping network')

net.stop()
