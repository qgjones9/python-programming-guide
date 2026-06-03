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

## Best practices

- Prefer `importlib.import_module()` over direct `__import__()`—it returns the module you expect without `fromlist` subtleties.
- Do not replace `builtins.__import__` unless you fully understand import hooks and debugging cost.
- For `pkgutil`, plugins, or custom loaders, use `importlib` machinery (PEP 302 hooks) instead of patching `__import__`.
