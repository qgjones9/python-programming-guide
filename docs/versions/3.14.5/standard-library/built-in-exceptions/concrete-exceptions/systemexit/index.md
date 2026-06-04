# [SystemExit](https://docs.python.org/3/library/exceptions.html#SystemExit)

Raised by [`sys.exit()`](https://docs.python.org/3/library/sys.html#sys.exit) to terminate the interpreter. Inherits from [`BaseException`](../../base-classes/baseexception/index.md), not [`Exception`](../../base-classes/exception/index.md). See [docs.python.org](https://docs.python.org/3/library/exceptions.html#SystemExit).

---

## When it is raised

| Argument to `sys.exit()` | Exit status |
|--------------------------|-------------|
| `None` or `0` | Success (0) |
| Integer `n` | Status `n` |
| Other object | Printed, status 1 |

Unhandled: interpreter exits **without** traceback.

---

## The `code` attribute

Stores the value passed to the constructor (default `None`).

---

## Demonstrating raise and catch

```python
import sys

# Goal: SystemExit is BaseException; sys.exit raises it
assert issubclass(SystemExit, BaseException)
assert not issubclass(SystemExit, Exception)

caught = None
try:
    sys.exit(0)
except SystemExit as exc:
    caught = exc.code
assert caught == 0
```

---

## Best practices

- Use `sys.exit()` in CLI apps; let `SystemExit` propagate from `main`.
- Use [`os._exit()`](https://docs.python.org/3/library/os.html#os._exit) only when `finally` must not run (e.g. after `fork`).
- Related: [`KeyboardInterrupt`](../keyboardinterrupt/index.md).
