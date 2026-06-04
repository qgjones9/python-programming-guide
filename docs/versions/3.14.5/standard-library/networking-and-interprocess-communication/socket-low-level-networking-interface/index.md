# [socket — Low-level networking interface](https://docs.python.org/3/library/socket.html)

The [`socket`](https://docs.python.org/3/library/socket.html) module exposes the **BSD socket API** in an object-oriented form: `socket()` returns a socket whose methods map to `bind`, `listen`, `connect`, `send`, `recv`, and friends. Buffer sizing on receive is automatic. Full address-family tables and platform notes remain on [docs.python.org](https://docs.python.org/3/library/socket.html). **Not available on WASI.**

Related: [`ssl`](ssl-tlsssl-wrapper-for-socket-objects/index.md), [`selectors`](selectors-high-level-io-multiplexing/index.md), [`socketserver`](../internet-protocols-and-support/socketserver-a-framework-for-network-servers/index.md).

---

## Creating sockets — [socket.socket](https://docs.python.org/3/library/socket.html#socket.socket)

| Parameter | Typical values |
|-----------|----------------|
| `family` | `AF_INET`, `AF_INET6`, `AF_UNIX` |
| `type` | `SOCK_STREAM` (TCP), `SOCK_DGRAM` (UDP) |
| `proto` | `0` (default for family/type) |

```python
# Goal: create an IPv4 TCP socket and inspect defaults
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
assert sock.family == socket.AF_INET
assert sock.type == socket.SOCK_STREAM
sock.close()
```

---

## Addresses — [Socket families](https://docs.python.org/3/library/socket.html#socket-families)

| Family | Address shape | Notes |
|--------|---------------|-------|
| `AF_INET` | `(host, port)` | `host` is hostname or dotted IPv4; `''` = `INADDR_ANY` |
| `AF_INET6` | `(host, port, flow, scope)` | `flow`/`scope` often `0` |
| `AF_UNIX` | path string or bytes | Abstract Linux namespaces use leading `\0` bytes |

```python
# Goal: bind to an ephemeral port on localhost
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 0))
port = sock.getsockname()[1]
assert port > 0
sock.close()
```

---

## Socket objects — [Socket Objects](https://docs.python.org/3/library/socket.html#socket-objects)

| Method | Role |
|--------|------|
| `bind(address)` | Assign local endpoint |
| `listen(backlog)` | Queue incoming connections (TCP) |
| `accept()` | Accept one connection; returns `(conn, addr)` |
| `connect(address)` | Client connect |
| `send` / `sendall` | Send bytes (all or raise) |
| `recv(bufsize)` | Receive up to bufsize bytes |
| `setblocking(False)` | Non-blocking mode |
| `setsockopt(level, optname, value)` | `SO_REUSEADDR`, `TCP_NODELAY`, etc. |
| `close()` | Release descriptor |

```python
# Goal: TCP echo on loopback without blocking forever
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 0))
server.listen(1)
host, port = server.getsockname()

client = socket.create_connection((host, port))
conn, addr = server.accept()
client.sendall(b"hi")
assert conn.recv(2) == b"hi"
conn.sendall(b"ok")
assert client.recv(2) == b"ok"
client.close()
conn.close()
server.close()
```

---

## UDP — datagram sockets

```python
# Goal: UDP sendto/recvfrom round-trip
import socket

rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rx.bind(("127.0.0.1", 0))
addr = rx.getsockname()
tx.sendto(b"pkt", addr)
data, sender = rx.recvfrom(8)
assert data == b"pkt"
rx.close()
tx.close()
```

---

## Timeouts — [Notes on socket timeouts](https://docs.python.org/3/library/socket.html#notes-on-socket-timeouts)

`settimeout(seconds)` applies to blocking operations; `None` restores blocking mode. A timeout of `0.0` is non-blocking.

```python
# Goal: settimeout controls blocking socket timeout value
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(1.5)
assert sock.gettimeout() == 1.5
sock.settimeout(None)
assert sock.gettimeout() is None
sock.close()
```

---

## Helper functions — [Module contents](https://docs.python.org/3/library/socket.html#module-contents)

| Function | Role |
|----------|------|
| `create_connection(address)` | Client TCP with optional source binding |
| `getaddrinfo(host, port, ...)` | Resolve host/service to candidate addresses |
| `gethostbyname(name)` | Legacy IPv4 lookup |
| `inet_pton` / `inet_ntop` | Binary ↔ presentation for IP addresses |

```python
# Goal: resolve localhost for stream sockets
import socket

infos = socket.getaddrinfo("localhost", 80, type=socket.SOCK_STREAM)
assert any(fam in (socket.AF_INET, socket.AF_INET6) for fam, *_ in infos)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`sendall`** for complete sends | `send` may transfer partial buffers |
| Set **`SO_REUSEADDR`** on servers in dev | Faster restart after `TIME_WAIT` |
| Prefer **`create_connection`** for clients | Tries multiple addresses from `getaddrinfo` |
| Use **`with socket.socket(...) as s:`** (3.12+) or explicit `close()` | Avoid fd leaks |
| Check **`recv` returning `b''`** | Peer closed connection (TCP) |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Assuming `send` sent everything | Loop or use `sendall` |
| Mixing `str` and `bytes` on wire | Encode/decode explicitly |
| `AF_INET` broadcast host `'<broadcast>'` | Not valid for IPv6 programs |
| Platform-specific `AF_*` constants | Guard with `hasattr(socket, "AF_...")` |

---

## Exceptions

`socket.error` is an alias of `OSError` since 3.3. Timeouts surface as `TimeoutError` or `socket.timeout` depending on context.
