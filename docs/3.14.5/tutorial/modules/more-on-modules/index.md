# [More on Modules](https://docs.python.org/3/tutorial/modules.html#more-on-modules)

Condensed notes for **§6.1 — More on Modules** in the [Python Tutorial](https://docs.python.org/3/tutorial/modules.html): import variants, module initialization, `as` aliases, and reloading. For the full `fibo` examples, follow the official page.

### Import forms and namespaces

- **`import m`** keeps a single module object; **`from m import x`** binds **`x`** in the importer’s global namespace.
- **`import m as alias`** is the same lookup as **`import m`**, but the local binding is **`alias`**.
- **`from m import *`** skips names starting with **`_`** by default; it is discouraged in application code because it obscures where names came from.

```python
# Simulate "module has its own globals" without writing a second file on disk.
import types

m = types.ModuleType("demo")
m.counter = 0


def inc() -> None:
    # Functions close over the module object via global lookup on attribute assignment.
    m.counter += 1


inc()
inc()
assert m.counter == 2
```

### Reload during development

- After editing a module on disk, **`importlib.reload(mod)`** re-executes the module body (watch for duplicate side effects if imports re-run registration code).

```python
import importlib
import sys

# sys is always loaded; reload re-runs initialization — safe to call, but side-effectful in general.
reloaded = importlib.reload(sys)
assert reloaded is sys  # reload returns the same module object
```

## Sections in this repo

- [Executing modules as scripts](executing-modules-as-scripts/index.md)
- [The module search path](the-module-search-path/index.md)
- [Compiled Python files](compiled-python-files/index.md)

Parent: [Modules](../index.md)
