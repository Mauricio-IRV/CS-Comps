# CS-Comps

### Background
This project was developed for CS comps at Carleton College, Fall 2024. More specifically, we are part of the “Building Hacking Tools from Scratch” team. Our primary inspiration for this tool was bettercap.

### The tool
ARP_SSL_Toolkit is a package that allows you to set up an adversary-in-the-middle (AITM) attack against another device, implementing:
* ARP spoofing
* Denial of service
* SSL stripping
* HTTP downgrading

### Installation/setup
* To replicate our testing environment, set up two virtual machines and designate one to be the attacker machine and the other to be the client.
   * You will act as both parties.
   * You could run this on a public network as well, but given the ethical and moral issues of that, please don’t.
* On the attacking machine:  to install the project, clone the git repo into a folder and cd into CS-Comps/prototype/. Then run the following commands:
   * `pip3 install scapy`
   * `pip3 install requests`

### Running instructions
* To start the adversary-in-the-middle attack, run sudo python3 main.py on the attacker machine.
   * You will be prompted to specify the IP of the device you wish to attack. Enter the IP of the VM you designated as “client.”
* Note: to run DOS, 
* On the client machine:  navigate to a website (e.g. github.com) in the browser. Log in, click through pages, etc.
* On the attacking machine:  observe the behavior of the client via the Keylogger.

> Note: The pyproject.toml is only for the python package build, and is completely irrelevant for anything other than intermittently packaging binaries for the resulting program.
