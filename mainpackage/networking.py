from cSubprocess import *
import re

# Input: Boolean to define ip_forwarding
def set_ip_forwarding(bool: bool):
    cat_cmd = "cat /proc/sys/net/ipv4/ip_forward"
    cat_rsp = clean_subprocess(cat_cmd, 0)

    if bool is True and not int(cat_rsp) == 1:
        clean_subprocess("sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'", -1)
        return 1
    elif bool is False and not int(cat_rsp) == 0:
        clean_subprocess("sudo bash -c 'echo 0 > /proc/sys/net/ipv4/ip_forward'", -1)
        return 1
    else:
        return 0
    
def get_ip_forwarding():
    cat_cmd = "cat /proc/sys/net/ipv4/ip_forward"
    cat_rsp = clean_subprocess(cat_cmd, 0)
    return cat_rsp

# Input: Boolean to define whether to set or unset the queueing iptables rule
def queue_iptables_rule(bool: bool, port: int):
    command = f"sudo iptables -t nat -L -n -v | grep -E 'REDIRECT.*ports {port}'"
    rsp = clean_subprocess(command, 0)
    ruleExists = False
    if rsp is not None:
        ruleExists = re.search(f"REDIRECT.*{port}", rsp) is not None

    if bool is True and not ruleExists:
        command = f"sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port {port}"
        return clean_subprocess(command, -1)
    
    elif bool is False and ruleExists:
        command = f"sudo iptables -t nat -D PREROUTING -p tcp --dport 80 -j REDIRECT --to-port {port}"
        return clean_subprocess(command, -1)

def get_iptables_rules():
    command = "sudo iptables -t nat -L -n -v"
    rsp = clean_subprocess(command)
    return rsp

# Input: An address within a subnetwork (e.g. gateway ipaddress)
# Description: Perform a ping scan on the subnet associated with the ipaddress
def ping_scan(gateway: str):
    command = f"nmap -sn {gateway}/24"
    return clean_subprocess(command, 1)

def ping_address(ip_address: str):
    command = 'ping -c 1 ' + ip_address
    clean_subprocess(command, -1)

def get_default_gateway_ip():
    command = "netstat -rn | awk '/^0.0.0.0/ {print $2}'"
    return clean_subprocess(command, 0)

def get_mac_address(ip_address: str):
    ping_address(ip_address)
    command = 'arp -a | grep ' + ip_address + ' | cut -d " " -f 4'
    return clean_subprocess(command, 0)

def get_ip_address():
    command = "ifconfig eth0 | grep 'inet ' | awk '{print $2}'"
    return clean_subprocess(command, 0)