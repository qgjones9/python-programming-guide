# [errno — Standard errno system symbols](https://docs.python.org/3/library/errno.html)

The [`errno`](https://docs.python.org/3/library/errno.html) module exposes **integer errno constants** (`ENOENT`, `EEXIST`, …) and `errorcode`, a reverse map from number to name. Platform-specific symbols are defined only when available on the current OS. Pair with [`os.strerror()`](https://docs.python.org/3/library/os.html#os.strerror) for human messages and with `OSError.errno` on raised exceptions. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/errno.html).

Related: [`os`](../os-miscellaneous-operating-system-interfaces/index.md) OS calls that raise `OSError`; built-in exception types mapped from errno (PEP 3151).

---

## Module contents — overview

| Name | Role |
|------|------|
| `errno.ENOENT`, `errno.EEXIST`, … | Integer codes matching C/POSIX headers |
| `errno.errorcode` | `dict` mapping code → short name (`ENOENT`) |
| Exception mapping | Many codes map to `FileNotFoundError`, `PermissionError`, etc. |

---

## Common errno values

| Constant | Typical meaning | Python exception (when mapped) |
|----------|-----------------|--------------------------------|
| `EPERM` / `EACCES` | Operation not permitted | `PermissionError` |
| `ENOENT` | No such file or directory | `FileNotFoundError` |
| `EEXIST` | File already exists | `FileExistsError` |
| `EISDIR` | Is a directory | `IsADirectoryError` |
| `ENOTDIR` | Not a directory | `NotADirectoryError` |
| `EAGAIN` / `EWOULDBLOCK` | Would block | `BlockingIOError` |
| `EINTR` | Interrupted system call | `InterruptedError` |
| `ETIMEDOUT` | Connection timed out | `TimeoutError` |
| `ECONNREFUSED` | Connection refused | `ConnectionRefusedError` |
| `EPIPE` | Broken pipe | `BrokenPipeError` |

Not every symbol exists on every platform — use `getattr(errno, "ENOSPC", None)` when optional.

---

## Usage patterns — [errno](https://docs.python.org/3/library/errno.html)

```python
# Goal: map errno integer to symbolic name
import errno

assert errno.errorcode[errno.ENOENT] == "ENOENT"
assert errno.errorcode[errno.EEXIST] == "EEXIST"
```

```python
# Goal: compare OSError.errno after a failed operation
import errno
import os
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    missing = os.path.join(tmp, "nope.txt")
    try:
        os.remove(missing)
    except FileNotFoundError as exc:
        assert exc.errno == errno.ENOENT
    else:
        raise AssertionError("expected FileNotFoundError")
```

```python
# Goal: translate code to message with os.strerror
import errno
import os

msg = os.strerror(errno.ENOENT)
assert isinstance(msg, str) and len(msg) > 0
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Catch **`OSError` subclasses** first | More specific than errno comparisons |
| Compare **`exc.errno == errno.XXX`** | Stable across platforms for mapped errors |
| Use **`os.strerror(code)`** for logs | Locale-aware message text |
| Guard **optional errno names** | Avoid `AttributeError` on Windows/WASI |
| Prefer **`except FileNotFoundError`** | Clearer than errno check on ENOENT |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| **`EWOULDBLOCK` alias to `EAGAIN`** | Same value on many platforms | Either name works |
| **Windows errno subset** | Missing socket constants | Use exception types for sockets |
| **Assuming all symbols importable** | Build-time/platform differences | Introspect `errno.errorcode.keys()` |
| **Comparing message strings** | Localized / varies by OS | Compare `.errno` or exception type |
| **Legacy `except IOError`** | Alias of `OSError` since 3.3 | Use `OSError` in new code |
