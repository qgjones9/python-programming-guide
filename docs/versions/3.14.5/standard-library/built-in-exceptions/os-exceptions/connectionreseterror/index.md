# [ConnectionResetError](https://docs.python.org/3/library/exceptions.html#ConnectionResetError)

`ConnectionResetError` is raised when the peer resets an established connection—often a RST packet on TCP. It subclasses [`ConnectionError`](../connectionerror/index.md). Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#ConnectionResetError).

---

## Role in the hierarchy

| errno | Exception |
|-------|-----------|
| `ECONNRESET` | `ConnectionResetError` |

```python
import errno

exc = OSError(errno.ECONNRESET, "Connection reset by peer")
assert isinstance(exc, ConnectionResetError)
assert issubclass(ConnectionResetError, ConnectionError)
```

---

## When it is raised

Reading or writing after the remote side crashed, closed abruptly, or middleboxes dropped state. Common in HTTP keep-alive when the server closes idle connections.

---

## Handling patterns

```python
def read_chunk(reader):
    try:
        return reader()
    except ConnectionResetError:
        return b""  # treat as EOF for this demo

class ResetReader:
    def __call__(self):
        raise ConnectionResetError("reset")

assert read_chunk(ResetReader()) == b""
```

Idempotent GET retries may be safe; POST retries need deduplication at the application layer.

---

## Best practices

- Pair with read timeouts so half-open connections do not stall workers forever.
- Count resets in metrics to detect upstream instability.
- Prefer explicit connection pooling with idle timeouts over holding sockets indefinitely.
