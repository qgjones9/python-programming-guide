# [hasattr()](https://docs.python.org/3/library/functions.html#hasattr)

## Description

Returns `True` if the object has the named attribute, otherwise `False` (implemented via `getattr` and `AttributeError`).

## What problem it solves

Optional features, duck typing, and plugin systems need to probe for capabilities before calling methods or reading properties.

## Implementation options

### Option 1: Duck-type a file-like object

```python
class Buffer:
    def read(self):
        return b"data"

def read_all(source):
    if hasattr(source, "read"):
        return source.read()
    return source

assert read_all(Buffer()) == b"data"
assert read_all(b"raw") == b"raw"
```

### Option 2: Check for optional protocol methods

```python
class Legacy:
    pass

class Modern:
    def close(self):
        pass

for obj in (Legacy(), Modern()):
    if hasattr(obj, "close"):
        obj.close()
```

## Best practices

- Race conditions exist: an attribute may disappear between `hasattr` and use in threaded code.
- For type checks, prefer `isinstance()` with ABCs (e.g. `collections.abc`) over attribute probing when possible.
- `getattr(obj, name, None) is not None` can distinguish missing attrs from attrs that exist but are `None`.
