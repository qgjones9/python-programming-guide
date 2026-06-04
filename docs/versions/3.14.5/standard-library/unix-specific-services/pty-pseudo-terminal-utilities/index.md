# [pty — Pseudo-terminal utilities](https://docs.python.org/3/library/pty.html)

The [`pty`](https://docs.python.org/3/library/pty.html) module allocates **pseudo-terminal (PTY) pairs** on Unix: a master fd for the parent and a slave tty for the child—so programs that expect a terminal (colors, password prompts, pagers) behave correctly when automated. Unix-only. Full API remains on [docs.python.org](https://docs.python.org/3/library/pty.html).

Related: [`subprocess`](../../concurrent-execution/subprocess-subprocess-management/index.md); [`tty`](../tty-terminal-control-functions/index.md).

---

## Core functions — [Example](https://docs.python.org/3/library/pty.html#example)

| Function | Role |
|----------|------|
| `pty.openpty()` | Return `(master_fd, slave_fd)` |
| `pty.fork()` | Fork; child gets controlling tty on slave, returns `(pid, fd)` in parent |
| `pty.spawn(argv, master_read=..., stdin=...)` | Run command attached to new PTY |
| `pty.master_open()` / `pty.slave_open()` | Lower-level open (platform-specific) |

```python
# Goal: openpty returns two fds (Unix)
import importlib.util
import os

if importlib.util.find_spec("pty"):
    import pty

    master, slave = pty.openpty()
    assert master != slave
    os.close(master)
    os.close(slave)
else:
    import sys

    assert sys.platform == "win32"
```

---

## `spawn` workflow

`pty.spawn` is what **`popen2`-style** automation uses internally: the child session leader attaches to the slave side; the parent reads/writes the master like a bidirectional pipe with tty semantics.

```python
# Goal: spawn echoes through PTY (Unix)
import importlib.util
import os

if importlib.util.find_spec("pty"):
    import pty

    captured = []

    def master_read(fd):
        data = os.read(fd, 1024)
        captured.append(data)
        return data

    status = pty.spawn(["/bin/echo", "hello"], master_read=master_read)
    assert status == 0
    assert b"hello" in b"".join(captured)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Close unused **master/slave** ends after fork | Prevent hangs |
| Prefer **`subprocess`** when tty is not required | Simpler pipes suffice |
| Read master fd in **non-blocking** or threaded loops | Avoid deadlock with full buffers |

---

## See also

- [`subprocess`](../../concurrent-execution/subprocess-subprocess-management/index.md) — process management
- [`termios`](../termios-posix-style-tty-control/index.md) — configure slave tty
