# [tty — Terminal control functions](https://docs.python.org/3/library/tty.html)

The [`tty`](https://docs.python.org/3/library/tty.html) module provides small helpers to put a terminal fd into **raw** or **cbreak** mode using [`termios`](termios-posix-style-tty-control/index.md). Raw mode disables echo and line buffering; cbreak keeps character-at-a-time input but may retain some signal handling. Unix-only. Full definitions remain on [docs.python.org](https://docs.python.org/3/library/tty.html).

Related: [`termios`](termios-posix-style-tty-control/index.md); [`msvcrt`](../../ms-windows-specific-services/msvcrt-useful-routines-from-the-ms-vc-runtime/index.md) on Windows for keypress I/O.

---

## Core functions

| Function | Role |
|----------|------|
| `tty.setraw(fd, when=termios.TCSAFLUSH)` | Raw mode: no echo, no line editing |
| `tty.setcbreak(fd, when=termios.TCSAFLUSH)` | Character-at-a-time without full raw |
| `tty.tcgetattr(fd)` / `tty.tcsetattr(...)` | Re-exported from `termios` |

```python
# Goal: setcbreak and restore (Unix)
import importlib.util
import sys

if importlib.util.find_spec("tty") and sys.stdin.isatty():
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        attrs = termios.tcgetattr(fd)
        assert not (attrs[3] & termios.ICANON)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)
elif importlib.util.find_spec("tty"):
    import tty

    assert hasattr(tty, "setcbreak")
else:
    assert sys.platform == "win32"
```

---

## Raw vs cbreak

| Mode | Echo | Line buffering | Typical use |
|------|------|----------------|-------------|
| cbreak | Often off | Off | Single-key menus |
| raw | Off | Off | Full-screen TUIs, `top`-like apps |

```python
# Goal: setraw clears canonical mode (Unix)
import importlib.util
import sys

if importlib.util.find_spec("tty") and sys.stdin.isatty():
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        lflag = termios.tcgetattr(fd)[3]
        assert not (lflag & termios.ICANON)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)
elif importlib.util.find_spec("tty"):
    import tty

    assert hasattr(tty, "setraw")
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Restore settings in **`finally`** | Essential for interactive shells |
| Use **`select`/`poll`** with non-blocking fd when reading keys | Avoid blocking forever |
| On Windows, use **`msvcrt.getwch`** or curses ports | No `tty` module |

---

## See also

- [`termios`](termios-posix-style-tty-control/index.md) — underlying attribute structs
- [`pty`](pty-pseudo-terminal-utilities/index.md) — child processes with tty semantics
