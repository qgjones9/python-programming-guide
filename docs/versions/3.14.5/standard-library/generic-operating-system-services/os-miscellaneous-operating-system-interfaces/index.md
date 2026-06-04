# [os — Miscellaneous operating system interfaces](https://docs.python.org/3/library/os.html)

The [`os`](https://docs.python.org/3/library/os.html) module wraps **operating-system services** in a mostly POSIX-shaped, portable API: environment variables, current working directory, file and directory operations, process identifiers, and platform-specific extensions guarded by availability notes. For path manipulation use [`os.path`](../../file-and-directory-access/ospath-common-pathname-manipulations/index.md) or [`pathlib`](../../file-and-directory-access/pathlib-object-oriented-filesystem-paths/index.md); for high-level copies see [`shutil`](../../file-and-directory-access/shutil-high-level-file-operations/index.md). Full API reference remains on [docs.python.org](https://docs.python.org/3/library/os.html).

Related: [`io`](../io-core-tools-for-working-with-streams/index.md) for stream types; [`errno`](../errno-standard-errno-system-symbols/index.md) for errno constants; [`subprocess`](../../concurrent-execution/subprocess-subprocess-management/index.md) for spawning processes.

---

## API surface — overview

| Area | Key APIs | Use when |
|------|----------|----------|
| Process / user | `getpid()`, `getuid()`, `environ` | Inspect or modify process context |
| Files & dirs | `listdir()`, `scandir()`, `mkdir()`, `rename()`, `remove()` | Directory trees without pathlib |
| Metadata | `stat()`, `stat_result` | Size, mtime, mode bits |
| Paths ↔ bytes | `fsencode()`, `fsdecode()` | Bridge str paths and OS bytes |
| Walk | `walk()` | Recursive directory traversal |
| Spawn (legacy) | `system()`, `popen()` | Prefer `subprocess` for new code |

---

## Process parameters — [Process Parameters](https://docs.python.org/3/library/os.html#process-parameters)

| API | Notes |
|-----|-------|
| `os.environ` | Mapping of environment strings; changes call `putenv` automatically |
| `os.environb` | Bytes environment (Unix); use when avoiding filesystem encoding |
| `os.getenv(key, default=None)` | Safe lookup without KeyError |
| `os.getpid()` | Current process ID |
| `os.name` | `'posix'`, `'nt'`, or `'java'` — coarse OS family |

```python
# Goal: read and set environment variables safely
import os

os.environ["DEMO_VAR"] = "alpha"
assert os.getenv("DEMO_VAR") == "alpha"
assert os.getenv("UNLIKELY_MISSING_KEY", "fallback") == "fallback"
del os.environ["DEMO_VAR"]
```

---

## File and directory operations — [Files and Directories](https://docs.python.org/3/library/os.html#files-and-directories)

| API | Notes |
|-----|-------|
| `os.getcwd()` / `os.chdir(path)` | Current working directory |
| `os.listdir(path='.')` | Names in directory (not full paths) |
| `os.scandir(path='.')` | Iterator of `DirEntry` with stat cache |
| `os.mkdir(path, mode=0o777)` | Single directory; `makedirs` for parents |
| `os.makedirs(name, exist_ok=False)` | Recursive create |
| `os.rename(src, dst)` / `os.replace(src, dst)` | `replace` overwrites destination on Windows |
| `os.remove(path)` / `os.unlink(path)` | Delete file |
| `os.rmdir(path)` | Remove empty directory |
| `os.stat(path)` | Metadata; use `DirEntry.stat()` from scandir when possible |

```python
# Goal: create a directory tree and list entries
import os
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    nested = os.path.join(tmp, "a", "b")
    os.makedirs(nested, exist_ok=True)
    assert os.path.isdir(nested)
    names = os.listdir(tmp)
    assert names == ["a"]
```

```python
# Goal: scandir with stat without extra syscalls
import os
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "note.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("hi")
    for entry in os.scandir(tmp):
        st = entry.stat()
        assert entry.name == "note.txt"
        assert st.st_size == 2
```

---

## Path encoding — [File Names, Command Line Arguments, and Environment Variables](https://docs.python.org/3/library/os.html#file-names-command-line-arguments-and-environment-variables)

| API | Role |
|-----|------|
| `os.fsencode(path)` | str → bytes using filesystem encoding |
| `os.fsdecode(path)` | bytes → str using filesystem encoding |
| UTF-8 mode (3.7+) | Forces UTF-8 for fs encoding when LC_CTYPE is C/POSIX |

Always pass **str** paths in new code; use `fsencode`/`fsdecode` when interfacing with C APIs or `os.environb`.

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`pathlib`** for joins and globs | Less error-prone than manual string paths |
| Use **`exist_ok=True`** with `makedirs` | Avoid races when multiple processes create dirs |
| Catch **`OSError`** subclasses | `FileNotFoundError`, `PermissionError` carry `.errno` |
| Use **`os.replace`** for atomic renames | Safer than `rename` when destination may exist |
| Avoid **`os.system`** for shell commands | Use `subprocess` with explicit args |
| Check **`os.path.exists`** vs **`isfile`** | Directories and symlinks need different tests |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| **`listdir` returns names only** | Broken paths when cwd changes | Join with base path or use scandir |
| **`mkdir` without parents** | `FileNotFoundError` | Use `makedirs` |
| **Platform-specific `os` attrs** | `AttributeError` on Windows/WASI | Consult availability notes upstream |
| **Stale `os.environ` snapshot** | External env changes invisible | Re-read via `getenv` after fork in some cases |
| **Symlink following in `stat`** | Unexpected target metadata | Use `lstat` or `DirEntry.is_symlink()` |

---

## Platform notes

| Platform | Limitation |
|----------|------------|
| Windows | No `fork()`; some uid/gid calls absent |
| WASI / mobile | Many process and signal APIs unavailable or stubbed |
| VxWorks | No `popen`, `fork`, `execv`, `spawn*` |

For portable code, feature-detect with `hasattr(os, "fork")` or use [`platform`](../platform-access-to-underlying-platforms-identifying-data/index.md).
