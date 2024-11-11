from scapy.all import Ether, TCP, IP, UDP, Raw, wrpcap, send 
from networking import *
#from netfilterqueue import NetfilterQueue

# Input: Routed packet
# Description: Print & accept packets that are being forwarded through the device
def print_packet(pkt):
    # Get packet payload
    scapy_pkt = IP(pkt.get_payload())
    print(scapy_pkt.show())

# Input: Scapy packet capture
# Description: Creates a packet_log.pcap file & a more detailed packet_log.txt file
def writeCapture(capture):
    print("\nSaving capture...")
    wrpcap("packet_log.pcap", capture)

    with open("packet_log.txt", "w") as text_file:
        for i, packet in enumerate(capture):
            text_file.write(f"\n--- Packet {i + 1}: " + packet.summary() + " ---\n")
            text_file.write(packet.show(dump=True))
            text_file.write(f"\n--- Packet {i + 1}: End ---\n")

# Input: Scapy packet capture
# Description: Displays scapy packet capture
def displayCapture(capture):
    for i, packet in enumerate(capture):
        print(f"\n--- Packet {i + 1}: " + packet.summary() + " ---\n")
        print(packet.show())
        print(f"\n--- Packet {i + 1}: End ---\n")

class Packet_Handler:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.pkt_lst = []

    # Input: Scapy Packet
    def add(self, scapy_pkt):
        self.pkt_lst.append(scapy_pkt)
    
    def write_to_file(self):
        with open(self.file_name, 'w') as file:
            # Convert to scapy_packet & write to file
            for i, pkt in enumerate(self.pkt_lst):
                file.write(f"\n--- Packet {i + 1}: " + pkt.summary() + " ---\n")
                file.write(pkt.show(dump=True))
                file.write(f"\n--- Packet {i + 1}: End ---\n")
