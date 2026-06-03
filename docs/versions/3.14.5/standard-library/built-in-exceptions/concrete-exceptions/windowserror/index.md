# [WindowsError](https://docs.python.org/3/library/exceptions.html#WindowsError)

**Windows-only compatibility alias** of [`OSError`](oserror/index.md) since Python 3.3. On other platforms the name exists for compatibility but is not Windows-specific. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#WindowsError).

---

## Relationship

| Platform | Behavior |
|----------|----------|
| Windows | Alias of `OSError`; may carry `winerror` |
| POSIX | Name available; alias of `OSError` |

---

## Demonstrating alias identity

```python
import builtins

# Goal: on Windows, WindowsError is OSError; elsewhere document the alias
if hasattr(builtins, 'WindowsError'):
    assert WindowsError is OSError
exc = OSError(3, 'path not found')
assert exc.errno == 3
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `except OSError as exc` | Read `exc.winerror` on Windows for native codes |
| `except WindowsError` | Legacy handlers only—identical to `OSError` on 3.3+ |
| Catch `PermissionError`, etc. | Prefer PEP 3151 subclasses over errno inspection |

Related: [`OSError`](oserror/index.md), [`EnvironmentError`](environmenterror/index.md).

---

## Best practices

- Use [`OSError`](oserror/index.md) with `winerror` / `errno` attributes instead of `WindowsError` in new code.
- Parent: [`OSError`](oserror/index.md).
