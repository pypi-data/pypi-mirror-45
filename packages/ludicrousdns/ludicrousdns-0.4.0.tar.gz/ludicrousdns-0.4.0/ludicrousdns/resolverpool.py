import os.path
import asyncio
import itertools

from .resolver import Resolver
from .util import read_nameservers_from_file


class ResolverPool:
    """A resolver that spawns a Resolver for each nameserver provided.
    """

    def __init__(self, nameservers=None, detect_wildcard_dns=True):
        if not nameservers:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            nameservers = read_nameservers_from_file(current_dir + "/data/nameservers.txt")

        if detect_wildcard_dns:
            wildcard_responses = {}
        else:
            wildcard_responses = None

        self.loop = asyncio.get_event_loop()
        self._resolvers = []
        for ns in nameservers:
            self._resolvers.append(Resolver(self.loop, ns, wildcard_responses=wildcard_responses))

    async def _resolve_hosts(self, hosts):
        host_iter = iter(hosts)
        resolver_futures = []
        for resolver in self._resolvers:
            resolver_futures.append(resolver.resolve_hosts(host_iter))

        results = await asyncio.gather(*resolver_futures)

        return list(itertools.chain.from_iterable(results))

    def resolve_hosts(self, hosts):
        return self.loop.run_until_complete(self._resolve_hosts(hosts))
