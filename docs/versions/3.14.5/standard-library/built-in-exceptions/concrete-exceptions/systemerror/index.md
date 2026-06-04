# [SystemError](https://docs.python.org/3/library/exceptions.html#SystemError)

Raised when the interpreter finds an **internal error** that is not fatal enough to abort immediately. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#SystemError).

---

## When it is raised

| Source | Meaning |
|--------|---------|
| CPython C API misuse | e.g. returning `NULL` without setting an exception |
| Interpreter bug | Should be reported with `sys.version` and traceback |

Not caused by ordinary Python application mistakes.

---

## Demonstrating raise and catch

```python
# Goal: SystemError is catchable like other Exception subclasses
caught = None
try:
    raise SystemError('internal interpreter fault (demo)')
except SystemError as exc:
    caught = str(exc)
assert 'internal' in caught
assert issubclass(SystemError, Exception)
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| Do not catch in app code | Treat as interpreter bug unless you wrap C extensions |
| Log and re-raise | Extension boundary where recovery is impossible |
| Report upstream | Include `sys.version` and minimal repro |

Related: [`SystemExit`](../systemexit/index.md), [`RuntimeError`](../runtimeerror/index.md).

---

## Best practices

- If you did not misuse the C API, report to [Python issue tracker](https://github.com/python/cpython/issues) with reproduction steps.
- Do not confuse with [`SystemExit`](../systemexit/index.md) or [`RuntimeError`](../runtimeerror/index.md).
