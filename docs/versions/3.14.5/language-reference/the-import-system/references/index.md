# [5.9. References](https://docs.python.org/3/reference/import.html#references)

The import system evolved from early package notes through PEP 302 (meta path hooks), PEP 420 (namespace packages), PEP 451 (module specs), and related follow-ons. These PEPs are the authoritative history when behavior differs across Python versions.

| PEP | Topic |
|-----|-------|
| [PEP 302](https://peps.python.org/pep-0302/) | Original `sys.meta_path` import hooks |
| [PEP 420](https://peps.python.org/pep-0420/) | Implicit namespace packages (3.3+) |
| [PEP 328](https://peps.python.org/pep-0328/) | Absolute imports and relative import syntax |
| [PEP 366](https://peps.python.org/pep-0366/) | `__package__` for main-module relative imports |
| [PEP 338](https://peps.python.org/pep-0338/) | Executing modules as scripts (`python -m`) |
| [PEP 451](https://peps.python.org/pep-0451/) | `ModuleSpec`; loader/import machinery split |

```python
# Goal: PEP 451 ModuleSpec is the modern encapsulation of per-module import state
import importlib.machinery
import json

assert hasattr(importlib.machinery, "ModuleSpec")
spec = json.__spec__
assert isinstance(spec, importlib.machinery.ModuleSpec)
assert spec.name == "json"
```

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Following pre-3.3 package tutorials | Missing spec-based APIs; wrong hook signatures | Read PEP 451 + current reference chapter |
| Using deprecated `find_module()` hooks | Removed in 3.12 | Implement `find_spec()` on finders and loaders |
| Ignoring PEP 420 when merging vendor trees | Duplicate `__init__.py` fights namespace layout | Use namespace portions instead of shadow copies |

Parent: [5. The import system](../index.md)
