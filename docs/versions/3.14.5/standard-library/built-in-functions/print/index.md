# [print()](https://docs.python.org/3/library/functions.html#print)

## Description

`print(*objects, sep=' ', end='\n', file=None, flush=False)` converts objects to strings and writes them to `sys.stdout` by default. Keyword arguments control separators, line endings, output stream, and flushing.

## What problem it solves

Quick user feedback, logging prototypes, and formatted console output without manual `sys.stdout.write` calls.

## Implementation options

### Default printing and custom separator

```python
import io

buf = io.StringIO()
print("a", "b", "c", sep="-", file=buf)
assert buf.getvalue() == "a-b-c\n"
```

### Suppress trailing newline

```python
import io

buf = io.StringIO()
print("loading", end="", file=buf)
print(".", end="", file=buf)
assert buf.getvalue() == "loading."
```

### Print to stderr for diagnostics

```python
import io
import sys

err = io.StringIO()
print("warning: low disk", file=err)
assert "warning" in err.getvalue()
```

## Best practices

- Use the `logging` module for production diagnostics; `print` for scripts and quick debugging.

  ```python
  import logging

  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  logger.info("server started")  # levels, handlers, timestamps in production
  ```

  ```python
  # Fine for scripts and REPL exploration:
  print("quick check:", 2 + 2)
  ```

- Specify `file=` when testing print output with `io.StringIO`.

  ```python
  import io

  buf = io.StringIO()
  print("hello", file=buf)
  assert buf.getvalue() == "hello\n"
  ```

  ```python
  # Incorrect in tests—captures real stdout and is harder to assert:
  # print("hello")
  ```

- `print` converts with `str()`—implement `__str__` on custom types for readable output.

  ```python
  class Version:
      def __init__(self, major, minor):
          self.major = major
          self.minor = minor

      def __str__(self):
          return f"{self.major}.{self.minor}"

  buf = __import__("io").StringIO()
  print(Version(3, 14), file=buf)
  assert buf.getvalue().strip() == "3.14"
  ```

  ```python
  class Version:
      pass

  # Without __str__, print falls back to repr-like output:
  # print(Version())  # <__main__.Version object at 0x...>
  ```
