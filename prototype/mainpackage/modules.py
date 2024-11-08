from scapy.all import Ether, TCP, IP, UDP, Raw, wrpcap, sendp, send
from scapy.layers.http import *
from netfilterqueue import NetfilterQueue

from networking import *
from export import *
import socket

orig_dsts = {}

def pkt_sniffer(pkt, target_ip):
    try:
        if IP in pkt and TCP in pkt and pkt[IP].src == target_ip:
            # Store dst ip as key and dst host as value
            key = pkt[IP].dst
            dst_host = socket.gethostbyaddr(pkt[IP].dst)[0]
            orig_dsts[key] = dst_host
    except:
        pass


def print_resp(resp, verbose):
    print("\nResponse Headers:")
    for header, value in resp.headers.items():
        print(f"{header}: {value}")
        
    if verbose:
        print("\nContent:")
        print(resp.content)

# Input: A Decoded Scapy Packet Payload
def get_host(payload):
    payload_lines = payload.splitlines()
    
    host = None

    for line in payload_lines:
        if line.lower().startswith("host:"):
            host = line.split(":")[1].strip()
            break
    
    return host

# Input: Routed packet
# Description: Deny service by dropping packets on route
def dos(pkt):
    print("Packet dropped: ", pkt)
    pkt.drop()
