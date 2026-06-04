# [pkgutil — Package extension utility](https://docs.python.org/3/library/pkgutil.html)

[`pkgutil`](https://docs.python.org/3/library/pkgutil.html) provides helpers on top of the import system: **namespace-style path extension**, iterating modules on a path, walking package trees, resolving dotted names to objects, and reading **package resources** via loader `get_data`. Since 3.3 it delegates to [`importlib`](../importlib-the-implementation-of-import/index.md) rather than legacy PEP 302 emulation. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/pkgutil.html).

---

## Key APIs

| Function | Purpose |
|----------|---------|
| `extend_path(path, name)` | Merge directories (and `*.pkg` files) into a package’s `__path__` |
| `iter_modules(path=None, prefix='')` | Yield `ModuleInfo(name, ispkg)` for one directory level |
| `walk_packages(path=None, prefix='', onerror=None)` | Recursively yield modules (imports packages to read `__path__`) |
| `get_importer(path_item)` | Cached finder from `sys.path_importer_cache` |
| `iter_importers(fullname='')` | Yield finders for a package or top level |
| `get_data(package, resource)` | Binary read of a resource relative to a package |
| `resolve_name(name)` | Resolve `'pkg.mod:obj.attr'` or legacy dotted form to an object |
| `ModuleInfo` | `namedtuple(module_finder, name, ispkg)` since 3.6 |

---

## Extending package search paths — [pkgutil.extend_path](https://docs.python.org/3/library/pkgutil.html#pkgutil.extend_path)

Place in a package’s `__init__.py` to merge multiple on-disk trees into one logical package:

```python
# Goal: extend_path returns a new list with extra entries
import pkgutil

base = ["pkg"]
extended = pkgutil.extend_path(base, "nonexistent_pkg_name_xyz")
assert isinstance(extended, list)
assert extended[0] == "pkg"
```

---

## Discovering modules

```python
# Goal: iter_modules finds json among top-level names
import pkgutil

names = {m.name for m in pkgutil.iter_modules() if m.name == "json"}
assert "json" in names
```

```python
# Goal: walk_packages under ctypes finds submodules
import ctypes
import pkgutil

found = any(m.name.startswith("ctypes.") for m in pkgutil.walk_packages(ctypes.__path__, ctypes.__name__ + "."))
assert found
```

---

## Package data — [pkgutil.get_data](https://docs.python.org/3/library/pkgutil.html#pkgutil.get_data)

Prefer [`importlib.resources`](../importlibresources-package-resource-reading-opening-and-access/index.md) for new code; `get_data` remains a thin wrapper over loader `get_data()`.

```python
# Goal: read a resource from the standard library importlib package
import pkgutil

data = pkgutil.get_data("importlib", "_bootstrap.py")
assert data is not None
assert b"ModuleSpec" in data or b"module" in data.lower()
```

---

## Name resolution — [pkgutil.resolve_name](https://docs.python.org/3/library/pkgutil.html#pkgutil.resolve_name)

```python
# Goal: colon form imports package then traverses attribute
import pkgutil

loader = pkgutil.resolve_name("importlib:abc.Loader")
assert loader.__name__ == "Loader"
```

---

## Security and performance

| Note | Detail |
|------|--------|
| `get_data` | Intended for **trusted** paths; does not verify the resource “belongs” to the package |
| `walk_packages` | Imports every package on the path—can be slow and have side effects |
| Namespace packages | Namespace loaders may not support `get_data` (returns `None`) |
