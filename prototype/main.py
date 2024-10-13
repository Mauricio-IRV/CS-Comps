from bettercap import run_bettercap
from arpspoof import *

def main():
    arp_spoofer = ArpSpoofer()

    target_ip = input("Target IP: ")
    gateway_ip = arp_spoofer.get_default_gateway_ip()

    arp_spoofer.spoof(gateway_ip, target_ip)

if __name__ == "__main__":
    main()