# [ConnectionError](https://docs.python.org/3/library/exceptions.html#ConnectionError)

`ConnectionError` is the base class for failures on connected streams—sockets, pipes, and similar endpoints when the peer closes, resets, or refuses communication. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#ConnectionError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md).
- Parent of four concrete types used in networking and IPC; catching `ConnectionError` handles all of them.

| Subclass | errno (typical) | Situation |
|----------|-----------------|-----------|
| [`BrokenPipeError`](../brokenpipeerror/index.md) | `EPIPE`, `ESHUTDOWN` | Write end closed or shut down for writing. |
| [`ConnectionAbortedError`](../connectionabortederror/index.md) | `ECONNABORTED` | Local or remote abort mid-handshake or session. |
| [`ConnectionRefusedError`](../connectionrefusederror/index.md) | `ECONNREFUSED` | Nothing listening on the target address/port. |
| [`ConnectionResetError`](../connectionreseterror/index.md) | `ECONNRESET` | Peer reset an established connection. |

```python
# Goal: connection failures share ConnectionError as intermediate base
for cls in (BrokenPipeError, ConnectionAbortedError,
            ConnectionRefusedError, ConnectionResetError):
    assert issubclass(cls, ConnectionError)
    assert issubclass(cls, OSError)
```

---

## Handling patterns

Use one broad handler for retryable network glitches, then branch on `type(exc)` or `exc.errno` for metrics and user messages.

```python
import errno

def connect_once(host, port):
    raise ConnectionRefusedError(
        errno.ECONNREFUSED, "Connection refused", (host, port)
    )

def connect_with_label(host, port):
    try:
        connect_once(host, port)
    except ConnectionError as exc:
        return type(exc).__name__
    return "ok"

assert connect_with_label("127.0.0.1", 9) == "ConnectionRefusedError"
```

Order handlers from specific subclass to `ConnectionError` to `OSError` when mixing strategies.

```python
def classify(exc):
    try:
        raise exc
    except ConnectionRefusedError:
        return "refused"
    except ConnectionError:
        return "other connection"
    except OSError:
        return "os"

assert classify(ConnectionResetError()) == "other connection"
assert classify(ConnectionRefusedError()) == "refused"
```

---

## Best practices

- Retry `ConnectionResetError` and transient `BrokenPipeError` only when the protocol is idempotent or you have application-level framing.
- Map `ConnectionRefusedError` to “service down” or “wrong host/port” in user-facing APIs.
- Prefer [`TimeoutError`](../timeouterror/index.md) for syscall-level timeouts; distinguish from `socket.timeout` and `asyncio.TimeoutError` in layered code.

---

## Sections in this repo

Connection-related subclasses:

- [BrokenPipeError](../brokenpipeerror/index.md)
- [ConnectionAbortedError](../connectionabortederror/index.md)
- [ConnectionRefusedError](../connectionrefusederror/index.md)
- [ConnectionResetError](../connectionreseterror/index.md)
