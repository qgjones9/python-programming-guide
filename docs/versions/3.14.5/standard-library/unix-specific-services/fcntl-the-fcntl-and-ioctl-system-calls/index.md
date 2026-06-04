# [fcntl — The fcntl and ioctl system calls](https://docs.python.org/3/library/fcntl.html)

The [`fcntl`](https://docs.python.org/3/library/fcntl.html) module performs **file descriptor control** on Unix: advisory locking (`F_GETLK`, `F_SETLK`, `F_SETLKW`), flag manipulation (`F_GETFL`, `F_SETFL`), and **`ioctl`** for device-specific operations. Unix-only (not available on Windows). Full constants remain on [docs.python.org](https://docs.python.org/3/library/fcntl.html).

Related: [`os.open`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md); [`msvcrt.locking`](../../ms-windows-specific-services/msvcrt-useful-routines-from-the-ms-vc-runtime/index.md) on Windows.

---

## Core functions

| Function | Role |
|----------|------|
| `fcntl.fcntl(fd, cmd, arg=0)` | General fd control |
| `fcntl.ioctl(fd, request, arg=0, mutate_flag=True)` | Device/ioctl operations |
| `fcntl.flock(fd, operation)` | Whole-file advisory locks (BSD) |

```python
# Goal: get and preserve file status flags (Unix)
import importlib.util
import os
import tempfile

if importlib.util.find_spec("fcntl"):
    import fcntl

    with tempfile.NamedTemporaryFile() as tmp:
        fd = tmp.fileno()
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        assert isinstance(flags, int)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags)
else:
    import sys

    assert sys.platform == "win32"
```

---

## Advisory locking pattern

POSIX record locks via **`struct flock`** packed bytes (platform-specific layout)—often easier with the third-party **`fcntl`** recipes in docs or **`filelock`** libraries for application code.

```python
# Goal: flock exclusive then unlock (Unix)
import importlib.util
import os
import tempfile

if importlib.util.find_spec("fcntl"):
    import fcntl

    with tempfile.NamedTemporaryFile() as tmp:
        fd = tmp.fileno()
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fd, fcntl.LOCK_UN)
```

---

## `ioctl` note

The **`ioctl`** request codes are device-specific (terminal sizes, socket flags, …). Portable Python code rarely calls `ioctl` directly—prefer higher-level modules (`termios`, `socket`, `tty`).

---

## Best practices

| Practice | Why |
|----------|-----|
| Treat locks as **advisory** | All processes must cooperate |
| Use **`LOCK_NB`** to avoid deadlocks | Retry or fail fast |
| Guard on **Windows** | Use `msvcrt.locking` or portalocker |

---

## See also

- [`os`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md) — fd open/close
- [`termios`](../termios-posix-style-tty-control/index.md) — tty ioctls via higher API
