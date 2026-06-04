# [ReferenceError](https://docs.python.org/3/library/exceptions.html#ReferenceError)

Raised when a **weak reference proxy** accesses an attribute after the referent has been garbage collected. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#ReferenceError) and the [`weakref`](https://docs.python.org/3/library/weakref.html) module.

---

## When it is raised

| Trigger | Notes |
|---------|-------|
| `weakref.proxy(obj).attr` after `obj` collected | Proxy cannot forward |
| Not raised for `weakref.ref` callbacks | Callback receives `None` instead |

---

## Demonstrating raise and catch

```python
# Goal: proxy raises ReferenceError after referent is gone
import weakref

class Thing:
    value = 42

obj = Thing()
proxy = weakref.proxy(obj)
assert proxy.value == 42
del obj

caught = None
try:
    proxy.value
except ReferenceError:
    caught = 'gone'
assert caught == 'gone'
```

---

## Best practices

- Prefer plain weak references when you can test for `None` instead of catching `ReferenceError`.
- Related: [`AttributeError`](../attributeerror/index.md) on live objects.
