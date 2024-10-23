import scapy.all as scapy

def writeCapture(capture):
    scapy.wrpcap("packet_log.pcap", capture)

    with open("packet_log.txt", "w") as text_file:
        for i, packet in enumerate(capture):
            text_file.write(f"\n--- Packet {i + 1}: " + packet.summary() + " ---\n")
            text_file.write(packet.show(dump=True))
            text_file.write(f"\n--- Packet {i + 1}: End ---\n")

def displayCapture(capture):
    for i, packet in enumerate(capture):
        print(f"\n--- Packet {i + 1}: " + packet.summary() + " ---\n")
        print(packet.show())
        print(f"\n--- Packet {i + 1}: End ---\n")