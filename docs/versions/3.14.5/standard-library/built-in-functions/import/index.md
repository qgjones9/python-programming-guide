# [__import__()](https://docs.python.org/3/library/functions.html#import__)

## Description

`__import__(name, globals=None, locals=None, fromlist=(), level=0)` is invoked by the `import` statement. It loads a module by name and returns the top-level package unless `fromlist` requests submodule attributes.

## What problem it solves

Programmatic importing when the module name is computed at runtime. This is advanced machinery—the standard library exposes safer helpers for most use cases.

## Implementation options

### Import a top-level module by name

```python
os = __import__("os")
assert hasattr(os, "path")
assert os.path.basename("/tmp/demo.txt") == "demo.txt"
```

### Load a submodule with `fromlist`

```python
json_module = __import__("json", fromlist=[""])
assert json_module.dumps([1, 2]) == "[1, 2]"
```

### Prefer `importlib.import_module` in application code

```python
import importlib

mod = importlib.import_module("collections.abc")
assert hasattr(mod, "Mapping")
```

### Load a module from a file path (plugin pattern)

```python
import importlib.util
import os
import tempfile

with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
    f.write("PLUGIN_VALUE = 42\n")
    path = f.name

try:
    spec = importlib.util.spec_from_file_location("plugin", path)
    plugin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin)
    assert plugin.PLUGIN_VALUE == 42
finally:
    os.unlink(path)
```

## Best practices

- **Prefer `importlib.import_module()` over direct `__import__()`**—it returns the module you expect without `fromlist` subtleties.

```python
import importlib

mod = importlib.import_module("json")
assert mod.dumps({"a": 1}) == '{"a": 1}'
```

- **Do not replace `builtins.__import__` unless you fully understand import hooks and debugging cost.** The snippet below restores the original hook immediately.

```python
import builtins

old_import = builtins.__import__

def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
    return old_import(name, globals, locals, fromlist, level)

builtins.__import__ = custom_import
import math as demo_math
builtins.__import__ = old_import
assert hasattr(demo_math, "pi")
```

- **For plugins or custom loaders, use `importlib` machinery instead of patching `__import__`.** See the file-path example above with `importlib.util.spec_from_file_location`.
