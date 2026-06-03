# [FileExistsError](https://docs.python.org/3/library/exceptions.html#FileExistsError)

`FileExistsError` is raised when a create operation would overwrite or duplicate an existing file or directory. It corresponds to `errno.EEXIST`. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#FileExistsError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md); counterpart to [`FileNotFoundError`](../filenotfounderror/index.md).
- Common from `os.mkdir()` without `exist_ok`, exclusive create flags, or `os.link()` when the target name is taken.

| errno | Exception |
|-------|-----------|
| `EEXIST` | `FileExistsError` |

---

## When it is raised

Creating a directory that already exists, or using APIs that require a **new** name when the path is occupied, produces `FileExistsError`. Some high-level APIs avoid raising it by design (`Path.mkdir(exist_ok=True)`, `open(..., "x")` vs `"w"`).

```python
import os
import tempfile

def demo_directory_exists():
    with tempfile.TemporaryDirectory() as tmp:
        sub = os.path.join(tmp, "already")
        os.mkdir(sub)
        try:
            os.mkdir(sub)
        except FileExistsError as exc:
            assert isinstance(exc, OSError)
            assert exc.filename == sub
            return True
    return False

assert demo_directory_exists()
```

---

## Handling patterns

Choose between catching the error and using non-throwing API options.

```python
import errno
from pathlib import Path

def ensure_dir(path):
    try:
        Path(path).mkdir(parents=True)
    except FileExistsError:
        pass  # race: another worker created it

# Constructor demo when EEXIST is reported without a live race
exc = OSError(errno.EEXIST, "File exists", "/tmp/x")
assert isinstance(exc, FileExistsError)
```

For atomic “create if absent,” prefer `open(path, "x")` or `os.open(..., os.O_CREAT | os.O_EXCL)` so existence is a single syscall.

---

## Best practices

- Do not treat `FileExistsError` like `FileNotFoundError` in cleanup code—usually you need to delete or pick another name.
- On shared filesystems, two processes can still race; `exist_ok=True` or exclusive create is safer than check-then-create (LBYL).
- Log `exc.filename` when reporting “could not create” to users.
