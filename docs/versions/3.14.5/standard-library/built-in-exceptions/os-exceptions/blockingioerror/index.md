# [BlockingIOError](https://docs.python.org/3/library/exceptions.html#BlockingIOError)

`BlockingIOError` is raised when an operation on a **non-blocking** object would block—for example a socket or file descriptor configured with `O_NONBLOCK`. It corresponds to `EAGAIN`, `EALREADY`, `EWOULDBLOCK`, and `EINPROGRESS`. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#BlockingIOError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md); used heavily in `asyncio`, `selectors`, and manual event loops.
- Adds optional attribute `characters_written` when raised from buffered I/O in the [`io`](https://docs.python.org/3/library/io.html) module.

| errno constant(s) | Situation |
|-------------------|-----------|
| `EAGAIN`, `EWOULDBLOCK` | Operation would block (no data ready). |
| `EALREADY` | Operation already in progress (e.g. connect). |
| `EINPROGRESS` | Non-blocking connect still underway. |

---

## When it is raised

On a non-blocking socket, `recv` with an empty buffer or `send` on a full kernel buffer typically raises `BlockingIOError` instead of waiting. Event loops catch it and register the fd for the next readiness edge.

```python
import errno

exc = OSError(errno.EAGAIN, "Resource temporarily unavailable")
assert isinstance(exc, BlockingIOError)
assert hasattr(BlockingIOError, "characters_written")  # set by buffered io on partial write
```

---

## Handling patterns

```python
import errno

def try_read_nonblocking(recv_fn):
    try:
        return recv_fn()
    except BlockingIOError:
        return None  # register for POLLOUT/POLLIN and retry

def fake_recv():
    raise BlockingIOError(errno.EAGAIN, "try again")

assert try_read_nonblocking(fake_recv) is None
```

In `asyncio`, this is usually handled internally; application coroutines see `await` instead of raw `BlockingIOError`.

---

## Best practices

- Do not treat `BlockingIOError` as a fatal error in non-blocking code paths—it is the backpressure signal.
- Inspect `characters_written` on partial buffered writes before retrying the remainder.
- Keep blocking and non-blocking code paths separate; mixing them causes surprising latency.
