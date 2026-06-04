# [bdb — Debugger framework](https://docs.python.org/3/library/bdb.html)

`bdb` implements the **debugger framework** underlying [`pdb`](pdb-the-python-debugger/index.md): breakpoints, stepping, stack frames, and dispatch to user-defined debuggers via `Bdb` subclasses. Canonical reference: [bdb.html](https://docs.python.org/3/library/bdb.html).

---

## Purpose

Application authors rarely import `bdb` directly unless building a **custom debugger** or programmatic breakpoint driver. Subclass `bdb.Bdb`, override `user_line`, `user_call`, and `user_return`, then call `set_trace()` or `run()` to enter the debug loop.

---

## Key classes

| Class | Role |
|-------|------|
| `Bdb` | Base debugger with `set_break`, `clear_break`, `set_step`, `set_continue` |
| `Breakpoint` | File/line breakpoint with hit count and condition |
| `BdbQuit` | Exception raised to exit debugger |
| `Tdb` | Trace prints line events (simple demo subclass) |

---

## Example — minimal line tracer via Bdb

```python
import bdb

class LineCollector(bdb.Bdb):
    def __init__(self):
        super().__init__()
        self.lines = []

    def user_line(self, frame):
        self.lines.append(frame.f_lineno)

def target():
    a = 1
    b = 2
    return a + b

globs = {"target": target}
collector = LineCollector()
collector.run("target()", globals=globs, locals=globs)
assert target() == 3
assert len(collector.lines) >= 1
```

---

## Example — breakpoint API

```python
import bdb

db = bdb.Bdb()
# set_break(filename, lineno) returns status; filename must match co_filename
func_code = (lambda: None).__code__
result = db.set_break(func_code.co_filename, func_code.co_firstlineno)
assert result is None or isinstance(result, str)
db.clear_all_breaks()
```

---

## Relationship to pdb

| Layer | Module |
|-------|--------|
| User-facing CLI | [`pdb`](pdb-the-python-debugger/index.md) |
| Framework | `bdb` |
| Execution tracing | [`sys.settrace`](https://docs.python.org/3/library/sys.html#sys.settrace) |

---

## See also

- [`pdb`](pdb-the-python-debugger/index.md)
- [`inspect`](https://docs.python.org/3/library/inspect.html) — stack frame introspection
