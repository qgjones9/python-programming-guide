# [callable()](https://docs.python.org/3/library/functions.html#callable)

## Description

`callable()` returns `True` if the object appears callable—functions, methods, classes, and instances with `__call__()`. A `True` result does not guarantee every call will succeed.

## What problem it solves

Plugin systems, callbacks, and generic dispatch need to know whether `obj()` is syntactically valid before invoking. `callable()` offers a quick guard without try/except around every call site.

## Implementation options

### Distinguishing callables from data

```python
assert callable(print)
assert callable(str)
assert not callable(42)
assert not callable("hello")

class Adder:
    def __call__(self, x, y):
        return x + y

adder = Adder()
assert callable(adder)
assert adder(2, 3) == 5
```

### Safe callback invocation

```python
def invoke(maybe_fn, *args, default=None):
    if callable(maybe_fn):
        return maybe_fn(*args)
    return default

assert invoke(lambda x: x * 2, 4) == 8
assert invoke(None, 4) is None
```

### Classes are callable constructors

```python
class Box:
    def __init__(self, value):
        self.value = value

assert callable(Box)
instance = Box(7)
assert instance.value == 7
```

## Best practices

- Classes are callable (constructors); instances are callable only with `__call__`.

  ```python
  class Box:
      def __init__(self, value):
          self.value = value

  box = Box(3)
  assert callable(Box)
  assert not callable(box)

  class CallableBox:
      def __call__(self):
          return 1

  assert callable(CallableBox())
  ```

- For duck typing at runtime, prefer calling within try/except over `callable()` when failure is expected.

  ```python
  def invoke(maybe_fn, arg):
      if callable(maybe_fn):
          return maybe_fn(arg)
      return maybe_fn  # already a value

  assert invoke(len, "hi") == 2
  assert invoke(42, None) == 42
  ```

- `callable()` is clearer than `hasattr(x, "__call__")` for deciding whether to invoke an object.

  ```python
  class Greeter:
      def greet(self):
          return "hi"

  obj = Greeter()
  assert not callable(obj)
  assert callable(obj.greet)
  assert callable(len)
  ```
