# [modulefinder — Find modules used by a script](https://docs.python.org/3/library/modulefinder.html)

[`modulefinder`](https://docs.python.org/3/library/modulefinder.html) provides **`ModuleFinder`**, a class that analyzes a Python script and records which modules it imports (and which imports failed). It is useful for bundling tools, dependency audits, and teaching how import graphs grow. The module can also be run as **`python -m modulefinder script.py`**. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/modulefinder.html).

---

## Module-level helpers

| Function | Purpose |
|----------|---------|
| `AddPackagePath(pkg_name, path)` | Tell the finder that `pkg_name` also lives at `path` |
| `ReplacePackage(oldname, newname)` | Map `oldname` imports to package `newname` |

---

## `ModuleFinder` — [class modulefinder.ModuleFinder](https://docs.python.org/3/library/modulefinder.html#modulefinder.ModuleFinder)

| Member | Role |
|--------|------|
| `run_script(pathname)` | Parse and trace imports starting from a file |
| `report()` | Print loaded modules and missing modules to stdout |
| `modules` | `dict` mapping module name → module-like object with `globalnames` |
| `badmodules` | Modules that could not be imported |

Constructor arguments: `path` (default `sys.path`), `debug`, `excludes`, `replace_paths`.

---

## Example — [Example usage of ModuleFinder](https://docs.python.org/3/library/modulefinder.html#example-usage-of-modulefinder)

```python
# Goal: finder records stdlib imports and failed optional ones
import os
import tempfile
from modulefinder import ModuleFinder

script = """
import re
try:
    import no_such_module_xyz_12345
except ImportError:
    pass
"""
with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
    f.write(script)
    path = f.name
try:
    finder = ModuleFinder()
    finder.run_script(path)
    assert "re" in finder.modules
    assert "no_such_module_xyz_12345" in finder.badmodules
finally:
    os.unlink(path)
```

```python
# Goal: AddPackagePath influences search locations (smoke test)
from modulefinder import AddPackagePath

AddPackagePath("fake_pkg", "/tmp")
# no exception — path registered for subsequent ModuleFinder runs
```

---

## Limitations

| Limitation | Detail |
|------------|--------|
| Static analysis | Only sees imports reachable by scanning bytecode at analysis time |
| Dynamic imports | `importlib.import_module(variable)` may be missed |
| C extensions | Listed when imported, not when merely loaded by the interpreter |
| `excludes` | Use to skip huge stdlib branches during reports |

For production dependency graphs of installed distributions, consider `pip freeze`, `pipdeptree`, or packaging tools instead of `modulefinder` alone.
