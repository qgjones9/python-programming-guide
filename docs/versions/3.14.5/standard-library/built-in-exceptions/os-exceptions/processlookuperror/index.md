# [ProcessLookupError](https://docs.python.org/3/library/exceptions.html#ProcessLookupError)

`ProcessLookupError` is raised when no process exists for the given process id—for example sending a signal to a PID that has already exited. It corresponds to `errno.ESRCH`. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#ProcessLookupError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md); mapped from `ESRCH` in the [OS exceptions errno table](../index.md#errno--exception-mapping).
- Related to [`ChildProcessError`](../childprocesserror/index.md) (`ECHILD`) for wait/waitpid semantics when the target is not a child of the current process.
- Distinct from application-level “job not found” errors—this type reflects the kernel reporting that the PID does not exist.

| errno | Exception |
|-------|-----------|
| `ESRCH` | `ProcessLookupError` |

---

## When it is raised

`os.kill(pid, sig)` on a stale PID, `os.getpriority` / scheduling helpers on a vanished process, or certain `/proc`-style operations when the target exited between your check and the syscall raise `ProcessLookupError`. Signal `0` on POSIX checks existence without delivering a signal and still raises `ESRCH` when the PID is invalid.

```python
import errno

exc = OSError(errno.ESRCH, "No such process")
assert isinstance(exc, ProcessLookupError)
assert exc.errno == errno.ESRCH
```

---

## Handling patterns

Treat `ProcessLookupError` as an idempotent “already gone” outcome during shutdown sweeps and supervisor health checks.

```python
import os

def signal_if_alive(pid, sig):
    try:
        os.kill(pid, sig)
        return True
    except ProcessLookupError:
        return False  # already exited

# PID unlikely to exist; ESRCH is the expected outcome on Unix
assert signal_if_alive(999999999, 0) is False
```

Prefer [`subprocess`](https://docs.python.org/3/library/subprocess.html) handles over raw PIDs; when you must track PIDs, catch races instead of pre-checking with `ps`.

```python
import errno
import os

def terminate_gracefully(pid):
    try:
        os.kill(pid, 15)  # SIGTERM where available
        return "signaled"
    except ProcessLookupError as exc:
        assert exc.errno == errno.ESRCH
        return "already_stopped"

assert terminate_gracefully(999999999) == "already_stopped"
```

---

## Best practices

- Race is normal: a process can exit between your check and `kill`; handle `ProcessLookupError` idempotently rather than treating it as a fatal bug.
- Prefer `subprocess.run`, `Popen`, and `Popen.poll()` over manual PID bookkeeping when possible.
- On Windows, process signalling uses different APIs; errno mapping and available signals differ from POSIX.
- Log `pid` from `exc.args` alongside `exc.errno` and `exc.strerror` for operators.
