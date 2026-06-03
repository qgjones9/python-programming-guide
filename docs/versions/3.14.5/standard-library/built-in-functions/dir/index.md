# [dir()](https://docs.python.org/3/library/functions.html#dir)

## Description

`dir()` returns a sorted list of names. Called with no arguments, it lists names in the current local scope; with an object, it returns attribute names the object exposes (after calling `__dir__()` when defined).

## What problem it solves

Exploring unfamiliar modules, classes, or instances in the REPL means discovering what you can call without reading source. `dir()` is the quick discovery tool—pair it with `help()` when you need docstrings.

## Implementation options

### Inspect a module's public API

```python
import json

names = [n for n in dir(json) if not n.startswith("_")]
assert "loads" in names
assert "dumps" in names
```

### Customize discovery with `__dir__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __dir__(self):
        return ["x", "y", "distance"]

p = Point(3, 4)
assert sorted(dir(p)) == ["distance", "x", "y"]
```

### Names visible in the current scope

```python
def demo():
    local_var = 42
    names = dir()
    assert "local_var" in names
    return names

assert "demo" in dir()  # function defined at module level
assert "local_var" in demo()
```

## Best practices

- Use `dir()` interactively to explore APIs; prefer `help()` or official docs for production code.

  ```python
  names = dir(str)
  assert "split" in names
  # In libraries, document public API explicitly instead of dir()-driven discovery
  ```

- Filter out names starting with `_` when presenting public interfaces to users.

  ```python
  class Service:
      def run(self):
          return "ok"

      def _internal(self):
          return "hidden"

  public = [n for n in dir(Service) if not n.startswith("_")]
  assert "run" in public
  assert "_internal" not in public
  ```

- Remember that `dir()` output may vary across Python versions and is not a formal API contract.

  ```python
  # fine for REPL exploration
  assert "append" in dir([])

  # do not treat dir() as a stable public API surface
  PUBLIC = ("run",)  # document explicitly instead
  assert "run" in PUBLIC
  ```
