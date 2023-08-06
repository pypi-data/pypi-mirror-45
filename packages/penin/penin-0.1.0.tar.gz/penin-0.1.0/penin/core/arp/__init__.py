"""Support for creating ARP requests and manipulations."""

from scapy.all import srp, Ether, ARP, conf


def create_arp_ping(destination):
    """Create an ARP ping."""
    conf.verb = 0
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=destination),
                  timeout=2)

    print("MAC, IP")
    for snd, rcv in ans:
        print(rcv.sprintf(r"%Ether.src%,%ARP.psrc%"))


    # # The fastest way to discover hosts on a local ethernet network is to use the ARP Ping method:
    # ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=host), timeout=2)
    #
    # # Answers can be reviewed with the following command:
    # ans.summary(lambda (s, r): r.sprintf("%Ether.src% %ARP.psrc%"))

    # if iface:
    #     conf.iface = iface
    #
    # res, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2)
    #
    # for _, pkt in res:
    #     if verbose:
    #         print(pkt.show())
    #     else:
    #         print(pkt.summary())

# 	cmd_arp_ping.py 	stupid setup.py typo (snamp vs snmp) 	3 months ago
#	cmd_arp_poison.py 	config management and fernet encryption 	9 months ago
#	cmd_arp_sniff.py 	config management and fernet encryption 	9 months ago