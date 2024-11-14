## Guidelines

### General features
- Attention-grabbing
- Why should viewer care?
    - Why is it important?
- What your tool can be used for / what problem is it solving
- Interesting issues that came up
- How your team approached the problem (what worked and what didn't)

### General four steps
- Issue at hand
- Why important?
- How did we proceed/what did we do? ---- Might end here
- What did we learn?

### Overview of pitch
- Two virtual machines and a server
- One attacks the other via ARP impersonation
    - The attacker then starts intercepting traffic to the attacker's own server after connecting securely to the server
    - Attacker prevents security headers from going to server, but forwards the other information
- Attacker returns modified webpage from server to target
    - Page has JavaScript embedded in it to keylog their login page
- Chaos ensues