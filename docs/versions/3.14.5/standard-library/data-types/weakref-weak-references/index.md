# [weakref — Weak references](https://docs.python.org/3/library/weakref.html)

The [`weakref`](https://docs.python.org/3/library/weakref.html) module creates **weak references** that do not keep objects alive. When only weak refs remain, garbage collection can reclaim the referent and weak mappings drop entries automatically. Use weak containers for caches, registries keyed by objects, and **`finalize`** cleanup hooks that outlive arbitrary `__del__` behavior. Full proxy and finalizer comparisons are on [docs.python.org](https://docs.python.org/3/library/weakref.html).

Not all types support weak refs (e.g. plain `list`, `dict`, `int`, `tuple` — though `dict`/`list` subclasses can enable it).

---

## Core API

| Name | Role |
|------|------|
| `weakref.ref(obj[, callback])` | Callable weak reference; returns `None` when dead |
| `weakref.proxy(obj[, callback])` | Transparent proxy; `ReferenceError` when dead |
| `getweakrefcount(obj)` | Count of weak refs to object |
| `getweakrefs(obj)` | List weak ref/proxy objects |
| `WeakMethod(method)` | Weak ref to bound method (rebinds while obj lives) |

Always test liveness with `ref() is not None` — not a separate boolean flag (thread-safe idiom).

```python
# Goal: weak ref returns None after object collected
import weakref

class Blob:
    pass

obj = Blob()
ref = weakref.ref(obj)
assert ref() is obj
del obj
assert ref() is None
```

---

## Weak containers

| Class | Eviction policy |
|-------|-----------------|
| `WeakKeyDictionary` | Entry removed when **key** collected |
| `WeakValueDictionary` | Entry removed when **value** collected |
| `WeakSet` | Element removed when object collected |

```python
# Goal: cache by object id without pinning objects
import gc
import weakref

_id2obj = weakref.WeakValueDictionary()

class Resource:
    pass

r = Resource()
oid = id(r)
_id2obj[oid] = r
assert _id2obj[oid] is r
del r
gc.collect()
assert oid not in _id2obj
```

---

## finalize — [Finalizer Objects](https://docs.python.org/3/library/weakref.html#finalizer-objects)

| Attribute / method | Role |
|--------------------|------|
| `finalize(obj, func, *args, **kwargs)` | Register one-shot callback at GC |
| `.alive` | Whether callback not yet run |
| `.detach()` | Unregister and return `(obj, func, args, kwargs)` |
| `.atexit` | If true (default), run at interpreter exit |

Avoid closing over `obj` in `func` if `func` is bound to `obj` — circular keep-alive.

```python
# Goal: run cleanup once when object is collected
import weakref

log = []

class Handle:
    pass

h = Handle()
fin = weakref.finalize(h, log.append, "closed")
assert fin.alive
del h
assert "closed" in log
assert not fin.alive
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`WeakValueDictionary` caches** | Large values drop when unused |
| Use **`finalize` over raw ref callbacks** | Finalizer stays alive until called |
| Subclass **`dict`/`list` for weak keys** | Built-ins lack weakref support |
| Add **`'__weakref__'` to `__slots__`** | Enables weak refs on slotted classes |
| Check **`ref() is not None`** before use | Race-free in threaded code |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `WeakKeyDictionary` equal keys | Replacement drops entry | `del d[k1]` before new key |
| `proxy` as dict key | Not hashable | Use `ref()` explicitly |
| `finalize` capturing `obj` in closure | Never collected | Pass only external resources |
| Expecting immediate callback | Runs at GC time | Do not rely on prompt cleanup |
| Weak refs to `str`/`int` interned objects | May never run | Weak-ref mutable/user types |

---

## See also

- [PEP 205](https://peps.python.org/pep-0205/) — weak references
- [`copy`](../copy-shallow-and-deep-copy-operations/index.md) — strong copies vs weak caches
