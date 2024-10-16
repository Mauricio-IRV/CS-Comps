Date: 10/16

# What's working: 
We have an ARP spoofer up and running, successfully getting in the middle of the target and the router. 

# Currently working on: 
The next big step we want to take is modifying the packets as they pass through. Possibly modifying them so that we can get an http response from the server which we pass on to the user.

As well as adding visibility to the packet modification and responses as they're passing between the server, us, and the user.

So we are first figuring out how to view/filter which packets are important to our purposes, then we will figure out how to change them.

# Anything else: 
Ideally we'll touch up some error handling and add some networking methods within the product. Additionally, we'll make the process slightly more streamlined since some preparation, such as manually enabling ipforwarding is currently required but this should not necessarily be necessary for the user to know prior to usage of the cmdline tool.