# [pdb — The Python Debugger](https://docs.python.org/3/library/pdb.html)

`pdb` is the **interactive source-level debugger** for Python. Set breakpoints, step through statements, inspect locals, and evaluate expressions at runtime. Built on [`bdb`](../bdb-debugger-framework/index.md). Canonical reference: [pdb.html](https://docs.python.org/3/library/pdb.html).

---

## Purpose

Use `pdb` when you need to **explore program state** interactively: run `python -m pdb script.py`, insert `breakpoint()` (or `pdb.set_trace()`), or invoke post-mortem debugging after an exception.

---

## Common entry points

| Entry | Usage |
|-------|-------|
| `breakpoint()` | Built-in (3.7+); respects `PYTHONBREAKPOINT` |
| `pdb.set_trace()` | Enter debugger at call site |
| `python -m pdb prog.py` | Start program under debugger |
| `pdb.post_mortem(tb)` | Debug after exception |

---

## Example — programmatic Pdb without stdin

```python
import pdb
import io

class OneCommandPdb(pdb.Pdb):
    def __init__(self):
        super().__init__(stdin=io.StringIO("c\n"), stdout=io.StringIO())

def add(a, b):
    return a + b

globs = {"add": add}
debugger = OneCommandPdb()
debugger.run("add(2, 3)", globals=globs, locals=globs)
assert add(2, 3) == 5
```

---

## Example — inspect frame with pdb helper

```python
import pdb

def sample():
    x = 10
    return x * 2

import inspect
frame = inspect.currentframe().f_back  # caller frame; use sample's frame in real debugging
# pdb.Pdb().interaction(frame, None)  # interactive — not for exec
assert sample() == 20
```

---

## Essential debugger commands (interactive)

| Command | Action |
|---------|--------|
| `l` (list) | Show source around current line |
| `n` (next) | Step over |
| `s` (step) | Step into |
| `c` (continue) | Run until next breakpoint |
| `p expr` | Print expression |
| `w` (where) | Print stack trace |
| `q` (quit) | Abort debugging |

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer `breakpoint()` in library code | Users can disable via `PYTHONBREAKPOINT=0` |
| Use **post-mortem** on test failures | `pytest --pdb` integrates this pattern |
| Avoid leaving breakpoints in committed code | CI will hang waiting for stdin |

---

## See also

- [`bdb`](../bdb-debugger-framework/index.md)
- [`inspect`](https://docs.python.org/3/library/inspect.html)
