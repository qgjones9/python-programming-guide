# [Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html)

Condensed notes for [chapter 2 — Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html): launching **`python`**, **`-c`**, **`-m`**, **`-i`**, **`sys.argv`**, interactive prompts, and **UTF-8** source encoding. For platform-specific install paths and shell quoting, follow the official page.

### 2.1 — [Invoking the Interpreter](https://docs.python.org/3/tutorial/interpreter.html#invoking-the-interpreter)

- **`python script.py args...`** runs a file; **`python -c 'code'`** runs a one-liner; **`python -m pkg.mod`** runs a module as **`__main__`**.
- **`-i`** after a script drops you into the REPL with the program’s globals still loaded—handy for post-mortem exploration.

```python
import sys

# When Python runs `python script.py a b`, argv[0] is the script path and the rest are args.
argv = ["demo.py", "a", "b"]
assert argv[1:] == ["a", "b"]

# `-c` and `-m` conventions are documented in `sys.argv[0]` — mirror them with a toy list.
assert ["-c", "tail"][0] == "-c"
```

#### 2.1.1 — [Argument Passing](https://docs.python.org/3/tutorial/interpreter.html#argument-passing)

- **`sys.argv[0]`** is **`'-c'`** for **`-c`**, the module name for **`-m`**, **`'-'`** for stdin-as-script, or the script path otherwise.

```python
import sys

# Simulate the tutorial’s contract without actually re-invoking the interpreter.
argv = ["-c", "extra"]
assert argv[0] == "-c" and argv[1] == "extra"
```

#### 2.1.2 — [Interactive Mode](https://docs.python.org/3/tutorial/interpreter.html#interactive-mode)

- **`>>>` / `...`** prompts distinguish primary vs continuation lines; blank lines often end blocks in the REPL (not in files).

```python
# In a .py file, indentation alone terminates blocks — no "blank line ends block" rule.
if True:
    x = 1
assert x == 1
```

### 2.2 — [The Interpreter and Its Environment](https://docs.python.org/3/tutorial/interpreter.html#the-interpreter-and-its-environment)

#### 2.2.1 — [Source Code Encoding](https://docs.python.org/3/tutorial/interpreter.html#source-code-encoding)

- Default is **UTF-8**; legacy files may start with **`# -*- coding: cp1252 -*-`** (first or second line if a shebang occupies line 1).

```python
# -*- coding: utf-8 -*-
# This file is UTF-8 by default in modern Python; the cookie form still parses if you need it.

assert "π".encode("utf-8") == b"\xcf\x80"  # non-ASCII literal is fine when the source encoding supports it
```

## Sections in this repo

- [Invoking the Interpreter](invoking-the-interpreter/index.md)
- [The Interpreter and Its Environment](the-interpreter-and-its-environment/index.md)

Next: [An Informal Introduction to Python](../an-informal-introduction-to-python/index.md)
