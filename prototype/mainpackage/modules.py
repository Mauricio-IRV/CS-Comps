from scapy.all import Ether, TCP, IP, UDP, Raw, wrpcap, sendp, send
from scapy.layers.http import *
from netfilterqueue import NetfilterQueue
import socket
import re
import requests

from networking import *
from export import *

# Receive all of the packets from the client

# send own https request to the server
# The request IP should be from the AITM

# Receive the packets from the server

# Manipulate the server https response
# Strip strict-transfer-protocol
# Replace https links with http

'''
------------------------
SSL STRIP HELPER METHODS
------------------------
'''

def ssl_strip():
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
