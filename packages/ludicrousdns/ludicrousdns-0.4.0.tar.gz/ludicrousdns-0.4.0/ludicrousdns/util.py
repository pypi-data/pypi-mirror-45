import asyncio
import re

import aiodns


def read_nameservers_from_file(filename):
    with open(filename) as f:
        return read_nameservers_from_string(f.read())


def read_nameservers_from_string(s):
    nameservers = [re.sub(r'#.*$', '', line).strip() for line in s.splitlines()]
    return [ns for ns in nameservers if ns != '']


async def filter_nameservers_async(nameservers):
    nameservers = list(nameservers)
    existent_domain = "google.com"
    nonexistent_domain = "doesntexist.example.com"

    loop = asyncio.get_event_loop()

    filtered_nameservers = set(nameservers)

    for ns in nameservers:
        test_resolver = aiodns.DNSResolver(loop=loop, nameservers=[ns], timeout=1, tries=1)
        try:
            await test_resolver.query(existent_domain, 'A')
        except aiodns.error.DNSError:
            filtered_nameservers.remove(ns)
            continue

        try:
            await test_resolver.query(nonexistent_domain, 'A')
            filtered_nameservers.remove(ns)
        except aiodns.error.DNSError:
            pass

    return list(filtered_nameservers)


def filter_nameservers(nameservers):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(filter_nameservers_async(nameservers))
