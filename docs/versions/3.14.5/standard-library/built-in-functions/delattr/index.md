# [delattr()](https://docs.python.org/3/library/functions.html#delattr)

## Description

`delattr(object, name)` deletes the named attribute from an object when deletion is allowed. It is equivalent to `del object.name`. The name string need not be a valid Python identifier.

## What problem it solves

Metaprogramming, cleanup routines, and serializers sometimes remove attributes dynamically—especially when names are computed at runtime. `delattr()` mirrors `setattr()` and `getattr()` for the delete operation.

## Implementation options

### Dynamic attribute removal

```python
class Config:
    pass

cfg = Config()
cfg.debug = True
cfg.verbose = False
assert hasattr(cfg, "debug")

delattr(cfg, "debug")
assert not hasattr(cfg, "debug")
assert hasattr(cfg, "verbose")
```

### Computed attribute names

```python
class Cache:
    def __init__(self):
        self._store = {}

cache = Cache()
setattr(cache, "item_42", "value")
key = "item_42"
delattr(cache, key)
assert not hasattr(cache, "item_42")
```

## Best practices

- Prefer plain `del obj.attr` when the attribute name is known statically—it is clearer.
- Deletion may fail with `AttributeError` (missing) or `TypeError` (non-deletable slots/properties).
- For user-controlled names, validate against an allowlist to avoid deleting critical internals.
