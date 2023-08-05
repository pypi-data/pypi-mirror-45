# ludicrousdns
[![pipeline status](https://gitlab.com/sheddow/ludicrousdns/badges/master/pipeline.svg)](https://gitlab.com/sheddow/ludicrousdns/commits/master) [![coverage report](https://gitlab.com/sheddow/ludicrousdns/badges/master/coverage.svg)](https://gitlab.com/sheddow/ludicrousdns/commits/master)

Ludicrously speedy, infectious with the async. `ludicrousdns` is designed to be a cleaner, more accurate and more rate-limited version of [massdns](https://github.com/blechschmidt/massdns). 

## Installation
```
pip install ludicrousdns
```

## Usage
`ludicrousdns` can be used both as a library and a binary:
```python
from ludicrousdns import ResolverPool
r = ResolverPool()
r.resolve_hosts(["example.com", "google.com"])
```
or
```shell
echo -e "example.com\ngoogle.com" > hosts.txt
ludicrousdns resolve -d hosts.txt
```
or simply
```shell
echo -e "example.com\ngoogle.com" | ludicrousdns resolve
```

## Features
- Rate-limited
- Detects wildcard DNS
- Ludicrously speedy

## TODO
- Add benchmark to measure CPU- and network usage
- Add benchmark to measure overall speed (use randomized subdomains to avoid effects of caching)
- Add timeout to connections, for example with [async_timeout](https://github.com/aio-libs/async-timeout)
- Add option to adjust rate-limiting
