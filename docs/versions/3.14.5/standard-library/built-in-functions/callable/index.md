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

## Best practices

- Classes are callable (constructors); instances are callable only with `__call__`.
- For duck typing, prefer calling within try/except or use `typing.Protocol` for static checks.
- `callable()` was restored in Python 3.2 after removal in 3.0—prefer it over older `hasattr(x, "__call__")` patterns.
