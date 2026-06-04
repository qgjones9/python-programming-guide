# [5.2. Packages](https://docs.python.org/3/reference/import.html#packages)

Packages organize modules into a naming hierarchy (`email.mime.text`). **All packages are modules**, but only modules with a [`__path__`](https://docs.python.org/3/reference/import.html#index-10) attribute are packages. Python distinguishes **regular packages** (typically a directory with `__init__.py`) from **namespace packages** (portions spread across locations, no single `__init__.py` required—see PEP 420).

| Package kind | Typical layout | `__path__` | `__init__.py` |
|--------------|----------------|------------|---------------|
| Regular | `pkg/__init__.py`, submodules as files | Set by loader (directory paths) | Executed on first import of the package |
| Namespace | Multiple `pkg/` directories on the search path | Custom iterable; re-searches when parent path changes | Not required at the root |
| Namespace subpackage | Subdir without `__init__.py` inside a regular package | Contributes a portion to the parent namespace | Absent in the subdir |

Importing `parent.one` executes `parent/__init__.py` then `parent/one/__init__.py` (when present). Subsequent imports of sibling subpackages reuse the already-initialized parent package object.

```python
# Goal: a module with __path__ is a package; math is a plain module
import math
import importlib
import importlib.util
import pathlib

assert not hasattr(math, "__path__")
spec = importlib.util.find_spec("importlib")
assert spec is not None
pkg = importlib.import_module("importlib")
assert hasattr(pkg, "__path__")
assert all(isinstance(p, str) for p in pkg.__path__)
assert any(pathlib.Path(p).is_dir() for p in pkg.__path__)
```

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Treating directories without `__init__.py` as importable before 3.3 | Implicit namespace behavior differs by version | Target 3.3+ semantics; document namespace layout |
| Forgetting that importing a submodule runs parent `__init__.py` | Side effects run earlier than expected | Keep package `__init__.py` lightweight |
| Assuming one filesystem tree equals one namespace package | Portions may live in separate roots | Design install layout for PEP 420 discovery |

Parent: [5. The import system](../index.md)
