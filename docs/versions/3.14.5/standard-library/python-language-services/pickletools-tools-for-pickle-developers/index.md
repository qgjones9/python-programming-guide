# [pickletools — Tools for pickle developers](https://docs.python.org/3/library/pickletools.html)

The [`pickletools`](https://docs.python.org/3/library/pickletools.html) module documents and **disassembles the pickle wire protocol**—the stack-based bytecode `pickle` uses to serialize objects. It is for protocol debugging and education, not for loading untrusted data. Full opcode tables remain on [docs.python.org](https://docs.python.org/3/library/pickletools.html).

Related: [`pickle`](../../data-persistence/pickle-python-object-serialization/index.md) (encoder/decoder); [`dis`](../dis-disassembler-for-python-bytecode/index.md) (Python bytecode, different format).

---

## Core functions — [Command-line usage](https://docs.python.org/3/library/pickletools.html#command-line-usage)

| Function | Role |
|----------|------|
| `pickletools.dis(pickle, out=None, memo=None, ...)` | Annotated disassembly of pickle bytes |
| `pickletools.genops(pickle)` | Yield `(opcode, arg, pos)` for each operation |
| `pickletools.optimize(pickle)` | Remove unused PUT opcodes (shrink blobs) |
| `pickletools.dis(..., annotate=1)` | Add protocol-level comments |
| `pickletools.opcodes` | List of `OpcodeInfo` metadata objects |

```python
# Goal: disassemble a minimal pickle
import io
import pickle
import pickletools

data = pickle.dumps({"a": 1}, protocol=pickle.HIGHEST_PROTOCOL)
buf = io.StringIO()
pickletools.dis(data, out=buf)
text = buf.getvalue()
assert "dict" in text.lower() or "SETITEM" in text
```

```python
# Goal: iterate opcodes with genops
import pickle
import pickletools

data = pickle.dumps([1, 2, 3], protocol=4)
ops = [op.name for op, arg, pos in pickletools.genops(data)]
assert "EMPTY_LIST" in ops or "MARK" in ops
assert "STOP" in ops
```

---

## `OpcodeInfo` highlights

| Attribute | Meaning |
|-----------|---------|
| `name` | Opcode mnemonic (`BININT`, `GLOBAL`, …) |
| `code` | Single-byte or multi-byte opcode identifier |
| `arg` | Whether an argument follows |
| `stack_before` / `stack_after` | Stack effect documentation |
| `proto` | Minimum protocol version introducing the opcode |

```python
# Goal: optimize removes redundant PUTs when possible
import pickle
import pickletools

original = pickle.dumps({"k": "v" * 100}, protocol=4)
optimized = pickletools.optimize(original)
assert len(optimized) <= len(original)
assert pickle.loads(optimized) == pickle.loads(original)
```

---

## Security note

**Never** use `pickletools` output to justify loading pickles from untrusted sources. Disassembly does not sandbox **`GLOBAL`** / **`REDUCE`** opcodes that can execute arbitrary callables during **`pickle.loads`**.

```python
# Goal: compare protocol sizes (illustrative)
import pickle

obj = list(range(100))
sizes = {p: len(pickle.dumps(obj, protocol=p)) for p in range(pickle.HIGHEST_PROTOCOL + 1)}
assert sizes[pickle.HIGHEST_PROTOCOL] <= sizes[0]
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`protocol=pickle.HIGHEST_PROTOCOL`** for size/speed | Older protocols lack efficient opcodes |
| Run **`pickletools.optimize`** on cached blobs | Safe when round-trip equality holds |
| Use **`dis(..., annotate=1)`** when learning the stack machine | Comments map ops to Python values |

---

## See also

- [`pickle`](../../data-persistence/pickle-python-object-serialization/index.md) — serialization API
- [`dis`](../dis-disassembler-for-python-bytecode/index.md) — Python VM bytecode
