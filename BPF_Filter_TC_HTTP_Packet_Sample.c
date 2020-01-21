#This is a reference file of eBPF filter with linux 'tc' command 
#See more example within linux/samples/bpf/

SEC("classifier")
static inline int classification(struct __sk_buff *skb) {
	void *data_end = (void *)(long)skb->data_end;
	void *data = (void *)(long)skb->data;
	struct ethhdr *eth = data;

	__u16 h_proto;
	__u64 nh_off = 0;
	nh_off = sizeof(*eth);

	if (data + nh_off > data_end) {
		return TC_ACT_OK;
	}
	if (h_proto == bpf_htons(ETH_P_IP)) {
		if (is_http(skb, nh_off) == 1) {
			trace_printk("There is HTTP Packet!\n");
		}
	}
	return TC_ACT_OK;

}

int is_http(struct __sk_buff *skb, __u64 nh_off) {
	void *data_end = (void *)(long)skb->data_end;
	void *data = (void *)(long)skb->data;
	struct iphdr *iph = data + nh_off;
		if (iph + 1 > data_end) {
			return 0;
		}
		if (iph->protocol != IPPROTO_TCP) {
			return 0;
		}
    
	  __u32 tcp_hlen = 0;
		plength = ip_total_length - ip_hlen - tcp_hlen;
		if (plength >= 7) {
			unsigned long p[7];
			int i = 0;
			for (i = 0; i < 7; i++) {
				p[i] = load_byte(skb, poffset + i);
			}
			
			int *value;
			if ((p[0] == 'H') && (p[1] == 'T') && (p[2] == 'T') && (p[3] == 'P')) {
				return 1;
			}
		}
		return 0;
}


# clang -O2 -target bpf -c classifier.c -o classifier.o
# tc qdisc add dev eth0 handle 0: ingress
# tc filter add dev eth0 ingress bpf obj classifier.o flowid 0:
# tc exec bpf dbg
# tc qdisc del dev eth0 ingress
