# [IsADirectoryError](https://docs.python.org/3/library/exceptions.html#IsADirectoryError)

`IsADirectoryError` is raised when a **file** operation is requested on a directory path—for example `os.remove()` on a folder. It corresponds to `errno.EISDIR`. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#IsADirectoryError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md).
- Pair with [`NotADirectoryError`](../notadirectoryerror/index.md) (`ENOTDIR`) for the opposite mistake.

| errno | Exception |
|-------|-----------|
| `EISDIR` | `IsADirectoryError` |

---

## When it is raised

Removing, truncating, or opening for write a path that is a directory triggers `IsADirectoryError`. Use `shutil.rmtree`, `Path.rmdir`, or directory-aware APIs instead.

```python
import os
import tempfile

def demo_is_a_directory():
    with tempfile.TemporaryDirectory() as tmp:
        try:
            os.remove(tmp)
        except IsADirectoryError as exc:
            assert exc.filename == tmp
            return True
    return False

assert demo_is_a_directory()
```

---

## Handling patterns

Validate intent with `pathlib.Path.is_file()` only when UX demands early feedback; EAFP with a clear error message is still fine.

```python
from pathlib import Path

def remove_file_only(path):
    p = Path(path)
    try:
        p.unlink()
    except IsADirectoryError as exc:
        raise ValueError(f"{exc.filename!r} is a directory, not a file") from exc

# Constructed demo without touching live paths
import errno
assert isinstance(OSError(errno.EISDIR, "Is a directory", "/tmp"), IsADirectoryError)
```

---

## Best practices

- Guide users toward `shutil.rmtree` or `Path.iterdir()` when they hit this error in CLI tools.
- Distinguish from `PermissionError` when deleting directory contents—may need recursive delete plus permission checks.
