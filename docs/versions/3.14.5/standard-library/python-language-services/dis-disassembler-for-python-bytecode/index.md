# [dis — Disassembler for Python bytecode](https://docs.python.org/3/library/dis.html)

The [`dis`](https://docs.python.org/3/library/dis.html) module **disassembles Python bytecode**: opcodes, jump targets, line numbers, and exception tables. Use it to understand what `compile()` and the interpreter actually execute. Opcode reference and specialized helpers remain on [docs.python.org](https://docs.python.org/3/library/dis.html).

Related: [`ast`](../ast-abstract-syntax-trees/index.md) (source), [`pickletools`](../pickletools-tools-for-pickle-developers/index.md) (pickle opcodes, different format).

---

## Core functions — [Bytecode analysis](https://docs.python.org/3/library/dis.html#bytecode-analysis)

| Function | Role |
|----------|------|
| `dis.dis(x=None)` | Print disassembly of function, method, code object, or source string |
| `dis.disassemble(code, lasti=-1, ...)` | Disassemble a code object |
| `dis.bytecode(x)` | `Bytecode` iterable wrapper |
| `dis.show_code(code)` | Human-readable code object summary |
| `dis.get_instructions(x)` | Iterator of `Instruction` named tuples |
| `dis.opname` / `dis.opmap` | Opcode index ↔ name mappings |

```python
# Goal: inspect opcodes for a simple function
import dis

def add(a, b):
    return a + b

instrs = list(dis.get_instructions(add))
opnames = [i.opname for i in instrs]
assert "BINARY_OP" in opnames or "BINARY_ADD" in opnames
assert any(i.opname == "RETURN_VALUE" for i in instrs)
```

```python
# Goal: disassemble compile() output
import dis

code = compile("x = 1 + 2", "<snippet>", "exec")
names = [i.argval for i in dis.get_instructions(code) if i.argval == "x"]
assert names == ["x"]
```

---

## `Instruction` fields

| Field | Meaning |
|-------|---------|
| `opname` | Opcode name (`LOAD_CONST`, `STORE_NAME`, …) |
| `arg` / `argval` | Numeric arg and resolved constant/name index |
| `offset` | Byte offset in code string |
| `starts_line` | Source line number when line changes |
| `is_jump_target` | Label destination for control flow |

```python
# Goal: find constant operands in bytecode
import dis

def f():
    a, b = 1, 2
    return a + b

const_tuples = [
    i.argval
    for i in dis.get_instructions(f)
    if i.opname == "LOAD_CONST" and isinstance(i.argval, tuple)
]
assert (1, 2) in const_tuples
```

---

## Specialized disassembly (3.11+)

| API | Use |
|-----|-----|
| `dis.disassemble(code, show_caches=True)` | Show inline cache entries |
| Exception table entries | Printed for `try`/`except`/`finally` regions |
| `dis.stack_effect(opcode, oparg, ...)` | Static stack delta for an opcode |

```python
# Goal: capture dis output without printing
import dis
import io

code = compile("pass", "<x>", "exec")
buf = io.StringIO()
dis.dis(code, file=buf)
text = buf.getvalue()
assert "RESUME" in text or "RETURN" in text
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Disassemble **`function.__code__`**, not the wrapper | Decorators replace the callable object |
| Compare bytecode across Python versions carefully | Opcode set evolves (`BINARY_OP`, specialized calls) |
| Use **`show_code`** first for constants and varnames | Faster orientation before full `dis` dump |

---

## See also

- [`compile`](../../built-in-functions/compile/index.md) — build code objects from source/AST
- [`pickletools`](../pickletools-tools-for-pickle-developers/index.md) — pickle format disassembly
