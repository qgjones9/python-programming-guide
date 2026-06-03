# [help()](https://docs.python.org/3/library/functions.html#help)

## Description

Invokes the interactive help system for modules, functions, classes, keywords, or any object with documentation.

## What problem it solves

In the REPL or while learning a library, you need quick access to docstrings and signatures without leaving the terminal.

## Implementation options

### Option 1: Look up a function's docstring programmatically

```python
import json

doc = help.__class__  # help is an instance; use pydoc via help() interactively
# In the REPL: help(json.loads)

assert callable(json.loads)
assert json.loads.__doc__ is not None
```

### Option 2: Inspect a custom class

```python
class Account:
    """Track a simple bank balance."""

    def deposit(self, amount: float) -> None:
        """Add funds to the account."""
        pass

assert "bank balance" in Account.__doc__
```

## Best practices

- Use `help(obj)` in the interactive interpreter; in scripts, prefer reading docs or `inspect.getdoc()`.
- Write clear docstrings on public APIs—`help()` displays them to users and teammates.
- A slash (`/`) in signatures shown by `help()` marks positional-only parameters.
