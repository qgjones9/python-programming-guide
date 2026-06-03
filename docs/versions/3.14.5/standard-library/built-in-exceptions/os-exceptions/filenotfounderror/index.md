# [FileNotFoundError](https://docs.python.org/3/library/exceptions.html#FileNotFoundError)

`FileNotFoundError` is raised when a file or directory path does not exist at the time of the syscall. It corresponds to `errno.ENOENT` and is the most common OS exception in everyday file I/O. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#FileNotFoundError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md); sibling to `FileExistsError`, `PermissionError`, and other errno-specific types.
- Raised by `open()`, `pathlib.Path.read_text()`, `os.stat()`, `shutil.copy()`, and most APIs that touch the filesystem.
- An `except OSError` or `except FileNotFoundError` handler matches; prefer the specific type when “missing path” is the only outcome you treat specially.

| errno | Exception |
|-------|-----------|
| `ENOENT` | `FileNotFoundError` |

---

## When it is raised

Typical triggers include opening a path that was never created, following a broken symlink target, or referencing a parent directory that does not exist. It is **not** raised for wrong types (that is usually `TypeError`) or permission denied on an existing path (`PermissionError`).

```python
import os
import tempfile

def demo_missing_file():
    path = os.path.join(tempfile.gettempdir(), "pguide-filenotfound-demo")
    try:
        open(path)
    except FileNotFoundError as exc:
        assert isinstance(exc, OSError)
        assert exc.filename == path
        return True
    return False

assert demo_missing_file()
```

---

## Handling patterns

Use EAFP: call the operation and catch `FileNotFoundError` rather than pre-checking with `os.path.exists`, which races with other processes.

```python
from pathlib import Path

def load_optional_json(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return None

assert load_optional_json("/tmp/pguide-no-such-file") is None
```

For idempotent cleanup, swallowing `FileNotFoundError` is idiomatic—the desired end state (path absent) is already true.

```python
import os

def unlink_quiet(path):
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass

unlink_quiet("/tmp/pguide-idempotent-remove")
```

---

## Best practices

- Distinguish `FileNotFoundError` from `NotADirectoryError` and `IsADirectoryError` when path semantics matter for error messages.
- Include `exc.filename` in logs; it is set for most path-taking builtins and `os` functions.
- Re-raise or wrap with `raise ... from exc` when translating to application-level errors so the original path remains in `__cause__`.
