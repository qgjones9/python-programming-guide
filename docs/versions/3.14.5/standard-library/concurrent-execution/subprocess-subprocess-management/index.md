# [subprocess — Subprocess management](https://docs.python.org/3/library/subprocess.html)

The [`subprocess`](https://docs.python.org/3/library/subprocess.html) module launches **child OS processes**, connects to their stdin/stdout/stderr, and waits for exit codes — the modern replacement for `os.system`, `os.spawn*`, and `popen2`. Use it for shell tools, compilers, and services **outside** Python’s [`multiprocessing`](../multiprocessing-process-based-parallelism/index.md) model. Reference: [docs.python.org](https://docs.python.org/3/library/subprocess.html).

---

## High-level API

| Function | Role |
|----------|------|
| `run(args, *, capture_output=False, text=False, timeout=None, check=False, ...)` | One-shot: start, wait, return `CompletedProcess` |
| `Popen(...)` | Fine-grained control, pipes, incremental I/O |

Prefer **`run()`** for most scripts; use **`Popen`** when you need non-blocking reads or custom pipe wiring.

```python
# Goal: run captures stdout as text
import subprocess
import sys

cp = subprocess.run(
    [sys.executable, "-c", "print('hi')"],
    capture_output=True,
    text=True,
    check=True,
)
assert cp.stdout.strip() == "hi"
assert cp.returncode == 0
```

```python
# Goal: check=False inspects failing exit code
import subprocess
import sys

cp = subprocess.run(
    [sys.executable, "-c", "import sys; sys.exit(2)"],
    check=False,
)
assert cp.returncode == 2
```

---

## Safety defaults (3.6+)

`subprocess` avoids invoking the shell unless `shell=True`. Passing a **list** of arguments (`["echo", "hi"]`) avoids injection; reserve `shell=True` for trusted controlled strings.

| Flag | Effect |
|------|--------|
| `text=True` / `encoding` | Decode streams as str |
| `timeout=` | Raises `TimeoutExpired`; kill child |
| `check=True` | `CalledProcessError` on non-zero exit |

---

## `Popen` patterns

| Need | Approach |
|------|----------|
| Stream large output | `Popen` + `communicate()` or read loops |
| Merge stderr into stdout | `stderr=subprocess.STDOUT` |
| New session / process group | `start_new_session=True` (POSIX) |
| Replace legacy `os.popen` | `run` or `Popen` with pipes |

```python
# Goal: Popen with pipe read
import subprocess
import sys

with subprocess.Popen(
    [sys.executable, "-c", "print(99)"],
    stdout=subprocess.PIPE,
    text=True,
) as proc:
    out, _ = proc.communicate()
    assert proc.returncode == 0
assert out.strip() == "99"
```

---

## Platform notes — [Replacing Older Functions](https://docs.python.org/3/library/subprocess.html#replacing-older-functions-with-the-subprocess-module)

| Topic | Detail |
|-------|--------|
| Windows | `creationflags`, `startupinfo`; list2cmdline for argument quoting |
| `posix_spawn` | Optional fast path when `close_fds` and fds allow |
| Timeouts | Kill process tree behavior documented per version |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Deadlock on full pipes | Use `communicate()` or drain streams |
| `shell=True` with user input | Never for untrusted data |
| Orphan processes on timeout | Use `timeout=` on `run`/`communicate` |
| Assuming cwd/env inherited | Pass explicit `cwd`, `env` |

---

## See also

- [multiprocessing](../multiprocessing-process-based-parallelism/index.md) — Python worker processes
- [os](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md) — low-level process IDs
- [asyncio subprocess](https://docs.python.org/3/library/asyncio-subprocess.html) — non-blocking integration
