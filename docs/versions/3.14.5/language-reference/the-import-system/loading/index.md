# [5.4. Loading](https://docs.python.org/3/reference/import.html#loading)

Once a [`ModuleSpec`](https://docs.python.org/3/library/importlib.html#importlib.machinery.ModuleSpec) is found, the loader materializes the module object and runs its code. Critical invariant: the module is inserted into [`sys.modules`](https://docs.python.org/3/library/sys.html#sys.modules) **before** `exec_module()` so circular imports terminate instead of recursing forever.

| Stage | Responsibility |
|-------|----------------|
| `create_module(spec)` | Optional; loader may construct the module object |
| `_init_module_attrs` | Sets `__name__`, `__loader__`, `__package__`, `__spec__`, … |
| `exec_module(module)` | Populates `module.__dict__` by running the module body |
| Submodule binding | Importing `pkg.sub` sets `pkg.sub` attribute on the parent |

If loading fails, only the failing module is removed from `sys.modules`; successfully loaded parents and side-effect imports remain cached. [`importlib.reload()`](https://docs.python.org/3/library/importlib.html#importlib.reload) reuses the same module object—unlike delete-and-reimport.

```python
# Goal: loaded stdlib modules expose import metadata on __spec__
import json

assert json.__spec__ is not None
assert json.__spec__.name == "json"
assert json.__spec__.loader is not None
assert json.__name__ == "json"
```

```python
# Goal: parent gains a submodule attribute when a subpackage loads
import importlib
import sys

for name in ("importlib", "importlib.metadata"):
    sys.modules.pop(name, None)

parent = importlib.import_module("importlib")
child = importlib.import_module("importlib.metadata")

assert getattr(parent, "metadata") is child
assert sys.modules["importlib.metadata"] is child
```

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Importing before `sys.modules` registration in custom loaders | Infinite recursion on circular imports | Register the module before executing its code |
| Assuming `exec_module` return value matters | Return value is ignored | Mutate `module.__dict__` in the loader |
| Expecting reload to refresh every importer | Other modules may keep old attribute bindings | Re-bind names or restart the interpreter |

Parent: [5. The import system](../index.md)
