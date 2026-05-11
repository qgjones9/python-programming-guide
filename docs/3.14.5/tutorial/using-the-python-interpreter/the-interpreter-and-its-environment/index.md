# [The Interpreter and Its Environment](https://docs.python.org/3/tutorial/interpreter.html#the-interpreter-and-its-environment)

Condensed notes for **§2.2** of [Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html): how Python picks **source encodings** and why UTF-8 is the default.

```python
import encodings

# Any codec name accepted in `# -*- coding: ... -*-` must exist in the codec registry.
assert encodings.search_function("utf-8") is not None
```

## Sections in this repo

- [Source Code Encoding](source-code-encoding/index.md)

Parent: [Using the Python Interpreter](../index.md)
