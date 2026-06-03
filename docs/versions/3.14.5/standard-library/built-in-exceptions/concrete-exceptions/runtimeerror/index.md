# [RuntimeError](https://docs.python.org/3/library/exceptions.html#RuntimeError)

Raised when an error is detected that **does not fit a more specific** built-in category. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#RuntimeError).

---

## When it is raised

| Source | Example |
|--------|----------|
| Interpreter / stdlib | `list` modified during iteration, bad `__iter__` |
| Third-party libraries | Generic “something went wrong at runtime” |
| Legacy code | Before finer-grained types existed |

Several concrete types are **`RuntimeError` subclasses** (see below).

---

## Demonstrating raise and catch

```python
# Goal: RuntimeError is a catch-all Exception subclass
caught = None
try:
    raise RuntimeError('unexpected interpreter state')
except RuntimeError as exc:
    caught = str(exc)
assert caught == 'unexpected interpreter state'
assert issubclass(RuntimeError, Exception)
```

---

## Related subclasses in this repo

| Type | Purpose |
|------|---------|
| [`NotImplementedError`](notimplementederror/index.md) | Abstract / stub methods |
| [`RecursionError`](recursionerror/index.md) | Exceeded recursion limit |
| [`PythonFinalizationError`](pythonfinalizationerror/index.md) | Blocked during shutdown |

---

## Sections in this repo

- [NotImplementedError](notimplementederror/index.md)
- [RecursionError](recursionerror/index.md)
- [PythonFinalizationError](pythonfinalizationerror/index.md)

---

## Best practices

- Prefer a **specific** built-in or domain exception when one applies.
- Use `RuntimeError` for internal invariant violations in your own libraries when no better type exists.
