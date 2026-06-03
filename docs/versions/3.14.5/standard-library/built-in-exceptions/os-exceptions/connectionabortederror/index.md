# [ConnectionAbortedError](https://docs.python.org/3/library/exceptions.html#ConnectionAbortedError)

`ConnectionAbortedError` is raised when a connection attempt or established session is aborted by the local stack or the peer. It subclasses [`ConnectionError`](../connectionerror/index.md). Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#ConnectionAbortedError).

---

## Role in the hierarchy

| errno | Exception |
|-------|-----------|
| `ECONNABORTED` | `ConnectionAbortedError` |

```python
import errno

exc = OSError(errno.ECONNABORTED, "Software caused connection abort")
assert isinstance(exc, ConnectionAbortedError)
assert issubclass(ConnectionAbortedError, ConnectionError)
```

---

## When it is raised

Typical causes include TLS handshake failure, firewall RST, or the application closing a socket while data is in flight. Distinct from [`ConnectionResetError`](../connectionreseterror/index.md) (`ECONNRESET`) in errno semantics, though both fall under `except ConnectionError`.

---

## Handling patterns

```python
import errno

def log_connection_errors():
    errors = []
    for exc in (
        ConnectionAbortedError(errno.ECONNABORTED, "aborted"),
        ConnectionResetError(errno.ECONNRESET, "reset"),
    ):
        try:
            raise exc
        except ConnectionError as caught:
            errors.append(type(caught).__name__)
    return errors

assert log_connection_errors() == ["ConnectionAbortedError", "ConnectionResetError"]
```

Use retries only when the abort happened before any side effect; otherwise treat as failed request.

---

## Best practices

- Log remote address and `errno` when available on socket wrappers.
- Combine with timeout configuration so hung handshakes become [`TimeoutError`](../timeouterror/index.md) instead of indefinite waits.
