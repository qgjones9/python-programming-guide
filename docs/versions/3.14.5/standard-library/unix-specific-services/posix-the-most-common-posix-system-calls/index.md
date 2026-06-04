# [posix — The most common POSIX system calls](https://docs.python.org/3/library/posix.html)

The [`posix`](https://docs.python.org/3/library/posix.html) module exposes **POSIX system call bindings** that also appear on the public [`os`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md) module. Historically it was the low-level namespace; new code should **`import os`** rather than `posix` directly. On Windows, most `posix` names are absent. Full name list remains on [docs.python.org](https://docs.python.org/3/library/posix.html).

Related: [`os`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md); [`fcntl`](fcntl-the-fcntl-and-ioctl-system-calls/index.md) for fd control.

---

## Relationship to `os`

| Aspect | Detail |
|--------|--------|
| Implementation | `os` re-exports `posix` (or `nt`) names |
| Portability | Prefer `os.open`, `os.fork`, `os.waitpid`, … |
| `posix` module | Still importable on Unix for introspection |

```python
# Goal: posix names mirror os on Unix
import importlib.util
import os
import sys

if sys.platform != "win32":
    import posix

    assert posix.getpid() == os.getpid()
    assert posix.O_RDONLY == os.O_RDONLY
else:
    assert importlib.util.find_spec("posix") is None
```

---

## Common overlapping names

| Name | Purpose |
|------|---------|
| `fork`, `execv`, `waitpid` | Process creation and reaping |
| `open`, `read`, `write`, `close` | File descriptors |
| `stat`, `lstat`, `fstat` | Metadata |
| `uname` | System identification tuple |
| `access` | Check path permissions |

```python
# Goal: uname via os (portable public API)
import os
import sys

if sys.platform != "win32":
    sysname, nodename, release, version, machine = os.uname()
    assert sysname
    assert machine
```

---

## Best practices

| Practice | Why |
|----------|-----|
| **`import os`**, not `posix` | Stable documented interface |
| Use **`os.supports_*`** sets to probe availability | Some calls missing on macOS or sandbox |
| Read **`posix`** only for debugging or re-export tests | Not for application logic |

---

## See also

- [`os`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md) — preferred POSIX facade
- [`pwd`](pwd-the-password-database/index.md) / [`grp`](grp-the-group-database/index.md) — account databases
