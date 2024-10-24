# TODO network probing 
# TODO IPTable Rerouting
from cSubprocess import *
import socket

def set_ip_forwarding(bool):
    cat_cmd = "cat /proc/sys/net/ipv4/ip_forward"
    cat_rsp = clean_subprocess(cat_cmd, 0)

    if bool is True and not int(cat_rsp) == 1:
        clean_subprocess("bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'", -1)
        return 1
    elif bool is False and not int(cat_rsp) == 0:
        clean_subprocess("bash -c 'echo 0 > /proc/sys/net/ipv4/ip_forward'", -1)
        return 1
    else:
        return 0

def get_default_gateway_ip():
    command = "netstat -rn | awk '/^0.0.0.0/ {print $2}'"
    return clean_subprocess(command, 0)

def ping_address(ip_address):
    command = 'ping -c 1 ' + ip_address
    clean_subprocess(command, -1)

def get_mac_address(ip_address):
    ping_address(ip_address)
    command = 'arp -a | grep ' + ip_address + ' | cut -d " " -f 4'
    return clean_subprocess(command, 0)

def get_ip_address():
    command = "ifconfig eth0 | grep 'inet ' | awk '{print $2}'"
    return clean_subprocess(command, 0)