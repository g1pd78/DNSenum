#!/usr/bin/env python3

# Dependencies:
# python3-dnspython

import dns.query as dq
import dns.resolver as dr
import dns.zone as dz
import argparse

NS = dr.Resolver()

subdomains = []

def AXFR(nameserver, domain):

	try:
		axfr = dz.from_xfr(dq.xfr(nameserver, domain))

		if axfr:
			print('[!] Zone Transfer from {nameserver}')


			for record in axfr:
				subdomains.append('{}.{}'.format(record.to_text(), domain))


	except Exception as error:
		print(error)
		pass


if __name__ == "__main__":

	# ArgParser - Define usage
    parser = argparse.ArgumentParser(prog="dns-axfr.py", epilog="DNS Zonetransfer Script", usage="dns-axfr.py [options] -d <DOMAIN>", prefix_chars='-', add_help=True)
	
	# Positional Arguments
    parser.add_argument('-d', action='store', metavar='Domain', type=str, help='Target Domain.\tExample: inlanefreight.htb', required=True)
    parser.add_argument('-n', action='store', metavar='Nameserver', type=str, help='Nameservers separated by a comma.\tExample: ns1.inlanefreight.htb,ns2.inlanefreight.htb')
    parser.add_argument('-v', action='version', version='DNS-AXFR - v1.0', help='Prints the version of DNS-AXFR.py')

    # Assign given arguments
    args = parser.parse_args()

    if not args.d:
    	print('[!] You must specify target domain.\n')
    	print(parser.print_help())
    	exit()

    if not args.n:
    	print('[!] You must specify target nameservers.\n')
    	print(parser.print_help())
    	exit()

    domain = args.d
    NS.nameservers = list(args.n.split(","))

    for nameserver in NS.nameservers:
    	AXFR(nameserver, domain)

    if subdomains is not None:
    	print('Subdomains found:\n')
    	for subdomain in subdomains:
    		print('{}'.format(subdomain))
    else:
    	print('No subdomains found')
    	exit()