# [NameError](https://docs.python.org/3/library/exceptions.html#NameError)

Raised when a **local or global name is not found** (unqualified names only). See [docs.python.org](https://docs.python.org/3/library/exceptions.html#NameError). Since 3.10 the exception exposes a `name` attribute.

---

## When it is raised

| Cause | Example |
|-------|----------|
| Undefined variable | Reference before assignment in global scope |
| Misspelled name | `pritn('hi')` |
| Deleted name | `del x` then use `x` |
| Not for missing attributes | Use [`AttributeError`](attributeerror/index.md) instead |

---

## Exception attribute (3.10+)

| Attribute | Meaning |
|-----------|----------|
| `name` | Variable name that could not be found |

---

## Demonstrating raise and catch

```python
# Goal: NameError includes the missing name
ns: dict[str, object] = {}
code = """
try:
    undefined_symbol
except NameError as exc:
    result = exc.name
"""
exec(code, ns, ns)
assert ns['result'] == 'undefined_symbol'
```

---

## Sections in this repo

- [UnboundLocalError](unboundlocalerror/index.md)

---

## Best practices

- Fix the underlying typo or import; do not catch `NameError` in production paths except for dynamic evaluation (`eval` / template engines).
- Distinguish from [`UnboundLocalError`](unboundlocalerror/index.md) when a local is referenced before assignment.
