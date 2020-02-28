NetworkHelper ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/netmiko.svg)
=======

Library to simplify Telnet connections to network deviceS.

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
3) Firmware - This function displays the firmware of one (or several) device
4) Register - This function displays the register of one (or several) devices
5) Ports - This function displays the switching table (show cdp neighbors)
6) Clear - This function clears all flash memory except firmware
7) Flashing - This function flashes cisco devices using firmware from the folder, finding matches in name of the first part. Example "c2801-adventerprisek9_ivs-mz.151-4.M12a.bin" the search will occur by coincidence "c2801". Used TFTP server connected to the topology
8)There is also device management using checkbox and their grouping using the SETTINGS function.

### Part Two - Checking VMware
There are a number of checks:
1)Checking power on of a virtual machine
2)Checking Installed VMTools
3)Checking installed programs
Windows: WinSDP, Java
Linux: tcpdump, net-tools, lynx, dnsutils, ftp, lftp, sshpass, curl, open-vm-tools
