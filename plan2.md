
#### A short description of the project. 
- SSL Stripping
- HTTPS spoofing
- Man-in-the-middle (different types of attacks)
- Building a command-line tool to implement the attacks
- ```bettercap```, ```nmap``` and ```sslstrip``` (tools for examples)

We aim to better understand the process of downgrading HTTPS connections through certain methods such as ARP address spoofing and SSL stripping. To do that, we are using a tool called bettercap to serve as the basis for our own implementation of a submodule that achieves part of this attack.

#### A short list of learning goals--what do you want to end up understanding that you don't understand yet?
- Everything
- Network security & vulnerabilities
- Command line tool implementation
- How to combine multiple programming languages into one tool.

#### A description of your project's architecture. This could be just a diagram of your expected code organization, but it could also include things like the setup of a target server, the data you're going to need for testing, a build system (e.g., Makefile or something similar), etc.
The architecture consists as follows: A target machine (VM) sends requests to an external server/domain (real life). An attacking machine (also VM) will intercept that data with bettercap using our submodules.

#### A list of feature goals.
- A small number of submodules that bettercap will end up using as its main attacking features.
- Command-line compatibility

#### A testing and benchmarking plan.
- Ensuring compatibility with bettercap as we build the modules.
- Returning captured traffic in the state that it was sent (expected responses)
- Making sure our code is efficient enough (Cython build).

#### A list of things one or more of you are worried about. This could be stuff you don't understand yet, things you think might take too long, etc.
- One worry, is trying to make sure that no one falls behind learning wise, for example, making sure that everyone gets exposure to coding, and researching.
- Additionally, there's the fear of, what if it doesn't work.

#### A brief explanation of how you're going to communicate and when you're going to meet to work together.
- Communication consists 3 in class weekly meetings, and 1 weekly meeting outside of class per week.
- Additionally, we will have at least 2 check ins on our progress sundays and wednesdays, as well as organization all throughout

#### A brief explanation of how you're going to ensure that all team members contribute substantially to the end product. (It is shockingly easy for one team member to ride the wave of the rest of the team's work, and end up with no contributions to show for themselves, and even less understanding of the project as a whole. Let's make sure this doesn't happen.)
- In order to to give everyone the ability to contribute all throughout the project we plan on implementing a rotational schedule, where we pass along 
our work. One person researches, one person starts codes, and one person does doing a little bit of both and then it's passed along to the next person 
thereby also promoting collaboration by making sure the next person understands what the previous person did, as well as communicating the next steps.

#### A list of development goals--what features do you want your software to have by the end of the project? you can label some of items "stretch goals"
- Using group-implemented modules to run attacks
- Fast and efficient (main goal)
- Cross-platform and diversity of targets

#### A discussion of how you will test (for correctness) and benchmark (for performance) your tool
- Checking return values of attacks against materials hosted on target site
- Percentage of successful attacks against varying levels of security
- Ability to discard non-viable points of attack
- Performance/output compared to existing tools

#### A more detailed schedule of development than you wrote last week. In addition to a list of development steps and proposed deadlines, you should feel free to annotate items that feel uncertain at this moment.
- Week 3 - Using existing tools (seeing how each tool works) and narrowing down to two or three attacks.

- Week 4 - Pick a bettercap module to implement and start implementing it.
  - Monday: Pick module to implement and figure out best platform and language to write tool in.
  - Wednesday Research implementation and structure, and start implementation.
  - Friday: Continue implementation of module.

- Week 5 -  Linking module
  - Monday: Research how to link custom modules to bettercap and start creating a link for our written module.
  - Wednesday: Debug and stabilize module within bettercap.
  - Friday: Test module for expected responses and begin research on next steps, including implementing necessary network features (tentative).

- Week 6 - Further network tool research (if necessary) and potential poster outlining.
  - Monday: Netprobe implementation.
  - Wednesday: Netsniff implementation.
  - Friday: Testing of implementations and start organization of benchmarks.
  
- Week 7 - Testing and benchmarking (maybe more poster stuff).
  - Monday: Begin general tests and continue research of benchmarking
  - Wednesday: Finish general tests and start benchmarking
  - Friday: Finish benchmarking and wrap all code up in a nice little bow
   
- Week 8 - Final testing and presentation rehearsal (definitely more poster stuff).

[Links & Resources](resources)