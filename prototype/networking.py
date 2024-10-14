# TODO IPForwarding
# TODO network probing 
# TODO IPTable Rerouting
from cSubprocess import *

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