#!/usr/bin/python
"""
A topology of three ASs connected to form a triangle.
"""
import sys
sys.path.append('/m/local2/wcr/Mininet-Emulab')

from mininet.net import Containernet
from mininet.node import * #Controller, Docker, DockerRouter, DockerP4Router
from mininet.nodelib import LinuxBridge
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.config import Subnet, NodeList
import os
setLogLevel('info')

net = Containernet(controller=Controller)
numOfAS = 3
sizeOfAS = 3
nodes = NodeList() # used for generating topology file
admin_ip = ""
pingmesh_admin_ip = ""
fault_report_collection_port = 9024
trouble_report_collection_port = 9026

info('*** Adding docker containers\n')

host_dict = dict()
for i in range(0, numOfAS * (sizeOfAS - 1)):
    new_host = net.addDocker('d{}'.format(i), cls=DockerPingHost, dimage="localhost/rockylinux:v2", monitor="/m/local2/wcr/Diagnosis-driver/pingmesh_client.py")
    host_dict['d{}'.format(i)] = new_host
    nodes.addNode(new_host.name, lanIp=new_host.getLANIp(), nodeType="host")

host_dict['admin'] = net.addDocker('admin', cls=DockerPingHost, dimage="localhost/admin-host:v1", monitor="/m/local2/wcr/Diagnosis-driver/pingmesh_client.py")
nodes.addNode(host_dict['admin'].name, lanIp=host_dict['admin'].getLANIp(), nodeType="host")

info('*** Adding switches\n')

switch_dict = dict()
for i in range(0, numOfAS * sizeOfAS):
    new_switch = net.addDocker('s{}'.format(i), cls=DockerP4Router, 
                         dimage="localhost/p4switch-frr:test1",
                         software="frr",
                         json_path="/m/local2/wcr/P4-Switches/diagnosable_switch_v1.json", 
                         pcap_dump="/tmp",
                         log_console=True,
                         log_level="info",
                         rt_mediator= "/m/local2/wcr/P4-Switches/rt_mediator.py",
                         runtime_api= "/m/local2/wcr/P4-Switches/runtime_API.py",
                         switch_agent= "/m/local2/wcr/P4-Switches/switch_agent.py",
                         packet_injector= "/m/local2/wcr/P4-Switches/packet_injector.py",
                         bgp_adv_modifier= "/m/local2/wcr/P4-Switches/bgp_adv_modify.o",
                         bgpd='yes',
                         ospfd='yes')
    switch_dict['s{}'.format(i)] = new_switch
    nodes.addNode(new_switch.name, lanIp=new_switch.getLANIp(), loopbackIp=new_switch.getLoopbackIP(), nodeType="switch")

    new_switch.addRoutingConfig(configStr="log file /tmp/frr.log debugging")
    new_switch.addRoutingConfig(configStr="debug bgp neighbor-events")
    new_switch.addRoutingConfig(configStr="debug bgp bfd")
    new_switch.addRoutingConfig(configStr="debug bgp nht")

    new_switch.addRoutingConfig("bgpd", "router bgp {asn}".format(asn=int(i / sizeOfAS + 1)))
    new_switch.addRoutingConfig("bgpd", "bgp router-id " + new_switch.getLoopbackIP())
    new_switch.addRoutingConfig("bgpd", "network {}/32".format(new_switch.getLoopbackIP()))
    new_switch.addRoutingConfig("bgpd", "redistribute ospf")
    new_switch.addRoutingConfig("ospfd", "router ospf")
    new_switch.addRoutingConfig("ospfd", "ospf router-id " + new_switch.getLoopbackIP())

info('*** Adding subnets\n')
snet_list = list()
for i in range(0, 100):
    new_snet = Subnet(ipStr="10.{}.0.0".format(i), prefixLen=24)
    snet_list.append(new_snet)

info('*** Creating links & Configure routes\n')

snet_counter = 0

# configure inter-AS switch-switch links
for i in range(0, numOfAS):
    switch_name = "s{}".format(i * sizeOfAS)
    switch_dict[switch_name].addRoutingConfig(configStr="route-map OUT_AS_RMAP permit 10\nmatch ip address prefix-list AS_PREFIX_LIST\nset community {}:1".format(i + 1, i + 1))
    switch_dict[switch_name].addRoutingConfig(configStr="route-map OUT_AS_RMAP permit 20\nmatch ip address prefix-list INTERNET_PREFIX_LIST\nset community 0:1")
    switch_dict[switch_name].addRoutingConfig(configStr="route-map OUT_AS_RMAP permit 30\nmatch ip address prefix-list LB_PREFIX_LIST\nset community 0:1")
    switch_dict[switch_name].addRoutingConfig(configStr="route-map OUT_AS_RMAP permit 40\nmatch community OUT_AS_FILTER")
    switch_dict[switch_name].addRoutingConfig(configStr="route-map IN_AS_RMAP permit 10\nmatch community IN_AS_FILTER")
    switch_dict[switch_name].addRoutingConfig(configStr="ip prefix-list LB_PREFIX_LIST permit 192.168.19.0/24  ge 24")

    for j in range(i + 1, numOfAS):
        index1 = "s{}".format(i * sizeOfAS)
        index2 = "s{}".format(j * sizeOfAS)

        if i != j:
            ip1 = snet_list[snet_counter].allocateIPAddr()
            ip2 = snet_list[snet_counter].allocateIPAddr()

            # configure links
            link = net.addLink(switch_dict[index1], switch_dict[index2], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
            snet_list[snet_counter].addNode(switch_dict[index1], switch_dict[index2])

            nodes.addLink(switch_dict[index1].name, switch_dict[index2].name, ip1=ip1, ip2=ip2)

            # configure eBGP peers
            switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(ip2.split("/")[0], j + 1))
            switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(ip2.split("/")[0]))
            switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} route-map OUT_AS_RMAP out".format(ip2.split("/")[0]))
            switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} route-map IN_AS_RMAP in".format(ip2.split("/")[0]))

            switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(ip1.split("/")[0], i + 1))
            switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(ip1.split("/")[0]))
            switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} route-map OUT_AS_RMAP out".format(ip1.split("/")[0]))
            switch_dict[index2].addRoutingConfig("bgpd", "neighbor {} route-map IN_AS_RMAP in".format(ip1.split("/")[0]))

            # add new advertised network prefix
            switch_dict[index1].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
            switch_dict[index2].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
            switch_dict[index1].addRoutingConfig(configStr="ip prefix-list INTERNET_PREFIX_LIST permit {}".format(snet_list[snet_counter].getNetworkPrefix()))
            switch_dict[index2].addRoutingConfig(configStr="ip prefix-list INTERNET_PREFIX_LIST permit {}".format(snet_list[snet_counter].getNetworkPrefix()))

            snet_counter += 1

    for j in range(0, numOfAS):
        if j != i:
            switch_dict[switch_name].addRoutingConfig(configStr="bgp community-list standard OUT_AS_FILTER deny {}:1".format(j + 1))
            switch_dict[switch_name].addRoutingConfig(configStr="bgp community-list standard IN_AS_FILTER permit {}:1".format(j + 1))

    switch_dict[switch_name].addRoutingConfig(configStr="bgp community-list standard OUT_AS_FILTER permit {}:1".format(i + 1))
    switch_dict[switch_name].addRoutingConfig(configStr="bgp community-list standard OUT_AS_FILTER permit {}:1".format(0))
    switch_dict[switch_name].addRoutingConfig(configStr="bgp community-list standard IN_AS_FILTER permit {}:1".format(0))

# configure intra-AS switch-switch links
for i in range(0, numOfAS):
    edgeRouter = "s{}".format(i * sizeOfAS)
    edgeRouterIp = ""

    # configure a single AS
    bgp_network_list = []
    for j in range(0, sizeOfAS):
        index1 = "s{}".format(i * sizeOfAS + j)
        index2 =  "s{}".format(i * sizeOfAS + (j + 1) % sizeOfAS)

        # configure links
        ip1 = snet_list[snet_counter].allocateIPAddr()
        ip2 = snet_list[snet_counter].allocateIPAddr()
        link = net.addLink(switch_dict[index1], switch_dict[index2], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
        snet_list[snet_counter].addNode(switch_dict[index1], switch_dict[index2])

        # config IGP routing, using OSPF
        switch_dict[index1].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
        switch_dict[index1].addRoutingConfig("ospfd", "network " + switch_dict[index1].getLoopbackIP() + "/32" + " area {}".format(0))
        switch_dict[index2].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))

        # select edge router ip
        if index1 == edgeRouter:
            edgeRouterIp = switch_dict[index1].getLoopbackIP()

        # config iBGP peers
        if index1 != edgeRouter:
            loopbackIP1 = switch_dict[index1].getLoopbackIP()

            switch_dict[edgeRouter].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(loopbackIP1, i + 1))
            switch_dict[edgeRouter].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(loopbackIP1, edgeRouterIp))
            switch_dict[edgeRouter].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(loopbackIP1))

            switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} remote-as {}".format(edgeRouterIp, i + 1))
            switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} update-source {}".format(edgeRouterIp, loopbackIP1))
            switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} soft-reconfiguration inbound".format(edgeRouterIp))
            switch_dict[index1].addRoutingConfig("bgpd", "neighbor {} route-map RMAP out".format(edgeRouterIp))
            switch_dict[index1].addRoutingConfig(configStr="route-map RMAP permit 10\nset community {}:1".format(i + 1))

        # add new bgp advertised network prefix
        bgp_network_list.append(snet_list[snet_counter].getNetworkPrefix())

        nodes.addLink(switch_dict[index1].name, switch_dict[index2].name, ip1=ip1, ip2=ip2)

        snet_counter += 1

    # configure the advertised network prefixes for the AS
    for bgpNetwork in bgp_network_list:
        switch_dict[edgeRouter].addRoutingConfig("bgpd", "network " + bgpNetwork)
        switch_dict[edgeRouter].addRoutingConfig(configStr="ip prefix-list AS_PREFIX_LIST permit " + bgpNetwork)

# configure host-switch links
for i in range(0, numOfAS):
    edgeRouter = "s{}".format(i * sizeOfAS)

    # configure a single AS
    for j in range(0, sizeOfAS - 1):
        sid = "s{}".format(i * sizeOfAS + 1 + j)
        hid = "d{}".format(i * (sizeOfAS - 1) + j)

        ip1 = snet_list[snet_counter].allocateIPAddr()
        ip2 = snet_list[snet_counter].allocateIPAddr()
        net.addLink(switch_dict[sid], host_dict[hid], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
        snet_list[snet_counter].addNode(switch_dict[sid])
        switch_dict[sid].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))

        host_dict[hid].setDefaultRoute("gw {}".format(ip1.split("/")[0]))

        nodes.addLink(switch_dict[sid].name, host_dict[hid].name, ip1, ip2)

        switch_dict[edgeRouter].addRoutingConfig(configStr="ip prefix-list AS_PREFIX_LIST permit " + snet_list[snet_counter].getNetworkPrefix())

        snet_counter += 1

# configure the link between admin host and s0
admin_host = host_dict['admin']
ip1 = snet_list[snet_counter].allocateIPAddr()
ip2 = snet_list[snet_counter].allocateIPAddr()
net.addLink(switch_dict['s0'], admin_host, ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
snet_list[snet_counter].addNode(switch_dict['s0'])
switch_dict['s0'].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
admin_host.setDefaultRoute("gw {}".format(ip1.split("/")[0]))
nodes.addLink(switch_dict['s0'].name, admin_host.name, ip1, ip2)
switch_dict['s0'].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
switch_dict['s0'].addRoutingConfig(configStr="ip prefix-list AS_PREFIX_LIST permit " + snet_list[snet_counter].getNetworkPrefix())
snet_counter += 1

# configure the backup interface of the admin host

sid = "s0"
hid = "admin"
ip1 = snet_list[snet_counter].allocateIPAddr()
ip2 = snet_list[snet_counter].allocateIPAddr()
net.addLink(switch_dict[sid], host_dict[hid], ip1=ip1, ip2=ip2, addr1=Subnet.ipToMac(ip1), addr2=Subnet.ipToMac(ip2))
snet_list[snet_counter].addNode(switch_dict[sid])
switch_dict[sid].addRoutingConfig("ospfd", "network " + snet_list[snet_counter].getNetworkPrefix() + " area {}".format(0))
nodes.addLink(switch_dict[sid].name, host_dict[hid].name, ip1, ip2)
host_dict[hid].cmd("ip route add {subnet} dev {host}-eth1 src {intfIP} table 1".format(host=hid, intfIP=ip2.split("/")[0], subnet=snet_list[snet_counter].getNetworkPrefix()))
host_dict[hid].cmd("ip route add default via {gwIP} table 1".format(gwIP=ip1.split("/")[0]))
host_dict[hid].cmd("ip rule add from {intfIP} table 1".format(intfIP=ip2.split("/")[0]))
host_dict[hid].cmd("ip rule add to {intfIP} table 1".format(intfIP=ip2.split("/")[0]))

## add a new advertised network prefix for the AS
switch_dict[sid].addRoutingConfig("bgpd", "network " + snet_list[snet_counter].getNetworkPrefix())
switch_dict[sid].addRoutingConfig(configStr="ip prefix-list AS_PREFIX_LIST permit " + snet_list[snet_counter].getNetworkPrefix())

## set up admin_ip
print("Getting admin IP")
admin_ip = ip2.split("/")[0]
pingmesh_admin_ip = host_dict["admin"].getLANIp()
print("Admin IP: switch-{}, pingmesh-{}".format(admin_ip, pingmesh_admin_ip))

for snet in snet_list:
    snet.installSubnetTable()

info('*** Exp Setup\n')

nodes.writeFile("topo.txt")
nodes.writeHostList("hosts.txt")
os.system("docker cp /m/local2/wcr/Diagnosis-driver/driver.tar.bz mn.admin:/")
os.system("docker cp /m/local2/wcr/Mininet-Emulab/topo.txt mn.admin:/")
os.system("docker cp /m/local2/wcr/Mininet-Emulab/hosts.txt mn.admin:/")

print("tar: ", host_dict["admin"].cmd("tar -xf /driver.tar.bz -C /"))
print("install dns: ", host_dict["admin"].cmd("python3 /network_graph.py /topo.txt"))
print("start batfish server: ", host_dict["admin"].cmd("bash /batfish_integration/server/run_server.sh 2>&1 > /batfish_server.log &"))
host_dict["admin"].cmd("ifconfig eth0 up")

info('*** Starting network\n')

for switch in switch_dict.keys():
    switch_dict[switch].setAdminConfig(admin_ip, fault_report_collection_port)
    switch_dict[switch].start()

for host in host_dict.values():
    host.setAdminConfig(pingmesh_admin_ip, trouble_report_collection_port)
    host.setHostsFile("hosts.txt")
    host.start()

net.start()

info('*** Running CLI\n')

CLI(net)

info('*** Stopping network')

net.stop()
