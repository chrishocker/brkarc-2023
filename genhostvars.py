#!/usr/bin/env python3

import sys
import yaml
import ipaddress
import re

# ./genhostvars.py {{ hostname }} {{ eni_id }} {{ vpc_cidr }} {{ rtb_id_default }} {{ private_ip }} {{ subnet_cidr }} {{ route_cidr }}

hostname = sys.argv[1]
eni_id = sys.argv[2]
vpc_cidr_in = sys.argv[3]
rtb_id_default = sys.argv[4]
private_ip = sys.argv[5]
subnet_cidr_in = sys.argv[6]
route_cidr = sys.argv[7]

vpc_cidr = ipaddress.ip_network(vpc_cidr_in)
dns = vpc_cidr[2]
vpc_network = vpc_cidr[0]
vpc_mask = vpc_cidr.netmask
subnet_cidr = ipaddress.ip_network(subnet_cidr_in)
igw_address = subnet_cidr[1]
subnet_mask = subnet_cidr.netmask

if re.search('csr_a', hostname):
    tunnel_address = vpc_cidr[(99*256) + 1]
    peer_csr = subnet_cidr[-3]
elif re.search('csr_b', hostname):
    tunnel_address = vpc_cidr[(99*256) + 2]
    peer_csr = subnet_cidr[-2]

hostvars = {
    'dns' : str(dns),
    'igw' : str(igw_address),
    'vpc_prefix' : str(vpc_network),
    'vpc_mask' : str(vpc_mask),
    'subnet_mask' : str(subnet_mask),
    'peer_csr' : str(peer_csr),
    'eni' : eni_id,
    'rtb' : rtb_id_default,
    'cidr' : route_cidr,
    'private_ip' : private_ip,
    'tunnel_address' : str(tunnel_address)
}

with open('./host_vars/' + hostname, 'w') as outfile:
    outfile.write(yaml.dump(hostvars, default_flow_style=False))
