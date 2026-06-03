# [ChildProcessError](https://docs.python.org/3/library/exceptions.html#ChildProcessError)

`ChildProcessError` is raised when an operation on a child process fails at the OS level—for example waiting on a process that is not a child of the current process. It corresponds to `errno.ECHILD`. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#ChildProcessError).

---

## Role in the hierarchy

- Subclass of [`OSError`](../../concrete-exceptions/oserror/index.md).
- Related to but distinct from [`ProcessLookupError`](../processlookuperror/index.md) (`ESRCH`, “no such process”).

| errno | Exception |
|-------|-----------|
| `ECHILD` | `ChildProcessError` |

---

## When it is raised

Classic example: calling `os.wait()` when there are no unwaited-for child processes, or certain `waitpid` failures. Higher-level [`subprocess`](https://docs.python.org/3/library/subprocess.html) usually wraps these into `subprocess.SubprocessError`.

```python
import errno

exc = OSError(errno.ECHILD, "No child processes")
assert isinstance(exc, ChildProcessError)
```

---

## Handling patterns

Prefer `subprocess.run`, `Popen.communicate`, and context managers so child lifecycle is managed; low-level `os.wait` is rare in application code.

```python
import subprocess

def run_ok(cmd):
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

assert run_ok([__import__("sys").executable, "-c", "pass"])
```

When integrating with Unix process groups, ensure only the parent calls `wait` on its own children to avoid `ECHILD`.

---

## Best practices

- Reap zombies in long-running parents (periodic `waitpid` with `WNOHANG` or structured subprocess usage).
- Do not confuse exit code failures (`CalledProcessError`) with `ChildProcessError` OS errno failures.
- On Windows, process APIs differ; many `ECHILD` scenarios do not apply.
