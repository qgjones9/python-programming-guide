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

### Option 3: Chain lookups with a default factory pattern

```python
class Settings:
    theme = "dark"

cfg = Settings()
debug = getattr(cfg, "debug", False)
assert debug is False
assert getattr(cfg, "theme") == "dark"
```

### Option 4: Bound method from a string name

```python
class Calculator:
    def add(self, a, b):
        return a + b

calc = Calculator()
method = getattr(calc, "add")
assert method(2, 3) == 5
```

## Best practices

- Prefer dot notation when the attribute name is known at compile time; use `getattr()` when the name is dynamic.

  ```python
  class Config:
      host = "localhost"

  cfg = Config()
  assert cfg.host == "localhost"
  ```

  ```python
  class Config:
      host = "localhost"

  name = "host"
  cfg = Config()
  assert getattr(cfg, name) == "localhost"
  ```

- Use the three-argument form `getattr(obj, name, default)` instead of catching `AttributeError` for missing optional attrs.

  ```python
  class Config:
      host = "localhost"

  cfg = Config()
  timeout = getattr(cfg, "timeout", 30)
  assert timeout == 30
  ```

  ```python
  class Config:
      host = "localhost"

  cfg = Config()
  try:
      getattr(cfg, "timeout")
  except AttributeError:
      timeout = 30
  else:
      raise AssertionError("expected AttributeError")
  assert timeout == 30
  ```

- For name-mangled attributes (`__attr`), prefix with `_ClassName` when using `getattr()`.

  ```python
  class Widget:
      def __init__(self):
          self.__secret = 42

  w = Widget()
  assert getattr(w, "_Widget__secret") == 42
  assert not hasattr(w, "__secret")
  ```
