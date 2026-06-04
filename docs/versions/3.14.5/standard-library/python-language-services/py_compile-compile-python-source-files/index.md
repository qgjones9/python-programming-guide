# [py_compile — Compile Python source files](https://docs.python.org/3/library/py_compile.html)

The [`py_compile`](https://docs.python.org/3/library/py_compile.html) module compiles a single **`.py` source file** to **bytecode** and writes a **`.pyc`** cache file (or a caller-specified path). Importers use the same machinery when loading modules. Full parameters and exception types remain on [docs.python.org](https://docs.python.org/3/library/py_compile.html).

Related: [`compileall`](../compileall-byte-compile-python-libraries/index.md) for trees; [`importlib.util`](../../importing-modules/importlib-the-implementation-of-import/index.md) cache layout.

---

## Core functions — [Single-file compilation](https://docs.python.org/3/library/py_compile.html)

| Function | Role |
|----------|------|
| `py_compile.compile(source, cfile=None, dfile=None, doraise=False, ...)` | Compile `source` path to bytecode file |
| `py_compile.PyCompileError` | Wraps `SyntaxError` with filename context |
| `py_compile.compile(..., optimize=0\|1\|2)` | Strip asserts/docstrings at higher optimization |
| `py_compile.compile(..., invalidation_mode=...)` | Control timestamp vs hash-based cache invalidation |

```python
# Goal: compile a temp module and verify .pyc exists
import os
import py_compile
import tempfile

source = "VALUE = 42\n"
with tempfile.TemporaryDirectory() as tmp:
    py_path = os.path.join(tmp, "demo.py")
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(source)
    pyc_path = py_compile.compile(py_path, doraise=True)
    assert os.path.isfile(pyc_path)
    assert pyc_path.endswith(".pyc") or "__pycache__" in pyc_path
```

```python
# Goal: SyntaxError surfaces as PyCompileError when doraise=True
import os
import py_compile
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    bad = os.path.join(tmp, "bad.py")
    with open(bad, "w", encoding="utf-8") as f:
        f.write("def oops(\n")
    try:
        py_compile.compile(bad, doraise=True)
    except py_compile.PyCompileError as exc:
        assert "bad.py" in str(exc)
    else:
        raise AssertionError("expected PyCompileError")
```

---

## Cache layout (PEP 3147)

| Component | Meaning |
|-----------|---------|
| `__pycache__/module.cpython-314.pyc` | Default cache path next to source |
| `opt-N` tag | Optimization level embedded in filename |
| Hash-based pyc | Invalidates when source content changes, not mtime alone |

```python
# Goal: explicit cfile path
import os
import py_compile
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    src = os.path.join(tmp, "m.py")
    dst = os.path.join(tmp, "custom.pyc")
    with open(src, "w", encoding="utf-8") as f:
        f.write("pass\n")
    out = py_compile.compile(src, cfile=dst, doraise=True)
    assert out == dst
    assert os.path.getsize(dst) > 0
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Set **`doraise=True`** in build scripts | Silent failure returns `None` / prints to stderr by default |
| Use **`compileall`** for packages | One call recurses `__pycache__` for entire trees |
| Match **`optimize`** to production | `-O` / `-OO` change bytecode and `.pyc` names |

---

## See also

- [`compileall`](../compileall-byte-compile-python-libraries/index.md) — recursive compilation
- [`dis`](../dis-disassembler-for-python-bytecode/index.md) — inspect resulting bytecode
