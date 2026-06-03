# [dir()](https://docs.python.org/3/library/functions.html#dir)

## Description

Returns a sorted list of names in the current local scope, or valid attribute names for a given object.

## What problem it solves

When exploring unfamiliar modules, classes, or objects in the REPL, you need a quick way to discover available names without reading source code or documentation.

## Implementation options

### Option 1: Inspect a module's public API

```python
import json

names = [n for n in dir(json) if not n.startswith("_")]
assert "loads" in names
assert "dumps" in names
```

### Option 2: Customize discovery with __dir__

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

## Best practices

- Use `dir()` interactively to explore APIs; prefer `help()` or official docs for production code.
- Filter out names starting with `_` when presenting public interfaces to users.
- Remember that `dir()` output may vary across Python versions and is not a formal API contract.
