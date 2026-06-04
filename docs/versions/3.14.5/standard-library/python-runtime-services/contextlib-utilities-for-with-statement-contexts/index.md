# [contextlib — Utilities for with-statement contexts](https://docs.python.org/3/library/contextlib.html)

[`contextlib`](https://docs.python.org/3/library/contextlib.html) supplies **helpers for `with` statements**: decorators that turn generator functions into context managers, utilities to suppress exceptions, redirect streams, and stack multiple contexts (`ExitStack`, `AsyncExitStack`). Reference: [docs.python.org](https://docs.python.org/3/library/contextlib.html).

---

## Core utilities

| Name | Role |
|------|------|
| `@contextmanager` | Generator-based context manager decorator |
| `closing(thing)` | Calls `.close()` on exit |
| `suppress(*exceptions)` | Ignore listed exception types |
| `redirect_stdout` / `redirect_stderr` | Temporarily swap stream targets |
| `ExitStack` / `AsyncExitStack` | Dynamic `with` nesting |
| `nullcontext(enter_result=None)` | No-op context for optional managers |

---

## `@contextmanager` pattern — [Replacing try-finally](https://docs.python.org/3/library/contextlib.html#replacing-any-use-of-try-finally-and-flag-variables)

```python
# Goal: timer context using yield split
import contextlib
import time

@contextlib.contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        assert elapsed >= 0

with timer("block"):
    total = sum(range(100))
    assert total == 4950
```

Code before `yield` runs on enter; the `finally` block runs on exit (even on exceptions).

---

## Exception handling contexts

`suppress(FileNotFoundError)` replaces empty `except FileNotFoundError: pass`. For `__enter__` failures, `contextlib` documents patterns to catch and wrap errors from context manager entry.

---

## Reentrant and reusable managers — [Single use, reusable and reentrant context managers](https://docs.python.org/3/library/contextlib.html#single-use-reusable-and-reentrant-context-managers)

Generator-based managers are **single-use** unless decorated with `@contextmanager` on a class implementing reusable protocol. `ExitStack` handles arbitrary dynamic cleanup ordering (LIFO).

```python
# Goal: suppress expected exception
import contextlib

with contextlib.suppress(ZeroDivisionError):
    _ = 1 / 0
assert True  # reached after suppressed error
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`closing`** over manual `.close()` in `finally` | Shorter and exception-safe |
| Use **`ExitStack`** in multi-resource setup | One failure path closes earlier resources |
| Keep generator managers **yield exactly once** | Multiple yields break protocol |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Forgetting `try/finally` around `yield` | Cleanup skipped on exception | Always wrap post-yield cleanup in `finally` |
| Re-entering single-use `@contextmanager` | RuntimeError | Instantiate fresh manager or use class-based CM |

---

## See also

- [Context Manager Types](https://docs.python.org/3/reference/datamodel.html#context-managers) — language reference
- [`warnings`](../warnings-warning-control/index.md) — often paired with `catch_warnings`
