# [TimeoutError](https://docs.python.org/3/library/exceptions.html#TimeoutError)

Built-in `TimeoutError` is raised when a **system-level** function reports `errno.ETIMEDOUT`—for example some socket operations or other syscalls that honor timed waits. It is a subclass of [`OSError`](../../concrete-exceptions/oserror/index.md). Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#TimeoutError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md); see [`ETIMEDOUT`](../index.md#errno--exception-mapping) in the parent OS exceptions page.
- Sibling to connection-oriented types under [`ConnectionError`](../connectionerror/index.md); a hung peer may surface `ETIMEDOUT` rather than `ECONNREFUSED` depending on stack and network path.
- Not the same as executor- or asyncio-level deadline exceptions in all code paths—see the table below.

| errno | Exception |
|-------|-----------|
| `ETIMEDOUT` | `TimeoutError` (built-in, OS-related) |

### Distinguishing OS vs application timeouts

In current CPython releases, `asyncio.TimeoutError`, `concurrent.futures.TimeoutError`, and `socket.timeout` are the **same** built-in `TimeoutError` type. What differs is **how** the object was constructed:

| Signal | Typical source |
|--------|----------------|
| `exc.errno == errno.ETIMEDOUT` | Syscall or socket layer reported `ETIMEDOUT`. |
| `exc.errno is None` with a message | Pure-Python deadline (`Future.result(timeout=…)`, `asyncio.wait_for`, raised manually). |

Older tutorials may still import `concurrent.futures.TimeoutError` under an alias when supporting mixed Python versions.

```python
import errno

exc = OSError(errno.ETIMEDOUT, "Connection timed out")
assert isinstance(exc, TimeoutError)
assert issubclass(TimeoutError, OSError)
assert exc.errno == errno.ETIMEDOUT
```

---

## When it is raised

Blocking connect/read/write with a socket timeout, semaphores or locks with timed acquisition at the OS layer, and other primitives that return `ETIMEDOUT` surface this exception. Pure-Python deadlines (`concurrent.futures` `result(timeout=…)`, `asyncio.wait_for` without an underlying `ETIMEDOUT`) may raise **different** types even though the symptom is “timed out.”

```python
import errno

def demo_etimedout_mapping():
    exc = TimeoutError(errno.ETIMEDOUT, "timed out at system level")
    assert exc.errno == errno.ETIMEDOUT
    assert str(exc)  # human-readable strerror is set

demo_etimedout_mapping()
```

---

## Handling patterns

Catch built-in `TimeoutError` when you own syscall-level I/O; use qualified imports when mixing with futures or legacy socket code.

```python
import errno

def fetch_with_os_timeout(request):
    try:
        return request()
    except TimeoutError as exc:
        return f"timed out: errno={exc.errno}"

def slow():
    raise TimeoutError(errno.ETIMEDOUT, "timed out")

assert "errno=" in fetch_with_os_timeout(slow)
```

Separate retry policy for OS timeouts vs application deadlines keeps logs interpretable.

```python
import errno

def classify_timeout(exc):
    if isinstance(exc, TimeoutError) and exc.errno == errno.ETIMEDOUT:
        return "os"
    if isinstance(exc, TimeoutError):
        return "application"
    return "other"

assert classify_timeout(OSError(errno.ETIMEDOUT, "timed out")) == "os"
assert classify_timeout(TimeoutError("deadline exceeded")) == "application"
```

---

## Best practices

- Classify timeouts with `exc.errno == errno.ETIMEDOUT` rather than `type(exc).__name__` when several layers raise the same built-in class.
- Set socket [`settimeout`](https://docs.python.org/3/library/socket.html#socket.socket.settimeout) or use [`asyncio.wait_for`](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for) consistently; do not rely on hung syscalls without a bound.
- Log `errno`, `strerror`, and the raising frame’s layer (socket, thread pool, asyncio) for support tickets.
- Distinguish from [`BlockingIOError`](../blockingioerror/index.md) (`EAGAIN` / `EWOULDBLOCK`) on non-blocking sockets—would-block is not a timeout.
