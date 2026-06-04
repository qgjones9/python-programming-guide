# [5.3. Searching](https://docs.python.org/3/reference/import.html#searching)

Before loading, Python needs the **fully qualified name** (`foo.bar.baz`). Import walks prefixes left to right: `foo`, then `foo.bar`, then `foo.bar.baz`. Any intermediate failure raises [`ModuleNotFoundError`](https://docs.python.org/3/library/exceptions.html#ModuleNotFoundError).

| Step | Mechanism | Notes |
|------|-----------|-------|
| 1 | `sys.modules` cache | Hit → import completes immediately |
| 2 | Meta-path traversal | Each finder’s `find_spec(name, path, target)` |
| 3 | Spec hand-off | Finder returns `ModuleSpec`; loader loads later |

**Finders** decide *whether* a module exists; **loaders** execute module code. Objects implementing both are **importers**. Meta hooks (`sys.meta_path`) run before path processing; path hooks (`sys.path_hooks`) run for each entry on `sys.path` or `package.__path__`.

```python
# Goal: sys.modules caches every prefix of a dotted import
import sys

for name in ("encodings", "encodings.utf_8"):
    sys.modules.pop(name, None)

import encodings.utf_8

assert "encodings" in sys.modules
assert "encodings.utf_8" in sys.modules
assert sys.modules["encodings.utf_8"].__name__ == "encodings.utf_8"
```

```python
# Goal: deleting a cache entry forces a fresh search on next import
import sys
import importlib
import json

original = json
del sys.modules["json"]
reloaded = importlib.import_module("json")
assert reloaded is not original  # new module object
assert reloaded.dumps([]) == "[]"
```

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Setting `sys.modules[name] = None` | Next import raises `ModuleNotFoundError` | Use only to block imports deliberately |
| Deleting cache entries while holding references | Old and new imports see different module objects | Prefer `importlib.reload()` for in-place refresh |
| Confusing meta-path finders with path entry finders | Hooks registered on the wrong list | Meta → `sys.meta_path`; path → `sys.path_hooks` |

Parent: [5. The import system](../index.md)
