# [ipaddress — IPv4/IPv6 manipulation library](https://docs.python.org/3/library/ipaddress.html)

[`ipaddress`](https://docs.python.org/3/library/ipaddress.html) models **IPv4/IPv6 addresses, networks, and interfaces** with parsing, containment tests, CIDR math, and compressed string formatting—without calling the OS network stack. Reference: [ipaddress](https://docs.python.org/3/library/ipaddress.html).

---

## Core types

| Type | Example |
|------|---------|
| `ipaddress.IPv4Address('192.0.2.1')` | Single host |
| `ipaddress.IPv6Address('2001:db8::1')` | IPv6 host |
| `ipaddress.IPv4Network('192.0.2.0/24')` | Network block |
| `ipaddress.IPv6Network('2001:db8::/32')` | IPv6 prefix |
| `ipaddress.ip_network(..., strict=False)` | Accept host bits set (host portion ignored) |

---

## Common operations — [Comparison operators](https://docs.python.org/3/library/ipaddress.html#comparison-operators)

| Operation | Meaning |
|-----------|---------|
| `addr in net` | Host membership |
| `net1.overlaps(net2)` | Shared address space |
| `net.subnets(prefixlen_diff=2)` | Split into smaller nets |
| `net.supernet(new_prefix=...)` | Aggregate |
| `int(addr)`, `addr + 1` | Integer arithmetic |

---

## Example — networks and membership

```python
# Goal: parse CIDR, test membership, iterate hosts
import ipaddress

net = ipaddress.ip_network("192.0.2.0/28")
host = ipaddress.ip_address("192.0.2.5")
assert host in net
assert net.network_address == ipaddress.ip_address("192.0.2.0")
assert net.broadcast_address == ipaddress.ip_address("192.0.2.15")
assert len(list(net.hosts())) == 14

compressed = ipaddress.IPv6Address("2001:0db8:0000:0000:0000:0000:0000:0001")
assert str(compressed) == "2001:db8::1"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use `strict=False` when accepting user CIDR | Normalizes host bits to network address |
| Compare with `==` on address objects | Not raw strings (leading zeros differ) |
| Document **IPv4-mapped IPv6** handling | `IPv6Address.ipv4_mapped` when dual-stack |
