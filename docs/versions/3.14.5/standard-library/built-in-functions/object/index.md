# [object()](https://docs.python.org/3/library/functions.html#object)

## Description

`object()` returns a new featureless object—the root of Python's class hierarchy. All classes inherit from `object`. Instances of bare `object()` have no `__dict__` and cannot receive arbitrary attributes.

## What problem it solves

Understanding inheritance, creating minimal sentinel instances, and anchoring the type system—every user-defined class ultimately derives from `object`.

## Implementation options

### Create a unique sentinel

```python
MISSING = object()
cache = {}

def get(key, default=MISSING):
    if key in cache:
        return cache[key]
    if default is not MISSING:
        return default
    raise KeyError(key)

assert get("x", default=0) == 0
```

### All classes subclass object

```python
class Widget:
    pass

assert issubclass(Widget, object)
assert isinstance(Widget(), object)
```

### Bare object rejects arbitrary attributes

```python
bare = object()
try:
    bare.x = 1
    raised = False
except AttributeError:
    raised = True
assert raised
```

## Best practices

- Use a unique `object()` sentinel instead of `None` when `None` is valid data.

  ```python
  MISSING = object()

  def lookup(key, cache, default=MISSING):
      if key in cache:
          return cache[key]
      if default is not MISSING:
          return default
      raise KeyError(key)

  cache = {"x": None}
  assert lookup("x", cache) is None
  assert lookup("y", cache, default=0) == 0
  ```

  ```python
  # Incorrect when None is valid data—cannot distinguish missing from None:
  # MISSING = None
  # lookup("x", {"x": None}, default=MISSING)  # ambiguous
  ```

- Subclass `object` explicitly only when teaching—in Python 3 it is implicit.

  ```python
  class Widget:
      pass

  assert issubclass(Widget, object)
  ```

  ```python
  # Redundant in Python 3—new-style classes already inherit object:
  # class Widget(object):
  #     pass
  ```

- For rich instances, define a proper class instead of using bare `object()`.

  ```python
  class Point:
      __slots__ = ("x", "y")

      def __init__(self, x, y):
          self.x = x
          self.y = y

  p = Point(1, 2)
  assert (p.x, p.y) == (1, 2)
  ```

  ```python
  bare = object()
  # Incorrect—bare object() cannot hold arbitrary attributes:
  # bare.x = 1  # AttributeError
  ```
