from cSubprocess import *

# Input: Boolean to define ip_forwarding
def set_ip_forwarding(bool: bool):
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

# Input: Boolean to define whether to set or unset the queueing iptables rule
def queue_iptables_rule(bool: bool):
    if bool is True:
        command = "sudo iptables -I FORWARD -j NFQUEUE --queue-num 1"
        return clean_subprocess(command, -1)
    
    elif bool is False:
        command = "sudo iptables -D FORWARD -j NFQUEUE --queue-num 1"
        return clean_subprocess(command, -1)

def print_iptables_rules():
    command = "sudo iptables -L -v -n"
    return clean_subprocess(command, -1)

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