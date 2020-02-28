NetworkHelper ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/netmiko.svg)
=======

Library to simplify Telnet connections to network devices

## Installation

To install NetworkHelper, simply us pip:

NetworkHelper has the following requirements
- [netmiko](https://github.com/ktbyers/netmiko)
- [pyvmomi](https://github.com/vmware/pyvmomi)
- [flask](https://github.com/pallets/flask)
- [requests](https://github.com/psf/requests)

## Description

The program consists of two parts, this is the main part and the python script for checking VM

### Main part - control cisco devices
There are a number of automated management functions:
1) Reset - This function completely automates the reset of cisco devices answers all standard questions and handle the error of not launching the firmware (Rommon)
2) Config - This function fully automates the configuration of cisco devices using configuration files.
Sample configuration file (Don’t use enable it is already built in when connecting)
```
conf t
enable password cisco
line vty 0 4
password cisco
transport input telnet
int vlan 1
ip add 192.168.254.10 255.255.255.0
no sh
end
wr
```
