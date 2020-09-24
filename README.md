# Spoofing

**DISCLAIMER**

All content posted on the repository is for educational and research purposes only. Do not attempt to 
violate the law with anything contained here. Administrators of this server, the authors of this material, 
or anyone else affiliated in any way, are not going to accept responsibility for your actions. Neither 
the creator nor GitHub is not responsible for the comments posted on this repository.

This site contains materials that can be potentially damaging or dangerous. 
If you do not fully understand please LEAVE THIS WEBSITE. Also, be sure to check laws 
in your province/country before accessing repository.

## ARP Spoofing

**arp_spoof.py** captures packets on the local network. Arpspoof redirects packets from the target 
host (or all hosts) on the local network to those intended for another host on the local 
network by spoofing the ARP responses. This is a very effective way to sniff traffic 
on the switch.

If you want to not only disconnect users from the gateway, but also 
replace/sniff packets, then you will need to enable forwarding in ip_forward:

```
echo 1 > /proc/sys/net/ipv4/ip_forward
```

or

```
subprocess.run("iptables --flush", shell=True)
subprocess.run("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)

```
And also configure packet routing via iptables:

```
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -p tcp --destination-port 443 -j REDIRECT --to-port 8080
```

If you want to conduct phishing, the **mitmproxy** utility is best.
You can view the traffic passing through you using the **tcpdump** utility.

When user finish arpspoofing, method "restore" will refresh arp tabl-e/s to the previous values.

**ARP spoof detection**

Additionaly I crated a python-scrypt (arp_spoof_detector) that identifyes if someone spoofing your network.

## DNS Spoofing

A Domain Name System server translates the human-readable domain name (such as google.com) into an 
IP address that is used to make the connection between the server and the client, for instance, 
if a user wants to connect to google.com, the user's machine will automatically send a request 
to the DNS server, saying that I want the IP address of google.com. The server will respond with the c
orresponding IP address of that domain name and the user will then connect normally to the server.

**DNS spoofing**, also referred to as **DNS cache poisoning**, is a form of computer security hacking in 
which corrupt Domain Name System data is introduced into the DNS resolver's cache, causing the 
name server to return an incorrect result record, e.g. an IP address. This results in traffic 
being diverted to the attacker's computer (or any other computer)

Note: In order to be a man-in-the-middle, you need to execute the ARP spoof script, so the victim 
will be sending the DNS requests to your machine first, instead of directly routing them into the Internet.

Now since the attacker is in between, he'll receive that DNS request indicating "what is the 
IP address of google.com", then he'll forward that to the DNS server.

The attacker now received that DNS response that has the real IP address of google.com, what 
he will do now is to change this IP address to a malicious fake IP.

As you may guess, we need to insert an iptables rule, open the linux terminal and type:
```
iptables -I FORWARD -j NFQUEUE --queue-num 0
```

![alt text](https://raw.githubusercontent.com/ramapitecusment/spoofing_scapy/master/images/0.jpg)

![alt text](https://raw.githubusercontent.com/ramapitecusment/spoofing_scapy/master/images/1.jpg)

![alt text](https://raw.githubusercontent.com/ramapitecusment/spoofing_scapy/master/images/2.jpg)