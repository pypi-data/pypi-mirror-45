import asyncio
import itertools
import uuid

import aiodns


class DNSResponse:
    def __init__(self, type_, response):
        self.type = type_
        if type_ in ["A", "AAAA"]:
            self.value = set(h.host for h in response)
        elif type_ == "CNAME":
            self.value = response.cname
        else:
            raise ValueError("Unknown query type")

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.value == other.value


class BaseResolver:
    """Connects to a single nameserver with multiple workers.
    """

    def __init__(self, loop, nameserver, wildcard_responses=None, *, concurrency=10):
        self._concurrency = concurrency
        self._wildcard_responses = wildcard_responses

        self._resolver = aiodns.DNSResolver(loop=loop, nameservers=[nameserver])

    async def resolve_hosts(self, hosts):
        host_iterator = iter(hosts)
        workers = [self._worker(host_iterator) for _ in range(self._concurrency)]

        return itertools.chain.from_iterable(await asyncio.gather(*workers))

    async def _worker(self, host_iter):
        result = []
        for host in host_iter:
            resp = await self._query(host)
            matches_wildcard = await self._matches_wildcard(host, resp)
            if resp and not matches_wildcard:
                result.append((host, resp.value))
        return result

    async def _query(self, name):
        for query_type in ["CNAME", "A", "AAAA"]:
            try:
                resp = await self._lookup_dns_record(name, query_type)
                return DNSResponse(query_type, resp)
            except (aiodns.error.DNSError, UnicodeError):
                continue
        return None

    async def _lookup_dns_record(self, name, query_type):
        return await self._resolver.query(name, query_type)

    async def _matches_wildcard(self, name, resp):
        if self._wildcard_responses is None:
            return False

        parent_domain = name.split(".", 1)[1]
        if parent_domain not in self._wildcard_responses:
            wildcard = str(uuid.uuid4()) + "." + parent_domain
            wildcard_resp = await self._query(wildcard)
            self._wildcard_responses[parent_domain] = wildcard_resp
        else:
            wildcard_resp = self._wildcard_responses[parent_domain]

        return wildcard_resp == resp


class Resolver(BaseResolver):
    """Rate-limited with a simplified token bucket algorithm
    """

    def __init__(self, *args, rate=100, **kwargs):
        super().__init__(*args, **kwargs)
        self._rate = rate
        self._interval = 1/rate
        self._token_queue = asyncio.Queue()

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate
        self._interval = 1/rate

    async def _lookup_dns_record(self, name, query_type):
        await self._token_queue.get()
        return await super()._lookup_dns_record(name, query_type)

    async def _feed_tokens(self):
        while True:
            await self._token_queue.put(0)
            await asyncio.sleep(self._interval)

    async def resolve_hosts(self, hosts):
        token_feeder = asyncio.ensure_future(self._feed_tokens())
        try:
            result = await super().resolve_hosts(hosts)
        finally:
            token_feeder.cancel()
        return result
