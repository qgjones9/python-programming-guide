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

### Option 3: Prefer iteration when `__iter__` exists

```python
class Row:
    def __iter__(self):
        return iter([1, 2, 3])

def sum_iterable(obj):
    if hasattr(obj, "__iter__"):
        return sum(obj)
    raise TypeError("not iterable")

assert sum_iterable(Row()) == 6
```

### Option 4: Distinguish missing attrs from `None`

```python
class Config:
    timeout = None

cfg = Config()
assert hasattr(cfg, "timeout")
assert getattr(cfg, "missing", "default") == "default"
```

## Best practices

- In threaded code, an attribute may disappear between `hasattr()` and use—prefer a single `getattr()` call or lock the object if needed.

  ```python
  class Resource:
      def read(self):
          return b"data"

  def read_all(source):
      reader = getattr(source, "read", None)
      if reader is None:
          return source
      return reader()

  assert read_all(Resource()) == b"data"
  assert read_all(b"raw") == b"raw"
  ```

- For type checks, prefer `isinstance()` with ABCs over attribute probing when a protocol is well defined.

  ```python
  import collections.abc

  def total(items):
      if isinstance(items, collections.abc.Iterable):
          return sum(items)
      raise TypeError("expected iterable")

  assert total([1, 2, 3]) == 6
  ```

  ```python
  import collections.abc

  class Row:
      def __iter__(self):
          return iter([1, 2, 3])

  # hasattr probes one method; isinstance checks the protocol:
  assert hasattr(Row(), "__iter__")
  assert isinstance(Row(), collections.abc.Iterable)
  ```

- `getattr(obj, name, None) is not None` distinguishes a missing attribute from one that exists but is `None`.

  ```python
  class Config:
      timeout = None

  cfg = Config()
  assert hasattr(cfg, "timeout")
  assert getattr(cfg, "missing", None) is None
  assert getattr(cfg, "timeout", None) is None  # attr exists, value is None
  ```
