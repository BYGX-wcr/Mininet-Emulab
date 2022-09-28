#!/usr/bin/python
"""
A topology of five ASs, meant to be generic for fault injection.
"""

import sys
sys.path.append('/m/local2/wcr/Mininet-Emulab')

from mininet.net import Containernet
from mininet.node import *
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from mininet.config import Subnet, NodeList
import os
setLogLevel('info')

net = Containernet(controller=Controller)
nodes = NodeList() # used for generating topology file
admin_ip = ""
fault_report_collection_port = 9024

info('*** Adding docker containers\n')
host_image = "localhost/rockylinux:v1"
host_dict = dict()
host_count = 0

switch_image = "localhost/p4switch-frr:v9"
switch_dict = dict()
switch_count = 0
as_map = dict()

info('*** AS 1 (with admin host)\n')

# d0
for i in range(0, 1):
    new_host = net.addDocker('d{}'.format(host_count), dimage=host_image)
    as_map['d{}'.format(host_count)] = 1
    host_dict['d{}'.format(host_count)] = new_host
    host_count += 1

# admin
host_dict['admin'] = net.addDocker('admin', dimage=switch_image)

# s0
for i in range(0, 1):
    new_switch = net.addDocker('s{}'.format(switch_count), cls=DockerP4Router, 
                         dimage=switch_image,
                         software="frr",
                         json_path="/m/local2/wcr/P4-Switches/diagnosable_switch_v1.json", 
                         pcap_dump="/tmp",
                         log_console=True,
                         log_level="info",
                         rt_mediator= "/m/local2/wcr/P4-Switches/rt_mediator.py",
                         runtime_api= "/m/local2/wcr/P4-Switches/runtime_API.py",
                         switch_agent= "/m/local2/wcr/P4-Switches/switch_agent.py",
                         bgpd='yes',
                         ospfd='yes')
    as_map['s{}'.format(switch_count)] = 1
    switch_dict['s{}'.format(switch_count)] = new_switch
    switch_count += 1

    new_switch.addRoutingConfig(configStr="log file /tmp/frr.log debugging")
    new_switch.addRoutingConfig(configStr="debug bgp neighbor-events")
    new_switch.addRoutingConfig(configStr="debug bgp bfd")
    new_switch.addRoutingConfig(configStr="debug bgp nht")
    new_switch.addRoutingConfig(configStr="debug zebra dplane detailed")
    new_switch.addRoutingConfig("bgpd", "router bgp {asn}".format(asn=1))
    new_switch.addRoutingConfig("bgpd", "bgp router-id " + new_switch.getLoopbackIP())
    # new_switch.addRoutingConfig("bgpd", "no bgp ebgp-requires-policy")
    new_switch.addRoutingConfig("ospfd", "router ospf")
    new_switch.addRoutingConfig("ospfd", "ospf router-id " + new_switch.getLoopbackIP())

info('*** AS 2\n')

# d1 d2
for i in range(0, 2):
    new_host = net.addDocker('d{}'.format(host_count), dimage=host_image)
    as_map['d{}'.format(host_count)] = 2
    host_dict['d{}'.format(host_count)] = new_host
    host_count += 1

# s1 s2 s3 s4 s5 s6 s7
for i in range(0, 7):
    new_switch = net.addDocker('s{}'.format(switch_count), cls=DockerP4Router, 
                         dimage=switch_image,
                         software="frr",
                         json_path="/m/local2/wcr/P4-Switches/diagnosable_switch_v1.json", 
                         pcap_dump="/tmp",
                         log_console=True,
                         log_level="info",
                         rt_mediator= "/m/local2/wcr/P4-Switches/rt_mediator.py",
                         runtime_api= "/m/local2/wcr/P4-Switches/runtime_API.py",
                         switch_agent= "/m/local2/wcr/P4-Switches/switch_agent.py",
                         bgpd='yes',
                         ospfd='yes')
    as_map['s{}'.format(switch_count)] = 2
    switch_dict['s{}'.format(switch_count)] = new_switch
    switch_count += 1

    new_switch.addRoutingConfig(configStr="log file /tmp/frr.log debugging")
    new_switch.addRoutingConfig(configStr="debug bgp neighbor-events")
    new_switch.addRoutingConfig(configStr="debug bgp bfd")
    new_switch.addRoutingConfig(configStr="debug bgp nht")
    new_switch.addRoutingConfig(configStr="debug zebra dplane detailed")
    new_switch.addRoutingConfig("bgpd", "router bgp {asn}".format(asn=2))
    new_switch.addRoutingConfig("bgpd", "bgp router-id " + new_switch.getLoopbackIP())
    # new_switch.addRoutingConfig("bgpd", "no bgp ebgp-requires-policy")
    new_switch.addRoutingConfig("ospfd", "router ospf")
    new_switch.addRoutingConfig("ospfd", "ospf router-id " + new_switch.getLoopbackIP())

info('*** AS 3\n')

# d3 d4
for i in range(0, 2):
    new_host = net.addDocker('d{}'.format(host_count), dimage=host_image)
    as_map['d{}'.format(host_count)] = 3
    host_dict['d{}'.format(host_count)] = new_host
    host_count += 1

# s8 s9 s10 s11 s12 s13 s14
for i in range(0, 7):
    new_switch = net.addDocker('s{}'.format(switch_count), cls=DockerP4Router, 
                         dimage=switch_image,
                         software="frr",
                         json_path="/m/local2/wcr/P4-Switches/diagnosable_switch_v1.json", 
                         pcap_dump="/tmp",
                         log_console=True,
                         log_level="info",
                         rt_mediator= "/m/local2/wcr/P4-Switches/rt_mediator.py",
                         runtime_api= "/m/local2/wcr/P4-Switches/runtime_API.py",
                         switch_agent= "/m/local2/wcr/P4-Switches/switch_agent.py",
                         bgpd='yes',
                         ospfd='yes')
    as_map['s{}'.format(switch_count)] = 3
    switch_dict['s{}'.format(switch_count)] = new_switch
    switch_count += 1

    new_switch.addRoutingConfig(configStr="log file /tmp/frr.log debugging")
    new_switch.addRoutingConfig(configStr="debug bgp neighbor-events")
    new_switch.addRoutingConfig(configStr="debug bgp bfd")
    new_switch.addRoutingConfig(configStr="debug bgp nht")
    new_switch.addRoutingConfig(configStr="debug zebra dplane detailed")
    new_switch.addRoutingConfig("bgpd", "router bgp {asn}".format(asn=3))
    new_switch.addRoutingConfig("bgpd", "bgp router-id " + new_switch.getLoopbackIP())
    # new_switch.addRoutingConfig("bgpd", "no bgp ebgp-requires-policy")
    new_switch.addRoutingConfig("ospfd", "router ospf")
    new_switch.addRoutingConfig("ospfd", "ospf router-id " + new_switch.getLoopbackIP())

info('*** AS 4\n')

# d5
for i in range(0, 1):
    new_host = net.addDocker('d{}'.format(host_count), dimage=host_image)
    as_map['d{}'.format(host_count)] = 4
    host_dict['d{}'.format(host_count)] = new_host
    host_count += 1

# s15
for i in range(0, 1):
    new_switch = net.addDocker('s{}'.format(switch_count), cls=DockerP4Router, 
                         dimage=switch_image,
                         software="frr",
                         json_path="/m/local2/wcr/P4-Switches/diagnosable_switch_v1.json", 
                         pcap_dump="/tmp",
                         log_console=True,
                         log_level="info",
                         rt_mediator= "/m/local2/wcr/P4-Switches/rt_mediator.py",
                         runtime_api= "/m/local2/wcr/P4-Switches/runtime_API.py",
                         switch_agent= "/m/local2/wcr/P4-Switches/switch_agent.py",
                         bgpd='yes',
                         ospfd='yes')
    as_map['s{}'.format(switch_count)] = 4
    switch_dict['s{}'.format(switch_count)] = new_switch
    switch_count += 1

    new_switch.addRoutingConfig(configStr="log file /tmp/frr.log debugging")
    new_switch.addRoutingConfig(configStr="debug bgp neighbor-events")
    new_switch.addRoutingConfig(configStr="debug bgp bfd")
    new_switch.addRoutingConfig(configStr="debug bgp nht")
    new_switch.addRoutingConfig(configStr="debug zebra dplane detailed")
    new_switch.addRoutingConfig("bgpd", "router bgp {asn}".format(asn=4))
    new_switch.addRoutingConfig("bgpd", "bgp router-id " + new_switch.getLoopbackIP())
    # new_switch.addRoutingConfig("bgpd", "no bgp ebgp-requires-policy")
    new_switch.addRoutingConfig("ospfd", "router ospf")
    new_switch.addRoutingConfig("ospfd", "ospf router-id " + new_switch.getLoopbackIP())

info('*** AS 5\n')

# d6 d7
for i in range(0, 2):
    new_host = net.addDocker('d{}'.format(host_count), dimage=host_image)
    as_map['d{}'.format(host_count)] = 5
    host_dict['d{}'.format(host_count)] = new_host
    host_count += 1

# s16 s17 s18 s19
for i in range(0, 4):
    new_switch = net.addDocker('s{}'.format(switch_count), cls=DockerP4Router, 
                         dimage=switch_image,
                         software="frr",
                         json_path="/m/local2/wcr/P4-Switches/diagnosable_switch_v1.json", 
                         pcap_dump="/tmp",
                         log_console=True,
                         log_level="info",
                         rt_mediator= "/m/local2/wcr/P4-Switches/rt_mediator.py",
                         runtime_api= "/m/local2/wcr/P4-Switches/runtime_API.py",
                         switch_agent= "/m/local2/wcr/P4-Switches/switch_agent.py",
                         bgpd='yes',
                         ospfd='yes')
    as_map['s{}'.format(switch_count)] = 5
    switch_dict['s{}'.format(switch_count)] = new_switch
    switch_count += 1

    new_switch.addRoutingConfig(configStr="log file /tmp/frr.log debugging")
    new_switch.addRoutingConfig(configStr="debug bgp neighbor-events")
    new_switch.addRoutingConfig(configStr="debug bgp bfd")
    new_switch.addRoutingConfig(configStr="debug bgp nht")
    new_switch.addRoutingConfig(configStr="debug zebra dplane detailed")
    new_switch.addRoutingConfig("bgpd", "router bgp {asn}".format(asn=5))
    new_switch.addRoutingConfig("bgpd", "bgp router-id " + new_switch.getLoopbackIP())
    # new_switch.addRoutingConfig("bgpd", "no bgp ebgp-requires-policy")
    new_switch.addRoutingConfig("ospfd", "router ospf")
    new_switch.addRoutingConfig("ospfd", "ospf router-id " + new_switch.getLoopbackIP())

info('*** Creating links & Configure routes\n')

info('*** Global\n')

snet_list = list()
for i in range(0, 20):
    new_snet = Subnet(ipStr="10.0.{}.0".format(i), prefixLen=24)
    snet_list.append(new_snet)
snet_counter = 0

# EBGP pairs between admin switch s0 and edge switches of all the other ASes
admin_pairs = [("s0", "s1"), ("s0", "s8"), ("s0", "s15"), ("s0", "s16")]

for t in admin_pairs:
    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()

    index1 = t[0]
    index2 = t[1]

    # configure links
    link = net.addLink(switch_dict[index1], switch_dict[index2], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_dict[index1], switch_dict[index2])

    nodes.addNode(switch_dict[index1].name, ip=switch_dict[index1].getLoopbackIP(), nodeType="switch")
    nodes.addNode(switch_dict[index2].name, ip=switch_dict[index2].getLoopbackIP(), nodeType="switch")
    nodes.addLink(switch_dict[index1].name, switch_dict[index2].name, ip1=ip1, ip2=ip2)

    # configure eBGP peers
    switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(ip2.split("/")[0], as_map[index2]))
    switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(ip2.split("/")[0]))
    switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} route-map DENY_ADMIN_RMAP out".format(ip2.split("/")[0]))
    switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} route-map PERMIT_ADMIN_RMAP in".format(ip2.split("/")[0]))

    switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(ip1.split("/")[0], as_map[index1]))
    switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(ip1.split("/")[0]))
    switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} route-map PERMIT_ADMIN_RMAP out".format(ip1.split("/")[0]))
    switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} route-map DENY_ADMIN_RMAP in".format(ip1.split("/")[0]))

    # add new advertised network prefix
    switch_dict[index1].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
    switch_dict[index2].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())

    snet_counter += 1

# EBGP pairs between edge switches of non-admin ASes
switch_pairs = [("s2", "s15"), ("s9", "s15"), ("s10", "s17"), ("s3", "s16")]

for t in switch_pairs:
    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()

    index1 = t[0]
    index2 = t[1]

    # configure links
    link = net.addLink(switch_dict[index1], switch_dict[index2], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_dict[index1], switch_dict[index2])

    nodes.addNode(switch_dict[index1].name, ip=switch_dict[index1].getLoopbackIP(), nodeType="switch")
    nodes.addNode(switch_dict[index2].name, ip=switch_dict[index2].getLoopbackIP(), nodeType="switch")
    nodes.addLink(switch_dict[index1].name, switch_dict[index2].name, ip1=ip1, ip2=ip2)

    # configure eBGP peers
    switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(ip2.split("/")[0], as_map[index2]))
    switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(ip2.split("/")[0]))
    switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} route-map OUT_AS_RMAP out".format(ip2.split("/")[0]))
    switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} route-map IN_AS_RMAP in".format(ip2.split("/")[0]))

    switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(ip1.split("/")[0], as_map[index1]))
    switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(ip1.split("/")[0]))
    switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} route-map OUT_AS_RMAP out".format(ip1.split("/")[0]))
    switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} route-map IN_AS_RMAP in".format(ip1.split("/")[0]))

    # add new advertised network prefix
    switch_dict[index1].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
    switch_dict[index2].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())

    snet_counter += 1

for snet in snet_list:
    snet.installSubnetTable()

# configure policy for admin router
s = "s0"
switch_dict[s].addRoutingConfig(configStr="route-map PERMIT_ADMIN_RMAP permit 10\nmatch community ALL_AS")
switch_dict[s].addRoutingConfig(configStr="route-map DENY_ADMIN_RMAP permit 10\nmatch ip address prefix-list AS_PREFIX_LIST\nset community 1:1")
switch_dict[s].addRoutingConfig(configStr="route-map DENY_ADMIN_RMAP permit 20\nmatch ip address prefix-list INTERNET_PREFIX_LIST\nset community 0:1")
switch_dict[s].addRoutingConfig(configStr="route-map DENY_ADMIN_RMAP permit 30\nmatch community ADMIN_AS")

switch_dict[s].addRoutingConfig(configStr="ip prefix-list INTERNET_PREFIX_LIST permit 10.0.0.0/16 ge 16")

switch_dict[s].addRoutingConfig(configStr="bgp community-list standard ADMIN_AS permit 1:1")
for asn in range(0, 6):
    switch_dict[s].addRoutingConfig(configStr="bgp community-list standard ALL_AS permit {}:1".format(asn))

# configure policy for edge routers
for s in {"s1", "s2", "s3", "s8", "s9", "s10", "s15", "s16", "s17"}:
    switch_dict[s].addRoutingConfig(configStr="route-map OUT_AS_RMAP permit 10\nmatch ip address prefix-list AS_PREFIX_LIST\nset community {}:1".format(as_map[s]))
    switch_dict[s].addRoutingConfig(configStr="route-map OUT_AS_RMAP permit 20\nmatch ip address prefix-list INTERNET_PREFIX_LIST\nset community 0:1")
    switch_dict[s].addRoutingConfig(configStr="route-map OUT_AS_RMAP permit 30\nmatch community OUT_AS")
    switch_dict[s].addRoutingConfig(configStr="route-map IN_AS_RMAP permit 10\nmatch community IN_AS")

    switch_dict[s].addRoutingConfig(configStr="route-map PERMIT_ADMIN_RMAP permit 10\nmatch ip address prefix-list AS_PREFIX_LIST\nset community {}:1".format(as_map[s]))
    switch_dict[s].addRoutingConfig(configStr="route-map PERMIT_ADMIN_RMAP permit 20\nmatch ip address prefix-list INTERNET_PREFIX_LIST\nset community 0:1")
    switch_dict[s].addRoutingConfig(configStr="route-map PERMIT_ADMIN_RMAP permit 30\nmatch community ALL_AS")
    switch_dict[s].addRoutingConfig(configStr="route-map DENY_ADMIN_RMAP permit 10\nmatch community ADMIN_AS")

    switch_dict[s].addRoutingConfig(configStr="ip prefix-list INTERNET_PREFIX_LIST permit 10.0.0.0/16 ge 16")

    switch_dict[s].addRoutingConfig(configStr="bgp community-list standard IN_AS permit 0:1")
    switch_dict[s].addRoutingConfig(configStr="bgp community-list standard OUT_AS permit 0:1")
    switch_dict[s].addRoutingConfig(configStr="bgp community-list standard ADMIN_AS permit 1:1")
    for asn in range(0, 6):
        switch_dict[s].addRoutingConfig(configStr="bgp community-list standard ALL_AS permit {}:1".format(asn))

# s1 advertise and accept routes from all AS
for i in range(1, 6):
    switch_dict["s1"].addRoutingConfig(configStr="bgp community-list standard OUT_AS permit {}:1".format(i))
for i in range(1, 6):
    switch_dict["s1"].addRoutingConfig(configStr="bgp community-list standard IN_AS permit {}:1".format(i))

# s2 advertise and accept routes from all AS
for i in range(1, 6):
    switch_dict["s2"].addRoutingConfig(configStr="bgp community-list standard OUT_AS permit {}:1".format(i))
for i in range(1, 6):
    switch_dict["s2"].addRoutingConfig(configStr="bgp community-list standard IN_AS permit {}:1".format(i))

# s3 does not advertise routes from other AS and only accept routes from AS 2 and 5
switch_dict["s3"].addRoutingConfig(configStr="bgp community-list standard OUT_AS permit 2:1")
for i in {2, 5}:
    switch_dict["s3"].addRoutingConfig(configStr="bgp community-list standard IN_AS permit {}:1".format(i))

# s8 does not advertise routes from other AS and but accept routes from all AS
switch_dict["s8"].addRoutingConfig(configStr="bgp community-list standard OUT_AS permit 3:1")
for i in range(1, 6):
    switch_dict["s8"].addRoutingConfig(configStr="bgp community-list standard IN_AS permit {}:1".format(i))

# s9 does not advertise routes from other AS and only accept routes from AS 3 and 4
switch_dict["s9"].addRoutingConfig(configStr="bgp community-list standard OUT_AS permit 3:1")
for i in {3, 4}:
    switch_dict["s9"].addRoutingConfig(configStr="bgp community-list standard IN_AS permit {}:1".format(i))

# s10 advertise and accept routes from all AS
for i in range(1, 6):
    switch_dict["s10"].addRoutingConfig(configStr="bgp community-list standard OUT_AS permit {}:1".format(i))
for i in range(1, 6):
    switch_dict["s10"].addRoutingConfig(configStr="bgp community-list standard IN_AS permit {}:1".format(i))

# s15 advertise and accept routes from all AS
for i in range(1, 6):
    switch_dict["s15"].addRoutingConfig(configStr="bgp community-list standard OUT_AS permit {}:1".format(i))
for i in range(1, 6):
    switch_dict["s15"].addRoutingConfig(configStr="bgp community-list standard IN_AS permit {}:1".format(i))

# s16 does not advertise routes from other AS and accept routes from all AS
switch_dict["s16"].addRoutingConfig(configStr="bgp community-list standard OUT_AS permit 5:1")
for i in range(1, 6):
    switch_dict["s16"].addRoutingConfig(configStr="bgp community-list standard IN_AS permit {}:1".format(i))

# s17 does not advertise routes from other ASand accept routes from all AS
switch_dict["s17"].addRoutingConfig(configStr="bgp community-list standard OUT_AS permit 5:1".format(i))
for i in range(1, 6):
    switch_dict["s17"].addRoutingConfig(configStr="bgp community-list standard IN_AS permit {}:1".format(i))


info('*** AS1\n')

snet_list = list()
for i in range(0, 20):
    new_snet = Subnet(ipStr="10.1.{}.0".format(i), prefixLen=24)
    snet_list.append(new_snet)

snet_counter = 0

# configure intra-AS switch-switch links

# configure host-switch links

hs_pairs = [("s0", "d0")]
for t in hs_pairs:
    sid = t[0]
    hid = t[1]

    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    net.addLink(switch_dict[sid], host_dict[hid], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_dict[sid])
    switch_dict[sid].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))

    host_dict[hid].setDefaultRoute("gw {}".format(ip1.split("/")[0]))

    nodes.addNode(host_dict[hid].name, ip=ip2, nodeType="host")
    nodes.addLink(switch_dict[sid].name, host_dict[hid].name, ip1, ip2)

    # add a new advertised network prefix for the AS
    switch_dict[sid].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
    switch_dict[sid].addRoutingConfig(configStr="ip prefix-list AS_PREFIX_LIST permit " + snet_list[snet_counter].getNetworkPrefix())

    snet_counter += 1

# configure link to admin host

sid = "s0"
hid = "admin"

ip1 = snet_list[snet_counter].allocateIPAddr()
ip2 = snet_list[snet_counter].allocateIPAddr()
net.addLink(switch_dict[sid], host_dict[hid], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
snet_list[snet_counter].addNode(switch_dict[sid])
switch_dict[sid].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))

host_dict[hid].setDefaultRoute("gw {}".format(ip1.split("/")[0]))

nodes.addNode(host_dict[hid].name, ip=ip2, nodeType="host")
nodes.addLink(switch_dict[sid].name, host_dict[hid].name, ip1, ip2)

# add a new advertised network prefix for the AS
switch_dict[sid].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
switch_dict[sid].addRoutingConfig(configStr="ip prefix-list AS_PREFIX_LIST permit " + snet_list[snet_counter].getNetworkPrefix())

# set up admin_ip
admin_ip = ip2.split("/")[0]

snet_counter += 1

for snet in snet_list:
    snet.installSubnetTable()

info('*** AS2\n')

edge_switches = {"s1", "s2", "s3"}
route_reflectors = {"s4", "s5"}
inner_switches = {"s6", "s7"}

snet_list = list()
for i in range(0, 20):
    new_snet = Subnet(ipStr="10.2.{}.0".format(i), prefixLen=24)
    snet_list.append(new_snet)

snet_counter = 0

# configure intra-AS switch-switch links

switch_pairs = [("s1", "s4"), ("s1", "s5"), ("s2", "s4"), ("s2", "s5"), ("s3", "s4"), ("s3", "s5"), ("s6", "s5"), ("s6", "s4"), ("s7", "s5"), ("s7", "s4")]
for t in switch_pairs:
    index1 = t[0]
    index2 = t[1]

    # configure links
    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    link = net.addLink(switch_dict[index1], switch_dict[index2], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_dict[index1], switch_dict[index2])

    # config IGP routing, using OSPF
    switch_dict[index1].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
    switch_dict[index1].addRoutingConfig("ospfd", "network " + switch_dict[index1].getLoopbackIP() + "/32" + " area {}".format(0))
    switch_dict[index2].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
    switch_dict[index2].addRoutingConfig("ospfd", "network " + switch_dict[index2].getLoopbackIP() + "/32" + " area {}".format(0))

    nodes.addNode(switch_dict[index1].name, ip=switch_dict[index1].getLoopbackIP(), nodeType="switch")
    nodes.addNode(switch_dict[index2].name, ip=switch_dict[index2].getLoopbackIP(), nodeType="switch")
    nodes.addLink(switch_dict[index1].name, switch_dict[index2].name, ip1=ip1, ip2=ip2)

    for s in edge_switches:
        switch_dict[s].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
        switch_dict[s].addRoutingConfig(configStr="ip prefix-list AS_PREFIX_LIST permit " + snet_list[snet_counter].getNetworkPrefix())

    snet_counter += 1

# Configure BGP peers in the AS

for s in edge_switches:
    for rr in route_reflectors:
        client_router_ip = switch_dict[s].getLoopbackIP()
        route_reflector_ip = switch_dict[rr].getLoopbackIP()

        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(route_reflector_ip, 2))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(route_reflector_ip, client_router_ip))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(route_reflector_ip))

        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(client_router_ip, 2))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(client_router_ip, route_reflector_ip))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(client_router_ip))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} route-reflector-client".format(client_router_ip))

for s in inner_switches:
    switch_dict[s].addRoutingConfig(configStr="route-map RMAP permit 10\nset community {}:1".format(2))
    for rr in route_reflectors:
        client_router_ip = switch_dict[s].getLoopbackIP()
        route_reflector_ip = switch_dict[rr].getLoopbackIP()

        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(route_reflector_ip, 2))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(route_reflector_ip, client_router_ip))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(route_reflector_ip))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} disable-connected-check".format(route_reflector_ip))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} route-map RMAP out".format(route_reflector_ip))

        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(client_router_ip, 2))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(client_router_ip, route_reflector_ip))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(client_router_ip))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} disable-connected-check".format(client_router_ip))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} route-reflector-client".format(client_router_ip))

# configure host-switch links

hs_pairs = [("s6", "d1"), ("s7", "d2")]
for t in hs_pairs:
    sid = t[0]
    hid = t[1]

    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    net.addLink(switch_dict[sid], host_dict[hid], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_dict[sid])
    switch_dict[sid].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))

    host_dict[hid].setDefaultRoute("gw {}".format(ip1.split("/")[0]))

    nodes.addNode(host_dict[hid].name, ip=ip2, nodeType="host")
    nodes.addLink(switch_dict[sid].name, host_dict[hid].name, ip1, ip2)

    # add a new advertised network prefix for the AS
    switch_dict[sid].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())

    snet_counter += 1

for snet in snet_list:
    snet.installSubnetTable()

info('*** AS3\n')

edge_switches = {"s8", "s9", "s10"}
route_reflectors = {"s11", "s12"}
inner_switches = {"s13", "s14"}

snet_list = list()
for i in range(0, 20):
    new_snet = Subnet(ipStr="10.3.{}.0".format(i), prefixLen=24)
    snet_list.append(new_snet)

snet_counter = 0

# configure intra-AS switch-switch links

switch_pairs = [("s8", "s11"), ("s8", "s12"), ("s9", "s11"), ("s9", "s12"), ("s10", "s11"), ("s10", "s12"), ("s11", "s13"), ("s11", "s14"), ("s12", "s13"), ("s12", "s14")]
for t in switch_pairs:
    index1 = t[0]
    index2 = t[1]

    # configure links
    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    link = net.addLink(switch_dict[index1], switch_dict[index2], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_dict[index1], switch_dict[index2])

    # config IGP routing, using OSPF
    switch_dict[index1].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
    switch_dict[index1].addRoutingConfig("ospfd", "network " + switch_dict[index1].getLoopbackIP() + "/32" + " area {}".format(0))
    switch_dict[index2].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
    switch_dict[index2].addRoutingConfig("ospfd", "network " + switch_dict[index2].getLoopbackIP() + "/32" + " area {}".format(0))

    nodes.addNode(switch_dict[index1].name, ip=switch_dict[index1].getLoopbackIP(), nodeType="switch")
    nodes.addNode(switch_dict[index2].name, ip=switch_dict[index2].getLoopbackIP(), nodeType="switch")
    nodes.addLink(switch_dict[index1].name, switch_dict[index2].name, ip1=ip1, ip2=ip2)

    for s in edge_switches:
        switch_dict[s].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
        switch_dict[s].addRoutingConfig(configStr="ip prefix-list AS_PREFIX_LIST permit " + snet_list[snet_counter].getNetworkPrefix())

    snet_counter += 1

# Configure BGP peers in the AS

for s in edge_switches:
    for rr in route_reflectors:
        client_router_ip = switch_dict[s].getLoopbackIP()
        route_reflector_ip = switch_dict[rr].getLoopbackIP()

        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(route_reflector_ip, 3))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(route_reflector_ip, client_router_ip))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(route_reflector_ip))

        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(client_router_ip, 3))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(client_router_ip, route_reflector_ip))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(client_router_ip))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} route-reflector-client".format(client_router_ip))

for s in inner_switches:
    for rr in route_reflectors:
        client_router_ip = switch_dict[s].getLoopbackIP()
        route_reflector_ip = switch_dict[rr].getLoopbackIP()

        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(route_reflector_ip, 3))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(route_reflector_ip, client_router_ip))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(route_reflector_ip))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} disable-connected-check".format(route_reflector_ip))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} route-map RMAP out".format(route_reflector_ip))
        switch_dict[s].addRoutingConfig(configStr="route-map RMAP permit 10\nset community {}:1".format(3))

        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(client_router_ip, 3))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(client_router_ip, route_reflector_ip))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(client_router_ip))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} disable-connected-check".format(client_router_ip))
        switch_dict[rr].addRoutingConfig("bgpd", "neighbor {} route-reflector-client".format(client_router_ip))

# configure host-switch links

hs_pairs = [("s13", "d3"), ("s14", "d4")]
for t in hs_pairs:
    sid = t[0]
    hid = t[1]

    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    net.addLink(switch_dict[sid], host_dict[hid], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_dict[sid])
    switch_dict[sid].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))

    host_dict[hid].setDefaultRoute("gw {}".format(ip1.split("/")[0]))

    nodes.addNode(host_dict[hid].name, ip=ip2, nodeType="host")
    nodes.addLink(switch_dict[sid].name, host_dict[hid].name, ip1, ip2)

    # add a new advertised network prefix for the AS
    switch_dict[sid].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())

    snet_counter += 1

for snet in snet_list:
    snet.installSubnetTable()

info('*** AS4\n')

snet_list = list()
for i in range(0, 20):
    new_snet = Subnet(ipStr="10.4.{}.0".format(i), prefixLen=24)
    snet_list.append(new_snet)

snet_counter = 0

# configure intra-AS switch-switch links

# configure host-switch links

hs_pairs = [("s15", "d5")]
for t in hs_pairs:
    sid = t[0]
    hid = t[1]

    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    net.addLink(switch_dict[sid], host_dict[hid], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_dict[sid])
    switch_dict[sid].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))

    host_dict[hid].setDefaultRoute("gw {}".format(ip1.split("/")[0]))

    nodes.addNode(host_dict[hid].name, ip=ip2, nodeType="host")
    nodes.addLink(switch_dict[sid].name, host_dict[hid].name, ip1, ip2)

    # add a new advertised network prefix for the AS
    switch_dict[sid].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
    switch_dict[sid].addRoutingConfig(configStr="ip prefix-list AS_PREFIX_LIST permit " + snet_list[snet_counter].getNetworkPrefix())

    snet_counter += 1

for snet in snet_list:
    snet.installSubnetTable()

info('*** AS5\n')

edge_switches = {"s16", "s17"}
inner_switches = {"s18", "s19"}

snet_list = list()
for i in range(0, 20):
    new_snet = Subnet(ipStr="10.5.{}.0".format(i), prefixLen=24)
    snet_list.append(new_snet)

snet_counter = 0

# configure intra-AS switch-switch links

switch_pairs = [("s16", "s18"), ("s16", "s19"), ("s17", "s18"), ("s17", "s19")]
for t in switch_pairs:
    index1 = t[0]
    index2 = t[1]

    # configure links
    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    link = net.addLink(switch_dict[index1], switch_dict[index2], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_dict[index1], switch_dict[index2])

    # config IGP routing, using OSPF
    switch_dict[index1].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
    switch_dict[index1].addRoutingConfig("ospfd", "network " + switch_dict[index1].getLoopbackIP() + "/32" + " area {}".format(0))
    switch_dict[index2].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
    switch_dict[index2].addRoutingConfig("ospfd", "network " + switch_dict[index2].getLoopbackIP() + "/32" + " area {}".format(0))

    nodes.addNode(switch_dict[index1].name, ip=switch_dict[index1].getLoopbackIP(), nodeType="switch")
    nodes.addNode(switch_dict[index2].name, ip=switch_dict[index2].getLoopbackIP(), nodeType="switch")
    nodes.addLink(switch_dict[index1].name, switch_dict[index2].name, ip1=ip1, ip2=ip2)

    for s in edge_switches:
        switch_dict[s].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
        switch_dict[s].addRoutingConfig(configStr="ip prefix-list AS_PREFIX_LIST permit " + snet_list[snet_counter].getNetworkPrefix())

    snet_counter += 1

# Configure BGP peers in the AS

for s in edge_switches:
    for ins in inner_switches:
        client_router_ip = switch_dict[s].getLoopbackIP()
        route_reflector_ip = switch_dict[ins].getLoopbackIP()

        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(route_reflector_ip, 5))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(route_reflector_ip, client_router_ip))
        switch_dict[s].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(route_reflector_ip))

        switch_dict[ins].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(client_router_ip, 5))
        switch_dict[ins].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(client_router_ip, route_reflector_ip))
        switch_dict[ins].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(client_router_ip))
        switch_dict[ins].addRoutingConfig("bgpd", "neighbor {} route-map RMAP out".format(client_router_ip))
        switch_dict[ins].addRoutingConfig(configStr="route-map RMAP permit 10\nset community {}:1".format(5))

# configure host-switch links

hs_pairs = [("s18", "d6"), ("s19", "d7")]
for t in hs_pairs:
    sid = t[0]
    hid = t[1]

    ip1 = snet_list[snet_counter].allocateIPAddr()
    ip2 = snet_list[snet_counter].allocateIPAddr()
    net.addLink(switch_dict[sid], host_dict[hid], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
    snet_list[snet_counter].addNode(switch_dict[sid])
    switch_dict[sid].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))

    host_dict[hid].setDefaultRoute("gw {}".format(ip1.split("/")[0]))

    nodes.addNode(host_dict[hid].name, ip=ip2, nodeType="host")
    nodes.addLink(switch_dict[sid].name, host_dict[hid].name, ip1, ip2)

    # add a new advertised network prefix for the AS
    switch_dict[sid].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())

    snet_counter += 1

for snet in snet_list:
    snet.installSubnetTable()

info('*** Exp Setup\n')

nodes.writeFile("topo.txt")
os.system("docker cp /m/local2/wcr/Diagnosis-driver/driver.tar.bz mn.admin:/")
os.system("docker cp /m/local2/wcr/Mininet-Emulab/topo.txt mn.admin:/")

print("tar: ", host_dict["admin"].cmd("tar -xf /driver.tar.bz -C /"))
print("install dns: ", host_dict["admin"].cmd("python3 /network_graph.py /topo.txt"))
print("start query backend: ", host_dict["admin"].cmd("python3 /network_model.py --ribs-dir /ribs --topo /topo.txt --fsi-dir /fsi &"))

info('*** Starting network\n')

for host in host_dict.values():
    host.start()

for switch in switch_dict.keys():
    switch_dict[switch].setAdminConfig(admin_ip, fault_report_collection_port)
    switch_dict[switch].start()

net.start()

# restart frr to solve the uninstalled route issue
time.sleep(20)
for switch in {"s6", "s7", "s13", "s14"}:
    switch_dict[switch].cmd("/etc/init.d/frr restart")

info('*** Running CLI\n')

CLI(net)

info('*** Stopping network')

net.stop()