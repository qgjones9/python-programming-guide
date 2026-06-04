# [5.1. importlib](https://docs.python.org/3/reference/import.html#importlib)

The [`importlib`](https://docs.python.org/3/library/importlib.html) module exposes the import machinery as a rich API. The reference chapter points here for day-to-day programmatic imports: prefer [`importlib.import_module()`](https://docs.python.org/3/library/importlib.html#importlib.import_module) over calling built-in [`__import__()`](https://docs.python.org/3/library/functions.html#import__) directly, because `__import__()` performs only the search/create steps—not the name binding that an `import` statement performs afterward.

| API | Role |
|-----|------|
| `importlib.import_module(name)` | Recommended high-level import (returns the module object) |
| `importlib.util.find_spec(name)` | Inspect how a module would be found without loading it |
| `importlib.reload(module)` | Re-execute an existing module in place |
| `importlib.abc.*` | Abstract base classes for custom finders and loaders |

```python
# Goal: import_module returns the same cached object as a normal import
import importlib
import sys

mod = importlib.import_module("json")
import json

assert mod is json
assert sys.modules["json"] is mod
assert mod.dumps([1, 2]) == "[1, 2]"
```

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Calling `__import__("pkg.mod")` expecting `mod` | Returns the **top-level** package, not the leaf | Use `import_module("pkg.mod")` or assign from `import` |
| Reloading while other modules hold references | Stale class instances from the old module | Restart the process or redesign module-level singletons |
| Mixing `import_module` with partial parent imports | Parent packages must load before submodules | Import parents explicitly when constructing custom loaders |

Parent: [5. The import system](../index.md)
