# [Invoking the Interpreter](https://docs.python.org/3/tutorial/interpreter.html#invoking-the-interpreter)

Condensed notes for **§2.1** of [Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html): how **`python`** chooses between script mode, **`-c`**, **`-m`**, and stdin; and how interactive prompts behave.

```python
# `sys.executable` points at the running interpreter binary (or wrapper).
import sys

assert isinstance(sys.executable, str) and len(sys.executable) > 0
```

## Sections in this repo

- [Argument Passing](argument-passing/index.md)
- [Interactive Mode](interactive-mode/index.md)

Parent: [Using the Python Interpreter](../index.md)
