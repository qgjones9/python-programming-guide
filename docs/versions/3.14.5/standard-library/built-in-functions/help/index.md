# [help()](https://docs.python.org/3/library/functions.html#help)

## Description

Invokes the interactive help system for modules, functions, classes, keywords, or any object with documentation.

## What problem it solves

In the REPL or while learning a library, you need quick access to docstrings and signatures without leaving the terminal.

## Implementation options

### Option 1: Capture `help()` output for a built-in

```python
import contextlib
import io

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    help(len)
text = buf.getvalue()
assert "Return the number of items" in text or "__len__" in text
```

### Option 2: Help for a module or function object

```python
import json
import contextlib
import io

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    help(json.dumps)
text = buf.getvalue()
assert "dumps" in text
assert callable(json.dumps)
```

### Option 3: Docstrings on custom classes appear in help

```python
class Account:
    """Track a simple bank balance."""

    def deposit(self, amount: float) -> None:
        """Add funds to the account."""
        pass

import contextlib
import io

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    help(Account)
assert "bank balance" in buf.getvalue()
```

### Option 4: Non-interactive alternative with `inspect`

```python
import inspect

def describe(obj):
    return inspect.getdoc(obj) or ""

assert "Return the number of items" in describe(len)
```

## Best practices

- Use `help(obj)` in the interactive interpreter; in scripts, prefer `inspect.getdoc()` or official docs.

  ```python
  import inspect

  doc = inspect.getdoc(len) or ""
  assert "Return the number of items" in doc or "__len__" in doc
  ```

  ```python
  # In the REPL, this is ideal:
  # >>> help(dict)
  ```

- Write clear docstrings on public APIs—`help()` displays them to users and teammates.

  ```python
  def connect(host: str, port: int = 443) -> None:
      """Open a TLS connection to host on port."""
      pass

  assert "TLS connection" in (connect.__doc__ or "")
  ```

- A slash (`/`) in signatures shown by `help()` marks positional-only parameters (Python 3.8+).

  ```python
  def demo(a, /, b):
      return a + b

  import inspect

  sig = inspect.signature(demo)
  assert sig.parameters["a"].kind.name == "POSITIONAL_ONLY"
  ```
