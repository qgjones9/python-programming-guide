# [5.6. Replacing the standard import system](https://docs.python.org/3/reference/import.html#replacing-the-standard-import-system)

The import machinery is intentionally extensible. Two levels of replacement exist: wholesale (replace [`sys.meta_path`](https://docs.python.org/3/library/sys.html#sys.meta_path)) and surgical (override built-in [`__import__()`](https://docs.python.org/3/library/functions.html#import__) while leaving other APIs alone).

| Approach | Scope | Typical use |
|----------|-------|-------------|
| Clear/replace `sys.meta_path` | Entire import system | Virtual filesystems, embedded runtimes |
| Custom meta hook early in the list | Selective blocking or redirection | Deny-list modules, lazy loading |
| Replace `builtins.__import__` | `import` statement only | Sandboxing without breaking `importlib` APIs |

To **block** a module from a meta hook, raise [`ModuleNotFoundError`](https://docs.python.org/3/library/exceptions.html#ModuleNotFoundError) from `find_spec()`. Returning `None` means “keep searching other finders.”

```python
# Goal: default CPython meta path includes builtin, frozen, and path finders
import sys

finder_names = []
for finder in sys.meta_path:
    if isinstance(finder, type):
        finder_names.append(finder.__name__)
    else:
        finder_names.append(type(finder).__name__)

assert "BuiltinImporter" in finder_names
assert "FrozenImporter" in finder_names
assert "PathFinder" in finder_names
```

```python
# Goal: prepending a hook can intercept imports before defaults run
import sys
import importlib.abc

class BlockJsonFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == "json":
            raise ModuleNotFoundError("blocked for demo")
        return None

sys.modules.pop("json", None)
sys.meta_path.insert(0, BlockJsonFinder())
try:
    import json  # noqa: F401 — expect failure
    raised = False
except ModuleNotFoundError as exc:
    raised = True
    assert "blocked for demo" in str(exc)
finally:
    sys.meta_path.pop(0)

assert raised
```

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Removing all default finders | Built-ins and stdlib become unimportable | Append custom finders instead of replacing blindly |
| Returning `None` to block imports | Search continues; module may still load | Raise `ModuleNotFoundError` explicitly |
| Patching `__import__` only | `importlib.import_module` bypasses it | Hook `sys.meta_path` for consistent behavior |

Parent: [5. The import system](../index.md)
