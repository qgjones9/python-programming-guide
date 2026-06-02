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
- Specify `file=` when testing print output with `io.StringIO`.
- `print` converts with `str()`—implement `__str__` on custom types for readable output.
