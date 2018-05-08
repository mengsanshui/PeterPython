import argparse
import socket
import sched
import time
import netifaces as ni
import netaddr as na
import nmap
from scapy.all import sr, srp, ARP, Ether
from scapy.layers.inet import IP, ICMP, UDP, TCP


RUN_FREQUENCY = 20
scheduler = sched.scheduler(time.time, time.sleep)

def detect_inactive_hosts(scan_hosts):
    global scheduler
    scheduler.enter(RUN_FREQUENCY, 1, detect_inactive_hosts, (scan_hosts,))
    inactive_hosts = []
    try:
        ans, unans = sr(IP(dst=scan_hosts) / ICMP(), retry=0, timeout=1)
        ans.summary(lambda s, r: r.sprintf("%IP.src% is alive"))
        print("")
        for inactive in unans:
            print("%s is inactive" % inactive.dst)
            inactive_hosts.append(inactive.dst)
        print("Total %d hosts are inactive" % (len(inactive_hosts)))
    except KeyboardInterrupt:
        exit(0)

def inspect_ipv6_support():
    print ("IPV6 support built into Python: %s" %socket.has_ipv6)
    ipv6_addr = {}
    for interface in ni.interfaces():
        all_addresses = ni.ifaddresses(interface)
        print ("Interface %s:" %interface)
        for family,addrs in all_addresses.items():
            fam_name = ni.address_families[family]
            print (' Address family: %s' % fam_name)
            for addr in addrs:
                if fam_name == 'AF_INET6':
                    ipv6_addr[interface] = addr['addr']
                    print (' Address : %s' % addr['addr'])
                nmask = addr.get('netmask', None)
                if nmask:
                    print (' Netmask : %s' % nmask)
                bcast = addr.get('broadcast', None)
                if bcast:
                    print (' Broadcast: %s' % bcast)
    if ipv6_addr:
        print ("Found IPv6 address: %s" %ipv6_addr)
    else:
        print ("No IPv6 interface found!")

def extract_ipv6_info():
    print ("IPv6 support built into Python: %s" %socket.has_ipv6)
    for interface in ni.interfaces():
        all_addresses = ni.ifaddresses(interface)
        print ("Interface %s:" %interface)
        for family,addrs in all_addresses.items():
            fam_name = ni.address_families[family]
            for addr in addrs:
                if fam_name == 'AF_INET6':
                    addr = addr['addr']
                    has_eth_string = addr.split("%eth")
                    if has_eth_string:
                        addr = addr.split("%eth")[0]
                        try:
                            print (" IP Address: %s" % na.IPNetwork(addr))
                            print (" IP Version: %s" % na.IPNetwork(addr).version)
                            print (" IP Prefix length: %s" % na.IPNetwork(addr).prefixlen)
                            print (" Network: %s" % na.IPNetwork(addr).network)
                            print (" Broadcast: %s" % na.IPNetwork(addr).broadcast)
                        except Exception as e:
                            print ("Skip Non-IPv6 Interface")

if __name__ == "__main__":
    inspect_ipv6_support()
    extract_ipv6_info()
    #scan_hosts = '192.168.6.1-200'
    #scheduler.enter(1, 1, detect_inactive_hosts, (scan_hosts,))
    #scheduler.run()







