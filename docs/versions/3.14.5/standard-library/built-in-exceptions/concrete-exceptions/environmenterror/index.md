# [EnvironmentError](https://docs.python.org/3/library/exceptions.html#EnvironmentError)

**Compatibility alias** of [`OSError`](oserror/index.md) since Python 3.3. Kept so older code catching `EnvironmentError` continues to work. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#EnvironmentError).

---

## Relationship

| Name | Status since 3.3 |
|------|------------------|
| `EnvironmentError` | Alias of `OSError` |
| `IOError` | Alias of `OSError` |
| `WindowsError` | Alias of `OSError` (Windows only) |

---

## Demonstrating alias identity

```python
# Goal: EnvironmentError is OSError where the alias exists
import builtins

if hasattr(builtins, 'EnvironmentError'):
    assert EnvironmentError is OSError
exc = OSError(2, 'No such file', '/tmp/x')
assert exc.errno == 2
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `except OSError` | New code—covers legacy `EnvironmentError` handlers too |
| `except EnvironmentError` | Maintaining pre-3.3 libraries without renaming |
| Catch `FileNotFoundError`, etc. | Known filesystem operations |

Related: [`IOError`](ioerror/index.md), [`WindowsError`](windowserror/index.md), [`OSError`](oserror/index.md).

---

## Best practices

- Write new code against [`OSError`](oserror/index.md) and PEP 3151 subclasses (`FileNotFoundError`, etc.).
- When maintaining Python 2/3 straddling code, `EnvironmentError` may still appear in `except` clauses—safe on 3.x.
