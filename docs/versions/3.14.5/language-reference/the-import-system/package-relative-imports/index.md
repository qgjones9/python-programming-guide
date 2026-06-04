# [5.7. Package Relative Imports](https://docs.python.org/3/reference/import.html#package-relative-imports)

Relative imports use **leading dots** in `from … import` forms. One dot starts from the **current package**; each additional dot walks up one parent package level. They are only valid inside package modules (where `__package__` is set).

| Syntax | Resolves from | Example inside `subpackage1/moduleX.py` |
|--------|---------------|----------------------------------------|
| `from . import name` | Current package | `from . import moduleY` |
| `from .name import attr` | Submodule of current package | `from .moduleY import spam` |
| `from ..name import attr` | Parent package | `from ..moduleA import foo` |
| `from ..pkg import name` | Sibling under parent | `from ..subpackage2.moduleZ import eggs` |

Absolute imports allow both `import pkg.mod` and `from pkg import mod`. Relative imports allow **only** the `from` form because `import .moduleY` would require `.moduleY` to be a valid expression—which it is not.

```python
# Goal: AST records the dot level for relative from-imports
import ast

node = ast.parse("from ..sibling import thing")
imp = node.body[0]
assert isinstance(imp, ast.ImportFrom)
assert imp.level == 2
assert imp.module == "sibling"
assert [alias.name for alias in imp.names] == ["thing"]
```

```python
# Goal: __package__ anchors relative resolution (here, the stdlib package)
import importlib
import encodings

assert encodings.__package__ == "encodings"
sub = importlib.import_module("encodings.utf_8")
assert sub.__package__ == "encodings"
assert sub.__name__ == "encodings.utf_8"
```

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Running a package module as `python pkg/mod.py` | `__package__` unset → relative imports fail | Use `python -m pkg.mod` |
| Using `import .sub` syntax | SyntaxError—relative `import` form disallowed | Always use `from . import sub` |
| Miscounting dots | Import from wrong ancestor package | Draw the package tree; count parents |

Parent: [5. The import system](../index.md)
