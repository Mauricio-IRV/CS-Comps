# CS-Comps

### Background
This project was developed for CS comps at Carleton College, Fall 2024. More specifically, we are part of the “[Building Hacking Tools from Scratch](https://docs.google.com/document/d/e/2PACX-1vSouRo8KV3OQYULsrzRG4ekcRslUbjvLqcGHJjQ8peiBg_xVDK24utqCMxEoJRkYdpKWsjdgJuT5ZX9/pub)" team. Our primary inspiration for this tool was bettercap.

### The tool
ARP_SSL_Toolkit is a package that allows you to set up an adversary-in-the-middle (AITM) attack against another device, implementing:
* ARP spoofing
* Denial of service
* SSL stripping
* HTTPS downgrading

### Installation/setup
* To replicate our testing environment, set up two virtual machines and designate one to be the attacker machine and the other to be the target.
   * You will act as both parties.
   * You could run this on a public network as well, but given the ethical, moral, and legal issues of that, please don’t.
* On the attacking machine:  to install the project, clone the git repo into a folder and cd into CS-Comps/prototype/. Then run the following commands:
   * `pip3 install scapy`
   * `pip3 install requests`

### Running instructions
* To start the adversary-in-the-middle attack, run `sudo python3 main.py` on the attacker machine.
   * You will be prompted to specify the IP of the device you wish to attack. Enter the IP of the VM you designated as the target.
   * You will then be prompted to provide an attack mode.
       * **dos**: This attack mode is denial of service, which will prevent the client from being able to connect to any outside servers.
       * **ssl-strip**: This attack mode is SSL stripping, which will downgrade the client's connection from HTTPS to HTTP.
* On the client machine:  navigate to a website (e.g. github.com) in the browser. Log in, click through pages, etc. (Make sure that you have not visited the site with an HTTPS connection before. Clearing history and cookies would address this.)
   > Note: As of right now, our implementation is very limited and only works on select sites for SSL-Stripping. As such, for a working test we recommend visiting github.com.
* On the attacking machine:  observe the behavior of the client via the Keylogger.

> Note: The pyproject.toml is only for the python package build, and is completely irrelevant for anything other than intermittently packaging binaries for the resulting program.

### Redirects

For an overview of our project refer to [Unveiling the Intricacies of an AITM Attack](https://www.cs.carleton.edu/cs_comps/2425/security/mreyes-tthea-bezra/)

For acknowledgements and a brief overview of some of the references used refer to [Resources](https://github.com/Mauricio-IRV/CS-Comps/blob/main/notes/resources.md)