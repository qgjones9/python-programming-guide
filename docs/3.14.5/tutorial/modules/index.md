# [Modules](https://docs.python.org/3/tutorial/modules.html)

Condensed notes for [chapter 6 — Modules](https://docs.python.org/3/tutorial/modules.html): splitting code across files, import forms, `__name__`, the import path, bytecode caches, `dir()`, and packages. Each **§** heading links to the matching subsection on docs.python.org. For full narrative (including `fibo.py` walkthroughs), follow those links.

### 6.1 — [More on Modules](https://docs.python.org/3/tutorial/modules.html#more-on-modules)

- A **module** is executed **once** per interpreter process the first time it is imported; later imports reuse the already-initialized module object (use **`importlib.reload()`** while iterating on a module in the REPL).
- **`import m`** binds the name **`m`** to the module; attributes are **`m.attr`**. **`from m import f`** copies **`f`** into the current namespace (the module name **`m`** is not required to exist afterward).
- **`from m import *`** imports public names (not leading **`_`**) and is usually avoided in libraries because it makes name origins unclear.

```python
# import binds the module object; names inside stay qualified by the module.
import math

assert math.pi > 3.14  # access via attribute on the module

# from-import copies a specific callable into this namespace.
from math import sqrt as square_root

assert square_root(9) == 3.0
```

### 6.1.1 — [Executing modules as scripts](https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts)

- Running **`python fibo.py`** executes the file as **`__main__`**, not as an imported module: **`__name__`** is **`"__main__"`** in that case and **`"fibo"`** when **`import fibo`**.
- The usual pattern is to put “library code” at module top level and gate demo / CLI code under **`if __name__ == "__main__":`**.

```python
# __name__ tells you whether code is imported or run as the top-level script.
def work() -> str:
    return "ok"


if __name__ == "__main__":
    # This branch runs only when the file is executed directly, not when imported.
    assert work() == "ok"
```

### 6.1.2 — [The Module Search Path](https://docs.python.org/3/tutorial/modules.html#the-module-search-path)

- **`import spam`** searches **`sys.path`**: the script’s directory, entries from **`PYTHONPATH`**, and installation-dependent defaults.
- **Packages** are found when a directory on **`sys.path`** contains **`__init__.py`** (namespace packages relax this; see the tutorial’s Packages section).

```python
import sys

# sys.path is a list of strings; the first entries win on name collisions.
assert isinstance(sys.path, list)
assert all(isinstance(p, str) for p in sys.path)
```

### 6.1.3 — [“Compiled” Python files](https://docs.python.org/3/tutorial/modules.html#compiled-python-files)

- To speed startup, Python may write **`__pycache__/modulename.interpversion.pyc`** containing bytecode; source **`mtime`** must match or the cache is ignored/rebuilt.
- **`PYTHONDONTWRITEBYTECODE=1`** disables writing **`.pyc`** files (handy in read-only sandboxes).

```python
import py_compile

# py_compile produces a .pyc next to the source (or under __pycache__ depending on flags).
# Here we only assert the helper exists — actual file layout is version-specific.
assert callable(py_compile.compile)
```

### 6.2 — [Standard Modules](https://docs.python.org/3/tutorial/modules.html#standard-modules)

- The standard library includes cross-platform modules (**`sys`**, **`os`**, **`re`**, **`math`**, …); some are platform-specific (documented per module).
- **`sys.ps1` / `sys.ps2`** customize REPL prompts; only defined in interactive interpreters.

```python
import sys

# sys.platform is a coarse OS tag (e.g. "linux", "darwin", "win32").
assert isinstance(sys.platform, str) and len(sys.platform) >= 3
```

### 6.3 — [The `dir()` Function](https://docs.python.org/3/tutorial/modules.html#the-dir-function)

- **`dir()`** lists names in the **current** namespace; **`dir(module)`** lists names bound in **`module`** (mostly attributes, plus module internals).
- **`dir()`** is intended as a convenience for interactive exploration, not a stable public API surface.

```python
import math

names = dir(math)
assert "sqrt" in names and "pi" in names  # public-ish attributes of the math module
```

### 6.4 — [Packages](https://docs.python.org/3/tutorial/modules.html#packages)

- A **package** is a module namespace built from multiple files: **`sound/`** is the **`sound`** package; **`sound.effects.echo`** is **`sound/effects/echo.py`** (plus **`__init__.py`** files in classic layouts).
- **`import sound.effects.echo`** requires **`sound`**, **`sound.effects`**, and **`sound.effects.echo`** to exist on **`sys.path`**; **`sound.effects`** is also importable as a subpackage.

```python
# Package imports are attribute chains on module objects; no filesystem demo here.
import importlib

pkg = importlib.import_module("collections.abc")
assert hasattr(pkg, "Mapping")  # submodule of the standard library "collections" package
```

## Sections in this repo

- [More on Modules](more-on-modules/index.md)
- [Standard Modules](standard-modules/index.md)
- [The dir() Function](the-dir-function/index.md)
- [Packages](packages/index.md)

Next: [Input and Output](../input-and-output/index.md)
