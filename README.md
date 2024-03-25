# PodNet Network Emulation Platform

This is a project that extends [containernet](https://github.com/containernet/containernet) and [mininet](https://github.com/mininet/mininet).
The goal is to enable the usage of commodity routing software with programmable switch simulators.
The major idea is to containerize every switches in the emulated network to provision every switch with a full functional control plane.

## Additions to Containernet

- class DockerRouter: defined in mininet/node.py, provides the abstraction of an emulated switch hosted by a Docker container.
- class DockerP4Router: defined in mininet/node.py, provides the abstraction of a containerized emulated switch that uses [P4-BMv2](https://github.com/p4lang/behavioral-model.git).
- class DockerPingHost: defined in mininet/node.py, provides the abstraction of a containerized host that runs pingmesh to monitor the network.
- class Subnet: defined in mininet/config.py, provides the abstraction of a subnet and is mainly used to allocate IP addresses from a subnet
- class NodeList: defined in mininet/config.py, provides the abstraction of the topology of an emulated network and can generate the a file that stores the topology information.

## Emulated Network Setup
### Steps
1. create containers for every host and switches
2. add routing configurations
3. add links between hosts and switches
4. run experiment-specific setup commands
5. run the start function of every hosts and switches

### Examples
1. mininet/demo/generic_topo_bgp.py: the major setup used for testing diagnosis system and fault injection campaign
2. mininet/demo/vxlan_p4_demo.py: the major setup used for testing VXLAN network
