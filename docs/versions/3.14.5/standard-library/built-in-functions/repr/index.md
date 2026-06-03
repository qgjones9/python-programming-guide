# [repr()](https://docs.python.org/3/library/functions.html#repr)

## Description

`repr()` returns a string containing a printable representation of an object. For many built-in types the result is meant to be unambiguous; for custom classes you control it via `__repr__()`.

## What problem it solves

Debugging, logging, and REPL inspection need a representation that distinguishes types and values—often one that could recreate the object when passed to `eval()`.

## Implementation options

### Inspect built-in values

```python
assert repr(42) == "42"
assert repr("hi") == "'hi'"
assert repr([1, 2]) == "[1, 2]"
```

### Define a custom `__repr__` for clarity

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x!r}, {self.y!r})"

p = Point(3, 4)
assert repr(p) == "Point(3, 4)"
rebuilt = eval(repr(p), {"Point": Point})
assert (rebuilt.x, rebuilt.y) == (p.x, p.y)
```

### Contrast `repr` (developer) with `str` (user-facing)

```python
from datetime import date

d = date(2026, 5, 29)
assert str(d) == "2026-05-29"
assert repr(d) == "datetime.date(2026, 5, 29)"
```

## Best practices

- Implement `__repr__` so it ideally returns an evaluable expression (`Point(x, y)` not `<Point object at 0x…>`).

  ```python
  class Point:
      def __init__(self, x, y):
          self.x, self.y = x, y

      def __repr__(self):
          return f"Point({self.x!r}, {self.y!r})"

  p = Point(3, 4)
  assert repr(p) == "Point(3, 4)"
  ```

  ```python
  class Point:
      def __init__(self, x, y):
          self.x, self.y = x, y

  # Default repr is unhelpful in logs:
  # repr(Point(1, 2))  # Point object at 0x...
  ```

- Use `repr()` in logs and tracebacks; use `str()` for end-user output.

  ```python
  from datetime import date

  d = date(2026, 5, 29)
  assert str(d) == "2026-05-29"
  assert repr(d) == "datetime.date(2026, 5, 29)"
  ```

  ```python
  # Incorrect for user-facing UI—too technical:
  # label = repr(d)
  ```

- Prefer f-strings with `!r` (`f"{value!r}"`) when embedding values in debug messages.

  ```python
  name = "ada"
  msg = f"unexpected {name!r}"
  assert msg == "unexpected 'ada'"
  ```

  ```python
  # Loses quotes—harder to spot empty or whitespace strings in logs:
  # msg = f"unexpected {name}"
  ```
