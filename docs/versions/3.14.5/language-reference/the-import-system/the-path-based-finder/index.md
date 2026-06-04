# [5.5. The Path Based Finder](https://docs.python.org/3/reference/import.html#the-path-based-finder)

[`PathFinder`](https://docs.python.org/3/library/importlib.machinery.html#importlib.machinery.PathFinder) is the default meta-path finder that searches an **import path**—a list of string locations. It does not read files itself; for each path entry it obtains a **path entry finder** (often from [`sys.path_hooks`](https://docs.python.org/3/library/sys.html#sys.path_hooks)) and asks that finder for a spec.

| Variable | Purpose |
|----------|---------|
| `sys.path` | Top-level search locations (from `PYTHONPATH`, install layout, …) |
| `sys.path_hooks` | Callables that produce a finder for a path entry |
| `sys.path_importer_cache` | Maps path entries to finders (or `None` if none apply) |
| `package.__path__` | Search path when importing inside a package |

Path entries may name directories, zip files, or other locatable resources. The empty string entry represents the **current working directory**, which is resolved fresh on each lookup (unlike other cached entries).

```python
# Goal: PathFinder is on the default meta path and sys.path holds strings
import sys
import importlib.machinery

assert importlib.machinery.PathFinder in sys.meta_path
assert isinstance(sys.path, list)
assert all(isinstance(entry, str) for entry in sys.path)
```

```python
# Goal: find_spec locates a .py module on sys.path
import importlib.util

spec = importlib.util.find_spec("json")
assert spec is not None
assert spec.name == "json"
assert spec.origin is not None
assert spec.origin.endswith(".py") or spec.origin.endswith(".pyc")
```

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Putting non-strings on `sys.path` | Entries are silently ignored | Append only `str` paths |
| Stale `sys.path_importer_cache` after layout changes | Finder misses new directories | Clear the cache entry or restart |
| Confusing `PathFinder` with path entry finders | Wrong hook list customized | Replace path hooks only for filesystem/zip semantics |

Parent: [5. The import system](../index.md)
