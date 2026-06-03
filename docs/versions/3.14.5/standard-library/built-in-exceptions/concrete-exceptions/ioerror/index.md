# [IOError](https://docs.python.org/3/library/exceptions.html#IOError)

**Compatibility alias** of [`OSError`](oserror/index.md) since Python 3.3. Historically distinguished I/O errors from `OSError`; the hierarchies were merged (PEP 3151). See [docs.python.org](https://docs.python.org/3/library/exceptions.html#IOError).

---

## Relationship

| Name | Status since 3.3 |
|------|------------------|
| `IOError` | Alias of `OSError` |
| `EnvironmentError` | Alias of `OSError` |

---

## Demonstrating alias identity

```python
import builtins

# Goal: IOError is OSError where the alias exists
if hasattr(builtins, 'IOError'):
    assert IOError is OSError
caught = None
try:
    raise OSError('read failed')
except OSError:
    caught = 'os'
assert caught == 'os'
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `except OSError` | Modern replacement for broad I/O failure handling |
| `except IOError` | Legacy tutorials and Python 2 ports—same as `OSError` |
| `except FileNotFoundError` | Missing path is the expected failure mode |

Related: [`OSError`](oserror/index.md), [`EnvironmentError`](environmenterror/index.md).

---

## Best practices

- Prefer `OSError` and specific subclasses in new code.
- Tutorial and legacy examples may still say `IOError`; behavior is identical on Python 3.
