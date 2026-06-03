# [getattr()](https://docs.python.org/3/library/functions.html#getattr)

## Description

Returns the value of a named attribute on an object; with a default, returns that instead of raising `AttributeError`.

## What problem it solves

Attribute names may come from configuration, user input, or reflection—you need safe dynamic lookup without repetitive `try/except` blocks.

## Implementation options

### Option 1: Read optional config attributes

```python
class Config:
    host = "localhost"
    port = 8080

timeout = getattr(Config, "timeout", 30)
assert timeout == 30
assert Config.host == "localhost"
```

### Option 2: Dispatch by method name

```python
class Greeter:
    def hello(self):
        return "Hello"

    def goodbye(self):
        return "Goodbye"

g = Greeter()
fn = getattr(g, "hello")
assert fn() == "Hello"
```

## Best practices

- Prefer dot notation (`obj.attr`) when the attribute name is known at compile time.
- Use the three-argument form `getattr(obj, name, default)` instead of catching `AttributeError` for missing optional attrs.
- For private mangled names (`__attr`), manually prefix with `_ClassName` when using `getattr()`.
