import argparse
import sys

from . import ResolverPool
from . import read_nameservers_from_string
from . import filter_nameservers


def resolve(args, subparser):
    if sys.stdin.isatty() and args.domains == sys.stdin:
        subparser.print_help()
        sys.exit(1)

    if args.nameservers:
        with args.nameservers:
            nameservers = read_nameservers_from_string(args.nameservers.read())
    else:
        nameservers = None

    if args.no_wildcard_detection:
        detect_wildcard = False
    else:
        detect_wildcard = True

    resolver = ResolverPool(nameservers=nameservers, detect_wildcard_dns=detect_wildcard)

    domains = map(str.strip, args.domains)

    for name, result in resolver.resolve_hosts(domains):
        print("{} => {}".format(name, result))


def do_filter_nameservers(args, subparser):
    if sys.stdin.isatty() and args.nameservers == sys.stdin:
        subparser.print_help()
        sys.exit(1)

    nameservers = map(str.strip, args.nameservers)
    for ns in filter_nameservers(nameservers):
        print(ns)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    resolve_parser = subparsers.add_parser("resolve", help="Resolve domains")

    resolve_parser.add_argument("--no-wildcard-detection", action='store_true',
                                help="Do not detect wildcard DNS")
    resolve_parser.add_argument("-n", "--nameservers", type=argparse.FileType('r'),
                                help="File containing nameservers to connect to")
    resolve_parser.add_argument("-d", "--domains", type=argparse.FileType('r'),
                                help="File containing domains to resolve (defaults to stdin)",
                                default=sys.stdin)
    resolve_parser.set_defaults(func=resolve, subparser=resolve_parser)

    filter_help = "Takes a list of nameservers and outputs those that seem sane"
    filter_parser = subparsers.add_parser("filter-nameservers",
                                          help=filter_help)
    filter_parser.add_argument("-n", "--nameservers", type=argparse.FileType('r'),
                               help="File containing nameservers to test (defaults to stdin)",
                               default=sys.stdin)
    filter_parser.set_defaults(func=do_filter_nameservers, subparser=filter_parser)

    args = parser.parse_args()

    if 'func' not in args:
        parser.print_help()
        sys.exit(1)

    args.func(args, args.subparser)
