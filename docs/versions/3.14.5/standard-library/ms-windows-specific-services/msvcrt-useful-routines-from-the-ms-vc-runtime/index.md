# [msvcrt — Useful routines from the MS VC++ runtime](https://docs.python.org/3/library/msvcrt.html)

The [`msvcrt`](https://docs.python.org/3/library/msvcrt.html) module exposes selected **Microsoft C runtime** functions on Windows: console character I/O, file locking, heap allocation, and **`get_osfhandle`** bridging CRT file descriptors to Win32 handles. It is Windows-only. Full function list remains on [docs.python.org](https://docs.python.org/3/library/msvcrt.html).

Related: [`os`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md) for portable file APIs; [`sys.stdin`](../../python-runtime-services/sys-system-specific-parameters-and-functions/index.md) for standard streams.

---

## Common functions — [File Operations](https://docs.python.org/3/library/msvcrt.html#file-operations)

| Function | Role |
|----------|------|
| `msvcrt.getch()` | Read one keypress as bytes (no echo) |
| `msvcrt.getwch()` | Unicode variant of `getch` |
| `msvcrt.kbhit()` | Return whether a key is waiting |
| `msvcrt.locking(fd, mode, nbytes)` | Lock byte range of CRT file descriptor |
| `msvcrt.setmode(fd, flags)` | Text vs binary mode on CRT fd |
| `msvcrt.open_osfhandle(handle, flags)` | Wrap Win32 handle as CRT fd |
| `msvcrt.get_osfhandle(fd)` | Win32 handle for CRT fd |

```python
# Goal: platform guard — msvcrt exists only on Windows
import importlib.util
import sys

spec = importlib.util.find_spec("msvcrt")
if sys.platform == "win32":
    import msvcrt

    assert spec is not None
    assert hasattr(msvcrt, "getch")
    assert hasattr(msvcrt, "locking")
else:
    assert spec is None
```

---

## Console input pattern (Windows)

On Windows interactive CLIs, `msvcrt.getwch()` reads a single keystroke without waiting for Enter—useful for menus and games. On other platforms, use `tty`/`termios` or higher-level libraries.

```python
# Goal: document cross-platform guard for getwch demo
import sys

if sys.platform == "win32":
    import msvcrt

    # kbhit returns non-zero when a key is buffered (non-blocking check)
    assert msvcrt.kbhit() in (0, 1)
```

---

## File locking constants

| Constant | Meaning |
|----------|---------|
| `LK_LOCK` | Block until lock acquired |
| `LK_NBLCK` | Fail immediately if locked |
| `LK_RLCK` | Shared (read) lock |
| `LK_UNLCK` | Release lock |

Use **`os.open`** + **`msvcrt.locking`** only when you need byte-range locks compatible with other CRT consumers; prefer `fcntl` on Unix.

---

## Best practices

| Practice | Why |
|----------|-----|
| Wrap **`msvcrt`** usage in `sys.platform == "win32"` | Module absent elsewhere |
| Prefer **`open(..., 'rb')`** + portable APIs when locking is not required | Simpler cross-platform code |
| Do not mix **`getch`** with buffered `input()` | Input layers fight for the console buffer |

---

## See also

- [`winreg`](../winreg-windows-registry-access/index.md) — Windows configuration store
- [`tty`](../../unix-specific-services/tty-terminal-control-functions/index.md) — Unix terminal helpers (counterpart)
