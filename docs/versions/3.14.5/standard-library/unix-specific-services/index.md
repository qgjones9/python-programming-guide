# [Unix-specific services](https://docs.python.org/3/library/unix.html)

The **Unix-specific services** section covers modules tied to **POSIX** and Unix-like systems: shell-like lexing (`shlex`), low-level syscalls (`posix`, `fcntl`), account databases (`pwd`, `grp`), TTY control (`termios`, `tty`, `pty`), resource limits (`resource`), and syslog (`syslog`). Most are unavailable or limited on native Windows Python. Full reference remains on [docs.python.org](https://docs.python.org/3/library/unix.html).

Portable code should use [`os`](../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md) and [`pathlib`](../file-and-directory-access/pathlib-object-oriented-filesystem-paths/index.md) first, then reach for these modules when POSIX semantics are required.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`shlex`](shlex-simple-lexical-analysis/index.md) | POSIX shell-like tokenization (portable) |
| [`posix`](posix-the-most-common-posix-system-calls/index.md) | Low-level POSIX API (largely superseded by `os`) |
| [`pwd`](pwd-the-password-database/index.md) | User account entries from `/etc/passwd` |
| [`grp`](grp-the-group-database/index.md) | Group database entries |
| [`termios`](termios-posix-style-tty-control/index.md) | tty attribute get/set |
| [`tty`](tty-terminal-control-functions/index.md) | cbreak/raw mode helpers |
| [`pty`](pty-pseudo-terminal-utilities/index.md) | Fork PTY pairs for pseudo-terminals |
| [`fcntl`](fcntl-the-fcntl-and-ioctl-system-calls/index.md) | File descriptor control and locking |
| [`resource`](resource-resource-usage-information/index.md) | `getrusage`, resource limits |
| [`syslog`](syslog-unix-syslog-library-routines/index.md) | Send messages to syslog |

---

## Portability matrix

| Module | Linux | macOS | Windows |
|--------|-------|-------|---------|
| `shlex` | Yes | Yes | Yes |
| `posix`, `pwd`, `grp`, `termios`, `tty`, `pty`, `fcntl`, `resource`, `syslog` | Yes | Mostly | No / stub |

```python
# Goal: verify shlex is portable; pwd is Unix-only
import importlib.util
import sys

assert importlib.util.find_spec("shlex") is not None
has_pwd = importlib.util.find_spec("pwd") is not None
if sys.platform == "win32":
    assert not has_pwd
else:
    assert has_pwd
```

---

## Choosing the right tool

| Task | Module |
|------|--------|
| Parse shell command lines safely | [`shlex`](shlex-simple-lexical-analysis/index.md) |
| Resolve UID → username | [`pwd`](pwd-the-password-database/index.md) |
| Raw/cbreak terminal for REPL | [`tty`](tty-terminal-control-functions/index.md) + [`termios`](termios-posix-style-tty-control/index.md) |
| Spawn process attached to PTY | [`pty`](pty-pseudo-terminal-utilities/index.md) |
| Advisory file lock on fd | [`fcntl`](fcntl-the-fcntl-and-ioctl-system-calls/index.md) |
| Log to `/var/log/syslog` | [`syslog`](syslog-unix-syslog-library-routines/index.md) |

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`os.*`** over **`posix.*`** | Same bindings, stable public names |
| Restore tty settings in **`finally`** after `tty.setraw` | Avoid broken terminal echo |
| Use **`shlex.split(..., posix=True)`** for user input | Respects quoting rules |
| Guard **`pwd`/`grp`/`syslog`** imports on Windows CI | Clean skip vs ImportError |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [shlex — Simple lexical analysis](shlex-simple-lexical-analysis/index.md) | Shell-style splitting and quoting |
| [posix — The most common POSIX system calls](posix-the-most-common-posix-system-calls/index.md) | Thin POSIX namespace |
| [pwd — The password database](pwd-the-password-database/index.md) | User database lookups |
| [grp — The group database](grp-the-group-database/index.md) | Group database lookups |
| [termios — POSIX style tty control](termios-posix-style-tty-control/index.md) | Terminal attribute structs |
| [tty — Terminal control functions](tty-terminal-control-functions/index.md) | Raw/cbreak mode |
| [pty — Pseudo-terminal utilities](pty-pseudo-terminal-utilities/index.md) | PTY allocation and `spawn` |
| [fcntl — The fcntl and ioctl system calls](fcntl-the-fcntl-and-ioctl-system-calls/index.md) | Locks, flags, ioctls |
| [resource — Resource usage information](resource-resource-usage-information/index.md) | CPU/memory limits and usage |
| [syslog — Unix syslog library routines](syslog-unix-syslog-library-routines/index.md) | Unix system logging |
