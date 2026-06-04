# [ImportError](https://docs.python.org/3/library/exceptions.html#ImportError)

Raised when an `import` statement cannot load a module or resolve a name in `from module import name`. Full reference: [docs.python.org](https://docs.python.org/3/library/exceptions.html#ImportError). Since 3.6, missing modules usually surface as [`ModuleNotFoundError`](../modulenotfounderror/index.md) instead.

---

## When it is raised

| Situation | Typical exception today |
|-----------|-------------------------|
| Module file missing | `ModuleNotFoundError` |
| Name missing in `from m import x` | `ImportError` |
| Circular import partial init | `ImportError` or `AttributeError` |
| Invalid relative import | `ImportError` |

---

## Exception attributes (3.3+)

| Attribute | Meaning |
|-----------|----------|
| `name` | Module name attempted |
| `path` | Path that triggered the failure, if any |

---

## Demonstrating raise and catch

```python
# Goal: ImportError carries a message; subclass for missing modules
try:
    raise ImportError('cannot import name foo from bar')
except ImportError as exc:
    assert 'foo' in str(exc)
assert issubclass(ModuleNotFoundError, ImportError)
```

---

## Best practices

- Catch `ModuleNotFoundError` for optional dependencies; use `ImportError` when you want both import failure modes.
- Re-raise with `raise ... from exc` to preserve context when wrapping import failures.
- Avoid bare `except` around imports—log the module name from `exc.name` when available.

---

## Sections in this repo

- [ModuleNotFoundError](../modulenotfounderror/index.md)
