# [test.support.import_helper — Utilities for import tests](https://docs.python.org/3/library/test.html#module-test.support.import_helper)

`test.support.import_helper` manages **import state** during CPython regression tests: fresh module loads, sys.path tweaks, and cleanup of `sys.modules` entries. Canonical reference: [test.html#module-test.support.import_helper](https://docs.python.org/3/library/test.html#module-test.support.import_helper).

---

## Purpose

Import tests must not **pollute** `sys.modules` or leave altered `sys.path` entries. Context managers here isolate imports so test order remains independent.

---

## Key helpers

| Name | Role |
|------|------|
| `import_fresh_module(name, ...)` | Load module as if first import |
| `CleanImport(*module_names)` | Remove modules from `sys.modules` for block duration |
| `DirsOnSysPath` | Temporarily prepend directories to `sys.path` |
| `forget(module_name)` | Delete module and submodules from cache |

---

## Example — CleanImport ensures fresh load

```python
import sys
import types
import test.support.import_helper as ih

mod = types.ModuleType("demo_import_helper_mod")
mod.value = 1
sys.modules["demo_import_helper_mod"] = mod

with ih.CleanImport("demo_import_helper_mod"):
    assert "demo_import_helper_mod" not in sys.modules

assert "demo_import_helper_mod" in sys.modules
assert sys.modules["demo_import_helper_mod"].value == 1
del sys.modules["demo_import_helper_mod"]
```

---

## Example — DirsOnSysPath prepends search path

```python
import sys
import tempfile
import test.support.import_helper as ih

with tempfile.TemporaryDirectory() as tmp:
    with ih.DirsOnSysPath(tmp):
        assert tmp in sys.path
    assert tmp not in sys.path
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Always restore `sys.modules` after fake imports | Prevents cross-test leakage |
| Prefer `importlib` in application code | These helpers target regrtest edge cases |
| Use unique module names in tests | Avoid clobbering real stdlib modules |

---

## See also

- [`importlib`](https://docs.python.org/3/library/importlib.html)
- [`test.support`](testsupport-utilities-for-the-python-test-suite/index.md)
