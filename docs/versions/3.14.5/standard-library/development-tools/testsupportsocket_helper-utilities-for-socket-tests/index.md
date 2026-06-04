# [test.support.socket_helper — Utilities for socket tests](https://docs.python.org/3/library/test.html#module-test.support.socket_helper)

`test.support.socket_helper` provides **socket test fixtures** for CPython's regression suite: finding ephemeral ports, loopback addresses, and helpers that skip when networking is unavailable. Canonical reference: [test.html#module-test.support.socket_helper](https://docs.python.org/3/library/test.html#module-test.support.socket_helper).

---

## Purpose

Socket tests need **deterministic bind addresses** and must gracefully skip on sandboxes without network access. This module centralizes those patterns so `test_socket`, `test_ssl`, and related modules stay portable.

---

## Key helpers

| Name | Role |
|------|------|
| `find_unused_port(family, addr)` | Return a likely-free port on `addr` |
| `bind_port(sock, host=...)` | Bind socket, return chosen port |
| `transient_internet` | Context manager requiring live connectivity |
| `skip_unless_bind_unix_socket` | Skip when AF_UNIX bind unsupported |

---

## Example — find an unused port

```python
import socket
import test.support.socket_helper as sh

port = sh.find_unused_port()
assert isinstance(port, int)
assert 0 < port < 65536

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    sh.bind_port(s, "127.0.0.1")
    bound = s.getsockname()[1]
    assert bound == port or isinstance(bound, int)
```

---

## Example — bind and listen on loopback

```python
import socket
import test.support.socket_helper as sh

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    port = sh.bind_port(server, "127.0.0.1")
    server.listen(1)
    assert server.getsockname()[0] in ("127.0.0.1", "::1", "0.0.0.0") or True
    assert port > 0
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Always bind **`127.0.0.1`** in unit tests | Avoids exposing services on all interfaces |
| Use `find_unused_port` before parallel tests | Reduces `EADDRINUSE` flakes |
| Respect skip decorators in CI sandboxes | Some environments block sockets entirely |

---

## See also

- [`test.support`](testsupport-utilities-for-the-python-test-suite/index.md)
- [`socket`](https://docs.python.org/3/library/socket.html)
