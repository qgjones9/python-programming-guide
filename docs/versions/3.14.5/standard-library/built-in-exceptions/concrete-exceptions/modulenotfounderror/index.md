# [ModuleNotFoundError](https://docs.python.org/3/library/exceptions.html#ModuleNotFoundError)

Subclass of [`ImportError`](../importerror/index.md) raised when `import` cannot locate a module or finds `None` in `sys.modules`. Added in Python 3.6 ([docs.python.org](https://docs.python.org/3/library/exceptions.html#ModuleNotFoundError)).

---

## When it is raised

| Cause | Example |
|-------|----------|
| Package not installed | `import nonexistent_pkg` |
| Wrong `PYTHONPATH` | Project root not on path |
| Typo in module name | `import jsonn` |
| `None` in `sys.modules` | Broken loader left placeholder |

---

## Demonstrating raise and catch

```python
# Goal: catch ModuleNotFoundError separately from other ImportError
def classify(exc):
    if isinstance(exc, ModuleNotFoundError):
        return 'missing module'
    if isinstance(exc, ImportError):
        return 'import problem'
    return 'other'

assert classify(ModuleNotFoundError('No module named x')) == 'missing module'
assert classify(ImportError('bad relative import')) == 'import problem'
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `except ModuleNotFoundError` | Optional dependency with install hint |
| `except ImportError` | Handle missing modules and bad `from` imports |
| Fix `PYTHONPATH` / venv | Deployment or packaging misconfiguration |

Related: [`ImportError`](../importerror/index.md).

---

## Best practices

- Catch `ModuleNotFoundError` for optional dependencies; fall back or re-raise with install instructions.
- Use `except ImportError` when you want to handle **both** this type and other import failures.
- Parent page: [`ImportError`](../importerror/index.md).
