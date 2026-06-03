# [NotADirectoryError](https://docs.python.org/3/library/exceptions.html#NotADirectoryError)

`NotADirectoryError` is raised when a **directory** operation is requested on a non-directory path—for example `os.listdir()` on a regular file. It corresponds to `errno.ENOTDIR`. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#NotADirectoryError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md); see the [errno mapping table](../index.md#errno--exception-mapping) in the parent OS exceptions page.
- Pair with [`IsADirectoryError`](../isadirectoryerror/index.md) (`EISDIR`) for the opposite mistake (file operation on a directory).
- On many POSIX systems, opening or traversing a path component that is an ordinary file as if it were a directory also yields `ENOTDIR`.

| errno | Exception |
|-------|-----------|
| `ENOTDIR` | `NotADirectoryError` |

---

## When it is raised

Typical triggers include `os.listdir()`, `os.chdir()`, or `pathlib.Path.iterdir()` on a regular file, a symlink whose target is a file, or a path segment that exists but is not a directory. It is **not** raised when the path is missing (`FileNotFoundError`) or when access is denied on an existing directory (`PermissionError`).

```python
import os
import tempfile

def demo_not_a_directory():
    with tempfile.TemporaryDirectory() as tmp:
        fpath = os.path.join(tmp, "file.txt")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write("x")
        try:
            os.listdir(fpath)
        except NotADirectoryError as exc:
            assert isinstance(exc, OSError)
            assert exc.filename == fpath
            return True
    return False

assert demo_not_a_directory()
```

---

## Handling patterns

Use EAFP in directory walkers: attempt the operation and catch `NotADirectoryError` when following user-provided paths or symlinks.

```python
import errno
import os
import tempfile
from pathlib import Path

def safe_listdir(path):
    try:
        return list(Path(path).iterdir())
    except NotADirectoryError:
        return []

with tempfile.TemporaryDirectory() as tmp:
    fpath = os.path.join(tmp, "file.txt")
    Path(fpath).write_text("x")
    assert safe_listdir(fpath) == []
assert isinstance(OSError(errno.ENOTDIR, "Not a directory"), NotADirectoryError)
```

For APIs that require a directory root, translate to a clear application error while preserving the OS context with `raise ... from exc`.

```python
def require_directory(path):
    try:
        return list(os.listdir(path))
    except NotADirectoryError as exc:
        raise ValueError(f"{exc.filename!r} is not a directory") from exc
```

---

## Best practices

- Validate path types in APIs that require directories (`upload_dir`, batch importers); use `Path.is_dir()` for early UX feedback, but still handle `NotADirectoryError` under races.
- Do not confuse with [`FileNotFoundError`](../filenotfounderror/index.md)—the path often **exists** but has the wrong type.
- Log `exc.filename` and `exc.errno` for support tickets; re-raise or wrap with `from exc` when translating to domain errors.
