# [KeyError](https://docs.python.org/3/library/exceptions.html#KeyError)

Raised when a **mapping key is not found** among existing keys. Subclass of [`LookupError`](../base-classes/lookuperror/index.md). See [docs.python.org](https://docs.python.org/3/library/exceptions.html#KeyError).

---

## When it is raised

| Operation | Missing key |
|-----------|-------------|
| `d[key]` | **`KeyError`** |
| `d.get(key)` | Returns `None` (or default)—no exception |
| `d[key] = value` | Inserts key—never raises for missing key |

The exception message is the **repr of the key** (for example `'missing'`).

---

## Demonstrating raise and catch

```python
# Goal: KeyError on direct lookup; get() avoids it
data = {'a': 1}
caught = None
try:
    data['missing']
except KeyError as exc:
    caught = str(exc)
assert caught == "'missing'"
assert data.get('missing', 0) == 0
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `dict.get(key, default)` | Missing key is normal |
| `collections.defaultdict` | Every key should exist with a default |
| `except KeyError` | Translate to HTTP 404 or domain-specific error |

Related: [`IndexError`](indexerror/index.md), [`AttributeError`](attributeerror/index.md) (sometimes used after `getattr` translation).

---

## Best practices

- Do not use bare `except KeyError` to detect optional keys—use `.get()` instead.
- When re-raising as another type, consider `raise AttributeError(...) from None` to hide internal dict structure.
