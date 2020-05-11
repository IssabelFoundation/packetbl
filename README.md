# [PacketBL](https://www.issabel.org)
This software is a fork from Zevenet version of the original Packetbl software developen by Russell Miller.

The goal of this program is to connect netfilter with user space to check if a origin IP is malicious using  
a DNS server as a realtime database.  Packetbl uses netfilter-queue feature to receive a packet from netfilter 
to user space.

Packetbl will reject or will drop a connection if a DNS server resolves the queried client IP. So the DNS 
server will be used as a service of dynamic black lists. Those black lists are supported by specialist 
security providers, you can find some of them here: https://en.wikipedia.org/wiki/Comparison_of_DNS_blacklists

Our exclusive VoIP blacklist is:

- rbl.issabel.guru

# RBL
RBL or DNSBL is a tech that does DNS queries about a source IP to determinate if the IP is blacklisted. If the source IP is resolved by a remote DNS serve, the malicious packet can be dropped, rejected or logged to mitigate a cyber-attack.
RBL technology is typically used to mitigate email threats as spam or phishing. But it is useful for another services as FTP, SIP, SSH, web...


# New features
- Multi-thread, Packetbl will create a thread for each checking packet.
- Direct DNS queries, Packetbl can use a determinate DNS server to resolve a specific domain.
- Fail-over, This option is available since Linux 3.6 and allows to accept packet instead of dropping them when the netfilter queue is full.
- Queuesize, this parameter allows to set Netfilter queue size.
- Select a config file, it is possible to choose a packetbl config file with the "-f" command line option.


