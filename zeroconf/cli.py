import argparse
import re
import os

from .actions import discover_hosts, connected_peers, peer_probe


def check_ipv4_address(ips):
    """Checks whether a list of IP contains valid
    IPv4 addresses
    """
    ipv4 = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    tmp = [ipv4.match(x) for x in ips]
    return all(tmp)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timeout', help='seconds to wait for replies', type=int, default=5)
    parser.add_argument('-i', '--interfaces', help='limits the discovery on some\
                        interfaces (it accepts for now only IPv4 addresses\
                        separated by space)', nargs='*', default=None)
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='count')
    parser.add_argument('action', help='command to execute', choices=['discover', 'probe'], default='discover', nargs='?')

    try:
        args = parser.parse_args()
    except:
        return os.EX_USAGE

    if args.interfaces:
        if not check_ipv4_address(args.interfaces):
            print("IP address not valid")
            return os.EX_USAGE

    hosts = discover_hosts(timeout=args.timeout, interfaces=args.interfaces)
    for host in hosts:
        print('discovered host: %s' % (host))

    peers = connected_peers()
    for peer in peers:
        print('connected peer: %s' % (peer))

    if args.action == 'probe':
        for host in hosts:
            if host not in peers:
                # TODO: resolve all IPs to hostnames
                peer_probe(host)

    return os.EX_OK
