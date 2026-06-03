# [str()](https://docs.python.org/3/library/functions.html#func-str)

## Description

`str()` is the built-in text type constructor. With one argument it returns a readable string for an object (via `__str__` or `__repr__`). With bytes it decodes using an encoding (default UTF-8).

## What problem it solves

User-facing output, serialization to text, and bridging binary data (bytes) into Unicode strings all need a consistent text conversion path.

## Implementation options

### Convert values for display

```python
assert str(42) == "42"
assert str(3.14).startswith("3.14")
assert str(["a", "b"]) == "['a', 'b']"
```

### Decode bytes to text

```python
raw = bytes([0x63, 0x61, 0x66, 0xC3, 0xA9])
assert str(raw, encoding="utf-8") == "café"
```

### Custom `__str__` for readable output

```python
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __str__(self):
        return f"{self.major}.{self.minor}"

assert str(Version(3, 14)) == "3.14"
```

## Best practices

- Use `str()` for human-readable output; use `repr()` when debugging or logging needs ambiguity resolved.

  ```python
  from datetime import date

  d = date(2026, 5, 29)
  assert str(d) == "2026-05-29"
  assert repr(d) == "datetime.date(2026, 5, 29)"
  ```

  ```python
  # Incorrect for logs—loses type information:
  # log.debug(str(d))  # prefer repr(d) in tracebacks
  ```

- Always specify encoding when decoding bytes if the source encoding is not guaranteed UTF-8.

  ```python
  raw = "café".encode("utf-8")
  assert str(raw, encoding="utf-8") == "café"
  ```

  ```python
  # Incorrect on Windows or legacy data—default may not be UTF-8:
  # str(raw)  # encoding=None uses default codec
  ```

- Prefer f-strings for formatting when structure is known; use `str()` for generic object coercions.

  ```python
  major, minor = 3, 14
  assert f"{major}.{minor}" == "3.14"
  ```

  ```python
  class Version:
      def __str__(self):
          return "3.14"

  # str() dispatches __str__ for unknown object types:
  assert str(Version()) == "3.14"
  ```
