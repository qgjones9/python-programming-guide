# [compileall — Byte-compile Python libraries](https://docs.python.org/3/library/compileall.html)

The [`compileall`](https://docs.python.org/3/library/compileall.html) module **recursively byte-compiles** directories of Python source—typical before packaging, in CI, or when pre-warming containers. It wraps [`py_compile`](../py_compile-compile-python-source-files/index.md) with filesystem walking and failure reporting. Full CLI flags remain on [docs.python.org](https://docs.python.org/3/library/compileall.html).

Related: [`py_compile`](../py_compile-compile-python-source-files/index.md); `python -m compileall`.

---

## Core functions — [Command-line use](https://docs.python.org/3/library/compileall.html#command-line-use)

| Function | Role |
|----------|------|
| `compileall.compile_dir(dir, maxworkers=1, ...)` | Compile all `.py` under `dir` |
| `compileall.compile_file(fullname, ...)` | Compile one file |
| `compileall.compile_path(skip_cwd=True, ...)` | Compile entries on `sys.path` |
| Return value | `True` if all succeeded, `False` if any failure |

```python
# Goal: compile a small tree in a temp directory
import compileall
import os
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    pkg = os.path.join(tmp, "pkg")
    os.makedirs(pkg)
    with open(os.path.join(pkg, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("VERSION = '1.0'\n")
    with open(os.path.join(pkg, "mod.py"), "w", encoding="utf-8") as f:
        f.write("def run():\n    return VERSION\n")
    ok = compileall.compile_dir(tmp, quiet=1)
    assert ok
    cache = os.path.join(pkg, "__pycache__")
    assert os.path.isdir(cache)
```

```python
# Goal: compile_file reports failure on syntax error
import compileall
import os
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    bad = os.path.join(tmp, "broken.py")
    with open(bad, "w", encoding="utf-8") as f:
        f.write("if\n")
    ok = compileall.compile_file(bad, quiet=1)
    assert not ok
```

---

## Useful parameters

| Parameter | Effect |
|-----------|--------|
| `force=True` | Recompile even if pyc is up to date |
| `optimize=0\|1\|2` | Same as `py_compile.optimize` |
| `invalidation_mode` | Timestamp vs hash-based cache checks |
| `maxworkers` | Parallel compilation (thread pool) |
| `rx` / `stripdir` | Filter which files to compile |

```python
# Goal: force recompilation
import compileall
import os
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "x.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write("X = 1\n")
    assert compileall.compile_dir(tmp, quiet=1)
    assert compileall.compile_dir(tmp, quiet=1, force=True)
```

---

## Command-line

```text
python -m compileall [-l] [-r] [-f] [-q] [-j N] [-o LEVEL] directory ...
```

Use **`-q`** in automation: exit code non-zero when any file fails.

---

## Best practices

| Practice | Why |
|----------|-----|
| Run **`python -m compileall -q src`** in CI | Catches syntax errors without importing side effects |
| Skip virtualenvs and **`site-packages`** unless intentional | Saves time; third parties already ship pyc |
| Pair with **`tabnanny`** or linters | compileall only checks syntax, not style |

---

## See also

- [`py_compile`](../py_compile-compile-python-source-files/index.md) — single-file API
- [`importlib`](../../importing-modules/importlib-the-implementation-of-import/index.md) — import-time cache behavior
