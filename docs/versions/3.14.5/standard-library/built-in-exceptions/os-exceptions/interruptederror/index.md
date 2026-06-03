# [InterruptedError](https://docs.python.org/3/library/exceptions.html#InterruptedError)

`InterruptedError` is raised when a system call is interrupted by a signal before it completes. It corresponds to `errno.EINTR`. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#InterruptedError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md).
- Since **PEP 475** (Python 3.5), the interpreter **retries** most interrupted syscalls automatically, so application code rarely sees `InterruptedError` unless a signal handler raises or certain paths opt out.

| errno | Exception |
|-------|-----------|
| `EINTR` | `InterruptedError` |

---

## When it is raised

Slow syscalls (`read`, `select`, `sleep`) interrupted by SIGCHLD, SIGALRM, or user signals may surface `EINTR`. With default 3.5+ behaviour, CPython loops until the call succeeds or a different errno is returned.

```python
import errno

exc = OSError(errno.EINTR, "Interrupted system call")
assert isinstance(exc, InterruptedError)
```

---

## Handling patterns

Legacy code sometimes retried on `EINTR` manually; modern Python usually makes that unnecessary.

```python
import errno

def retry_on_eintr(action, retries=3):
    for _ in range(retries):
        try:
            return action()
        except InterruptedError:
            continue
    return None

calls = {"n": 0}

def flaky():
    calls["n"] += 1
    if calls["n"] < 2:
        raise InterruptedError(errno.EINTR, "interrupted")
    return "done"

assert retry_on_eintr(flaky) == "done"
```

If you install signal handlers that raise exceptions, expect those exceptions—not necessarily bare `InterruptedError`.

---

## Best practices

- Rely on PEP 475 automatic restart for new code; document any C extension that disables it.
- Do not busy-loop on `InterruptedError` without backoff when you must handle it manually.
- Test signal-heavy workloads (workers, timeouts) on the target OS; behaviour differs slightly on Windows.
