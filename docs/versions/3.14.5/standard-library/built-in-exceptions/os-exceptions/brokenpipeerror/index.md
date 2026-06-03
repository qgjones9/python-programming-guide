# [BrokenPipeError](https://docs.python.org/3/library/exceptions.html#BrokenPipeError)

`BrokenPipeError` is raised when writing to a pipe or socket whose read end has been closed, or when the socket has been shut down for writing. It is a subclass of [`ConnectionError`](../connectionerror/index.md). Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#BrokenPipeError).

---

## Role in the hierarchy

- Subclass of [`ConnectionError`](../connectionerror/index.md) → [`OSError`](../../concrete-exceptions/oserror/index.md).
- Familiar from shell pipelines when the consumer exits early (`head` closes while `producer` still writes).

| errno constant | Meaning |
|----------------|---------|
| `EPIPE` | Broken pipe on write. |
| `ESHUTDOWN` | Socket shut down for writing. |

---

## When it is raised

Writing to a closed socket, a subprocess pipe after the child exits, or ignoring `SIGPIPE` policy on POSIX can surface `BrokenPipeError` instead of process termination.

```python
import errno

exc = OSError(errno.EPIPE, "Broken pipe")
assert isinstance(exc, BrokenPipeError)
assert issubclass(BrokenPipeError, ConnectionError)
```

---

## Handling patterns

Treat as a normal shutdown signal in servers when the client disconnects; avoid logging at ERROR unless unexpected.

```python
import errno

def send_all(send_fn, data):
    try:
        send_fn(data)
        return True
    except BrokenPipeError:
        return False  # peer gone

def failing_send(_):
    raise BrokenPipeError(errno.EPIPE, "Broken pipe")

assert send_all(failing_send, b"data") is False
```

For subprocess stdout, catch `BrokenPipeError` when the reader stops early so the child is not left blocked on a full pipe buffer.

---

## Best practices

- In long-running daemons, downgrade expected client disconnects to debug-level logs.
- Do not retry blind writes after `BrokenPipeError`; reopen the connection or exit the worker.
- On Unix, CPython often converts SIGPIPE into this exception for socket operations.
