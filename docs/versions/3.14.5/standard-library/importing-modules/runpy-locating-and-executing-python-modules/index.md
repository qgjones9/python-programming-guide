# [runpy — Locating and executing Python modules](https://docs.python.org/3/library/runpy.html)

[`runpy`](https://docs.python.org/3/library/runpy.html) **locates and executes** Python code without requiring you to import it first in the usual way. It powers **`python -m package.module`** and running scripts by filesystem path. Code runs in the **current process**—side effects (including `sys.modules` entries) persist. For sandboxed or thread-safe loading, prefer [`importlib`](../importlib-the-implementation-of-import/index.md). Full API reference remains on [docs.python.org](https://docs.python.org/3/library/runpy.html).

---

## Functions

| Function | Use case |
|----------|----------|
| `run_module(mod_name, init_globals=None, run_name=None, alter_sys=False)` | Execute a module by absolute name; packages run `pkg.__main__` |
| `run_path(path_name, init_globals=None, run_name=None)` | Execute a `.py` file or a `sys.path` entry’s `__main__` |

Both set `__name__`, `__spec__`, `__file__`, and related module globals before execution, then restore altered `sys` attributes when finished.

---

## `run_module` — [runpy.run_module](https://docs.python.org/3/library/runpy.html#runpy.run_module)

| `alter_sys=True` | Effect |
|------------------|--------|
| Updates `sys.argv[0]` to `__file__` | Mimics script execution |
| Sets `sys.modules[__name__]` | Temporary module object during run |

**Not thread-safe** when `alter_sys` is used.

```python
# Goal: run a package __main__ submodule via run_module
import os
import runpy
import sys
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    pkg = os.path.join(tmp, "demo_pkg")
    os.makedirs(pkg)
    with open(os.path.join(pkg, "__init__.py"), "w") as f:
        f.write("")
    with open(os.path.join(pkg, "__main__.py"), "w") as f:
        f.write("MAIN_FLAG = 99\n")
    sys.path.insert(0, tmp)
    try:
        ns = runpy.run_module("demo_pkg", run_name="__main__")
        assert ns["MAIN_FLAG"] == 99
        assert ns["__name__"] == "__main__"
    finally:
        sys.path.remove(tmp)
        sys.modules.pop("demo_pkg", None)
```

---

## `run_path` — [runpy.run_path](https://docs.python.org/3/library/runpy.html#runpy.run_path)

Always adjusts `sys.path` when the target is a directory or zip with `__main__.py`—unlike `run_module`, `alter_sys` is not optional for path entries.

```python
# Goal: execute a standalone script file
import os
import runpy
import tempfile

with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
    f.write("ANSWER = 6 * 7\n")
    path = f.name
try:
    ns = runpy.run_path(path, run_name="__main__")
    assert ns["ANSWER"] == 42
    assert ns["__name__"] == "__main__"
finally:
    os.unlink(path)
```

```python
# Goal: init_globals seeds the namespace before execution
import os
import runpy
import tempfile

with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
    f.write("result = start + 1\n")
    path = f.name
try:
    ns = runpy.run_path(path, init_globals={"start": 10})
    assert ns["result"] == 11
finally:
    os.unlink(path)
```

---

## Comparison with `import`

| Approach | Returns | `sys.modules` after |
|----------|---------|---------------------|
| `importlib.import_module('pkg.mod')` | Module object | Permanent entry under real name |
| `runpy.run_module('pkg.mod')` | Globals `dict` | May use temporary `__main__` name |

Functions and classes defined during `runpy` execution may not behave correctly if you keep using them after the call returns—reload or re-import if you need long-lived objects.

---

## Related PEPs

| PEP | Topic |
|-----|-------|
| [PEP 338](https://peps.python.org/pep-0338/) | Executing modules as scripts |
| [PEP 366](https://peps.python.org/pep-0366/) | Relative imports in `__main__` |
| [PEP 451](https://peps.python.org/pep-0451/) | `ModuleSpec` and accurate `__cached__` |
