# [ConnectionRefusedError](https://docs.python.org/3/library/exceptions.html#ConnectionRefusedError)

`ConnectionRefusedError` is raised when a TCP connect (or similar) reaches a host but no process accepts on the target port—classic “connection refused.” It subclasses [`ConnectionError`](../connectionerror/index.md). Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#ConnectionRefusedError).

---

## Role in the hierarchy

| errno | Exception |
|-------|-----------|
| `ECONNREFUSED` | `ConnectionRefusedError` |

```python
import errno

exc = OSError(errno.ECONNREFUSED, "Connection refused", ("127.0.0.1", 65534))
assert isinstance(exc, ConnectionRefusedError)
assert exc.errno == errno.ECONNREFUSED
```

---

## When it is raised

Nothing is listening on the port, a firewall rejects actively, or the service is bound to another interface. Unlike [`TimeoutError`](../timeouterror/index.md), the kernel responds immediately with refusal.

---

## Handling patterns

```python
import errno

def describe_connect_failure():
    try:
        raise ConnectionRefusedError(
            errno.ECONNREFUSED, "Connection refused", ("127.0.0.1", 8080)
        )
    except ConnectionRefusedError:
        return "service unavailable"
    return "ok"

assert describe_connect_failure() == "service unavailable"
```

Health checks and client SDKs often map this to retry-with-backoff only when a dependency is expected to start (container boot), not for permanent misconfiguration.

---

## Best practices

- Verify host, port, and firewall rules before adding retry loops.
- Distinguish from DNS/`gaierror` and from `FileNotFoundError` on Unix domain socket paths.
- Surface clear messages: “nothing listening on host:port” aids operators faster than generic `OSError`.
