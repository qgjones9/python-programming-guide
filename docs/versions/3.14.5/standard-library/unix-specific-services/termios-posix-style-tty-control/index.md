# [termios — POSIX style tty control](https://docs.python.org/3/library/termios.html)

The [`termios`](https://docs.python.org/3/library/termios.html) module configures **terminal line disciplines**: baud rate, echo, canonical mode, signal generation (`ISIG`), and special characters (`VINTR`, `VEOF`, …). It wraps `termios(3)` on Unix. Windows lacks this module. Full struct field reference remains on [docs.python.org](https://docs.python.org/3/library/termios.html).

Related: [`tty`](../tty-terminal-control-functions/index.md) for raw/cbreak helpers; [`pty`](../pty-pseudo-terminal-utilities/index.md) for pseudo-TTY pairs.

---

## Core functions — [Example](https://docs.python.org/3/library/termios.html#example)

| Function | Role |
|----------|------|
| `termios.tcgetattr(fd)` | Return `[iflag, oflag, cflag, lflag, ispeed, ospeed, cc]` |
| `termios.tcsetattr(fd, when, attributes)` | Apply settings (`TCSANOW`, `TCSAFLUSH`, …) |
| `termios.tcsendbreak(fd, duration)` | Send break condition |
| `termios.tcflush(fd, queue)` | Discard input/output queues |
| `termios.tcflow(fd, action)` | Suspend/resume transmission |

```python
# Goal: read and restore tty attributes (Unix, real tty required)
import importlib.util
import sys

if importlib.util.find_spec("termios") and sys.stdin.isatty():
    import termios

    fd = sys.stdin.fileno()
    attrs = termios.tcgetattr(fd)
    assert len(attrs) == 7
    assert isinstance(attrs[0], int)  # iflag
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
elif importlib.util.find_spec("termios"):
    import termios

    assert hasattr(termios, "TCSANOW")
else:
    assert sys.platform == "win32"
```

---

## Attribute list indices

| Index | Flag word |
|-------|-----------|
| 0 | `iflag` — input processing |
| 1 | `oflag` — output processing |
| 2 | `cflag` — control modes |
| 3 | `lflag` — local modes (echo, canonical) |
| 4 | `ispeed` |
| 5 | `ospeed` |
| 6 | `cc` — control character list |

```python
# Goal: disable echo temporarily (Unix, real tty required)
import importlib.util
import sys

if importlib.util.find_spec("termios") and sys.stdin.isatty():
    import termios

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ECHO  # lflag
    try:
        termios.tcsetattr(fd, termios.TCSANOW, new)
        assert not (termios.tcgetattr(fd)[3] & termios.ECHO)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Always **`try/finally`** restore attributes | Broken echo cripples the shell |
| Prefer **`tty.setraw` / `setcbreak`** for common cases | Less error-prone than manual flag math |
| Operate on **`sys.stdin.fileno()`** or PTY master fd | Must be a tty |

---

## See also

- [`tty`](../tty-terminal-control-functions/index.md) — convenience wrappers
- [`pty`](../pty-pseudo-terminal-utilities/index.md) — allocate PTY for child processes
