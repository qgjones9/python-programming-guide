# [AttributeError](https://docs.python.org/3/library/exceptions.html#AttributeError)

Raised when **attribute reference or assignment** fails on an object. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#AttributeError). If the object does not support attributes at all, Python raises [`TypeError`](../typeerror/index.md) instead.

---

## When it is raised

| Cause | Example |
|-------|----------|
| Missing attribute | `obj.missing` on a plain instance |
| Failed `__getattr__` | Custom classes that re-raise or omit attrs |
| Wrong descriptor | Descriptor `__get__` raises or returns failure |

---

## Attributes on the exception (3.10+)

| Attribute | Meaning |
|-----------|----------|
| `name` | Attribute name that was accessed |
| `obj` | Object on which access was attempted |

---

## Demonstrating raise and catch

```python
# Goal: missing attribute sets name/obj and is catchable
class Box:
    pass

box = Box()
try:
    box.color
except AttributeError as exc:
    assert exc.name == 'color'
    assert exc.obj is box
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `getattr(obj, 'name', default)` | Optional attribute with fallback |
| `hasattr` then access | Duck-typing probe (beware `__getattr__` side effects) |
| `except AttributeError` | Translate to domain error or retry path |

Related: [`TypeError`](../typeerror/index.md) (unsupported operation), [`NameError`](../nameerror/index.md) (undefined name, not missing attr).
