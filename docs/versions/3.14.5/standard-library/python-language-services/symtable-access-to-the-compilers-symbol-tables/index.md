# [symtable — Access to the compiler's symbol tables](https://docs.python.org/3/library/symtable.html)

The [`symtable`](https://docs.python.org/3/library/symtable.html) module exposes the **symbol tables** CPython builds during compilation: which names are local, global, imported, assigned, or referenced in nested scopes. Use it for static analysis, scope-aware linting, or teaching how Python resolves names. Full attribute reference remains on [docs.python.org](https://docs.python.org/3/library/symtable.html).

Related: [`ast`](../ast-abstract-syntax-trees/index.md) for syntax structure; `compile(..., dont_inherit=True)` for runtime code objects.

---

## Core API — [Generating Symbol Tables](https://docs.python.org/3/library/symtable.html#generating-symbol-tables)

| Function / object | Role |
|-------------------|------|
| `symtable.symtable(code, filename, compile_type)` | Build top-level `SymbolTable` from source string |
| `SymbolTable.get_type()` | `'module'`, `'class'`, `'function'`, or `'annotation'` |
| `SymbolTable.get_identifiers()` | Names defined in this block |
| `SymbolTable.lookup(name)` | Return `Symbol` metadata for one identifier |
| `SymbolTable.get_children()` | Nested block tables (functions, classes, comprehensions) |
| `Symbol.get_namespace()` | Same scope categories as the table |
| `Symbol.is_global()`, `.is_local()`, `.is_nonlocal()`, `.is_free()` | Binding classification flags |

```python
# Goal: list locals in a function block
import symtable

source = "def f(x, y=1):\n    z = x + y\n    return z\n"
table = symtable.symtable(source, "<demo>", "exec")
func_table = table.lookup("f").get_namespace()
assert func_table.get_type() == "function"
assert set(func_table.get_identifiers()) >= {"x", "y", "z"}
```

```python
# Goal: detect a global assignment
import symtable

source = "count = 0\ndef bump():\n    global count\n    count += 1\n"
table = symtable.symtable(source, "<demo>", "exec")
bump = table.lookup("bump").get_namespace()
sym = bump.lookup("count")
assert sym.is_global()
assert sym.is_assigned()
```

---

## Scope types

| `get_type()` | Meaning |
|--------------|---------|
| `module` | Top-level module body |
| `class` | Class body (special name binding rules) |
| `function` | Function or lambda body |
| `annotation` | PEP 563 postponed annotation block (when applicable) |

```python
# Goal: walk nested symbol tables
import symtable

source = "class C:\n    def method(self):\n        pass\n"
table = symtable.symtable(source, "<demo>", "exec")
class_table = table.lookup("C").get_namespace()
children = class_table.get_children()
assert len(children) == 1
assert children[0].get_type() == "function"
assert "self" in children[0].get_identifiers()
```

---

## Comprehension and class-body quirks

| Situation | symtable behavior |
|-----------|-------------------|
| List/set/dict comprehensions | Often get their own nested `function`-typed block |
| Class body | Assignments create class-local names, not closure locals |
| `global` / `nonlocal` | Reflected in `Symbol` flags before bytecode emission |

Prefer **`symtable`** over guessing from `ast` when you need the compiler's final binding decisions (especially for comprehensions and `global`).

---

## Best practices

| Practice | Why |
|----------|-----|
| Pass a descriptive **`filename`** | Error messages and debugging |
| Use **`compile_type='exec'`** for modules, `'eval'` / `'single'` for other modes | Must match how the code will run |
| Combine with **`ast`** for source spans, **`symtable`** for binding | AST gives syntax; symtable gives scope |

---

## See also

- [`ast`](../ast-abstract-syntax-trees/index.md) — parse trees
- [`dis`](../dis-disassembler-for-python-bytecode/index.md) — see `LOAD_FAST` / `LOAD_GLOBAL` in bytecode
