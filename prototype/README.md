## README for the package

### Overview
ArpDoS is a package that allows you to set up an adversary-in-the-middle (AITM) attack against the device of your choice, implementing:
* ARP spoofing
* packet modification
* SSL stripping
* HTTP downgrading
### Installation Instructions
* To install the project, clone the git repo into a folder and cd into `CS-Comps/prototype/`. Then run the following commands (again, only on Kali):
    * `sudo apt install libnfnetlink-dev libnetfilter-queue-dev`
    * `pip3 install netfilterqueue`
    * `pip3 install requests`
* To start the adversary-in-the-middle attack, run `sudo python3 main.py` on the attacker machine.

> Note: The pyproject.toml is only for the python package build, and is completely irrelevant for anything other than intermittently packaging binaries for the resulting program.