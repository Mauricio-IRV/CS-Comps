from scapy.all import Ether, TCP, Raw, sendp, send

# Return decoded packet raw load
def get_dprl(packet):
    try:
        return packet[Raw].load.decode()
    except:
        pass
    
    return False