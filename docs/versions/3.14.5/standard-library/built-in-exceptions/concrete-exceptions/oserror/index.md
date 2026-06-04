# [OSError](https://docs.python.org/3/library/exceptions.html#OSError)

Raised for **system-related errors**, including I/O failures such as missing files or full disks. Since 3.3, `EnvironmentError`, `IOError`, and (on Windows) `WindowsError` are **aliases**. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#OSError) and [OS exceptions](https://docs.python.org/3/library/exceptions.html#os-exceptions).

---

## When it is raised

| Situation | Often becomes |
|-----------|---------------|
| Missing file on open | `FileNotFoundError` (`errno.ENOENT`) |
| Permission denied | `PermissionError` |
| Disk full | `OSError` with appropriate `errno` |
| Generic OS failure | Plain `OSError` |

Constructing `OSError` directly may return a **more specific subclass** based on `errno` (PEP 3151).

---

## Common attributes

| Attribute | Meaning |
|-----------|----------|
| `errno` | Numeric C `errno` value |
| `strerror` | OS error message |
| `filename` | Path involved (single-path operations) |
| `filename2` | Second path (e.g. `os.rename`) |
| `winerror` | Native Windows code (Windows only) |

---

## errno → subclass mapping (selected)

| `errno` | Subclass |
|---------|----------|
| `ENOENT` | `FileNotFoundError` |
| `EEXIST` | `FileExistsError` |
| `EACCES`, `EPERM` | `PermissionError` |
| `EISDIR` | `IsADirectoryError` |
| `ENOTDIR` | `NotADirectoryError` |
| `ETIMEDOUT` | `TimeoutError` |

Full list: [OS exceptions](https://docs.python.org/3/library/exceptions.html#os-exceptions).

---

## Demonstrating raise and catch

```python
import errno
import os
import tempfile

# Goal: missing file raises FileNotFoundError (OSError subclass)
missing = os.path.join(tempfile.gettempdir(), 'no_such_file_xyz')
caught = None
try:
    open(missing)
except FileNotFoundError as exc:
    caught = exc.errno
assert caught == errno.ENOENT
```

---

## Best practices

- Catch specific subclasses (`FileNotFoundError`) when you know the operation.
- Use `except OSError` for broad filesystem/network recovery.
- Legacy aliases: [`EnvironmentError`](../environmenterror/index.md), [`IOError`](../ioerror/index.md), [`WindowsError`](../windowserror/index.md).

---

## Sections in this repo

- [EnvironmentError](../environmenterror/index.md)
- [IOError](../ioerror/index.md)
- [WindowsError](../windowserror/index.md)
