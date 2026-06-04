# [pyclbr — Python module browser support](https://docs.python.org/3/library/pyclbr.html)

The [`pyclbr`](https://docs.python.org/3/library/pyclbr.html) module reads **class and top-level function definitions** from Python modules **without executing** them. It uses the tokenizer and parser internally, making it safer than `importlib` when browsing untrusted code. IDEs and documentation generators use similar techniques. Full API remains on [docs.python.org](https://docs.python.org/3/library/pyclbr.html).

Related: [`ast`](../ast-abstract-syntax-trees/index.md) for full AST access; [`inspect`](../../python-runtime-services/inspect-inspect-live-objects/index.md) for live objects after import.

---

## Core functions — [Function Objects](https://docs.python.org/3/library/pyclbr.html#function-objects)

| Function | Role |
|----------|------|
| `pyclbr.readmodule(module, path=None)` | Dict `{name: Class/Function}` for one module |
| `pyclbr.readmodule_ex(module, path=None)` | Same; returns `{}` on unreadable source, may raise for missing modules |
| `pyclbr.readmodule_ex` / `readmodule` | Accept dotted module names |
| `Class.name`, `.super`, `.methods`, `.file`, `.lineno` | Metadata for classes |
| `Function.name`, `.file`, `.lineno` | Metadata for functions |

```python
# Goal: list class definitions in a pure-Python stdlib module
import pyclbr

info = pyclbr.readmodule("ast")
assert "NodeVisitor" in info
assert "NodeTransformer" in info
cls = info["NodeVisitor"]
assert isinstance(cls, pyclbr.Class)
assert cls.lineno > 0
```

```python
# Goal: inspect class metadata without importing
import pyclbr

info = pyclbr.readmodule("ast")
assert "NodeVisitor" in info
visitor = info["NodeVisitor"]
assert isinstance(visitor, pyclbr.Class)
assert "generic_visit" in visitor.methods
```

---

## `Class` vs `Function` objects

| Attribute | `Class` | `Function` |
|-----------|---------|------------|
| `name` | Class name | Function name |
| `file` | Defining source path | Defining source path |
| `lineno` | Line of `class` statement | Line of `def` |
| `super` | List of base class names (strings) | — |
| `methods` | Dict of method name → `Function` | — |

Only **syntactic** definitions appear—dynamically assigned attributes (`MyClass.foo = ...`) are invisible to `pyclbr`.

```python
# Goal: readmodule_ex returns a dict for readable modules
import pyclbr

result = pyclbr.readmodule_ex("ast")
assert isinstance(result, dict)
assert "NodeVisitor" in result
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`readmodule_ex`** in UI tools | Avoid crashing on broken install paths |
| Pass **`path`** when the module is not on `sys.path` | Supports standalone file browsing |
| Use **`ast`** when you need assignments or decorators in detail | `pyclbr` is intentionally narrow |

---

## See also

- [`ast`](../ast-abstract-syntax-trees/index.md) — full parse tree
- [`importlib`](../../importing-modules/importlib-the-implementation-of-import/index.md) — actual module loading (executes code)
