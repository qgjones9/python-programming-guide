# [format()](https://docs.python.org/3/library/functions.html#format)

## Description

Converts a value to a formatted string according to a format specification, delegating to `type(value).__format__()`.

## What problem it solves

Displaying numbers, dates, and aligned columns requires controlled string representation beyond plain `str()`.

## Implementation options

### Option 1: Format numbers with precision and grouping

```python
pi = 3.14159265
assert format(pi, ".2f") == "3.14"
assert format(1_000_000, ",") == "1,000,000"
```

### Option 2: Pad and align text in columns

```python
rows = [("Alice", 95), ("Bob", 87)]
lines = [f"{name:<10}{format(score, '3d')}" for name, score in rows]
assert lines[0] == "Alice      95"
```

### Option 3: Binary, hex, and percentage display

```python
n = 42
assert format(n, "b") == "101010"
assert format(n, "#x") == "0x2a"
assert format(0.875, ".1%") == "87.5%"
```

### Option 4: Custom `__format__` on a class

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __format__(self, spec):
        if spec == "coords":
            return f"({self.x}, {self.y})"
        return repr(self)

p = Point(3, 4)
assert format(p, "coords") == "(3, 4)"
```

## Best practices

- f-strings are usually more readable than `format()` for simple cases; use `format()` when the spec string is computed or reused.

  ```python
  value = 3.14159
  assert f"{value:.2f}" == "3.14"
  ```

  ```python
  spec = ".2f"
  value = 3.14159
  assert format(value, spec) == "3.14"
  ```

- Learn the [format specification mini-language](https://docs.python.org/3/library/string.html#formatspec) for reusable patterns like alignment and grouping.

  ```python
  rows = [("Alice", 95), ("Bob", 87)]
  lines = [f"{name:<10}{format(score, '3d')}" for name, score in rows]
  assert lines[0] == "Alice      95"
  assert format(1_000_000, ",") == "1,000,000"
  ```

- Custom classes can implement `__format__()` to support format specs in both f-strings and `format()`.

  ```python
  class Point:
      def __init__(self, x, y):
          self.x, self.y = x, y

      def __format__(self, spec):
          if spec == "coords":
              return f"({self.x}, {self.y})"
          return repr(self)

  p = Point(3, 4)
  assert format(p, "coords") == "(3, 4)"
  assert f"{p:coords}" == "(3, 4)"
  ```
