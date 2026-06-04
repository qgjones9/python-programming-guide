# [zipapp — Manage executable Python zip archives](https://docs.python.org/3/library/zipapp.html)

[`zipapp`](https://docs.python.org/3/library/zipapp.html) builds **`.pyz` zip application archives** that CPython executes directly when they contain a top-level [`__main__.py`](../../python-runtime-services/__main__-top-level-code-environment/index.md). Optional shebang lines make archives runnable on POSIX; the Windows launcher handles `.pyz`/`.pyzw`. Full format spec and CLI flags: [docs.python.org](https://docs.python.org/3/library/zipapp.html).

Added in Python 3.5; compression (`--compress`) in 3.7.

---

## Basic usage — [Basic Example](https://docs.python.org/3/library/zipapp.html#basic-example)

```text
python -m zipapp myapp -m "myapp:main"
python myapp.pyz
```

| CLI option | Effect |
|------------|--------|
| `-o`, `--output` | Output filename (required when source is already an archive) |
| `-p`, `--python` | Shebang interpreter line + executable bit (POSIX) |
| `-m`, `--main` | Synthesize `__main__.py` calling `pkg.mod:callable` |
| `-c`, `--compress` | Deflate-compress member files |
| `--info` | Print embedded interpreter from shebang |

---

## Python API — [Python API](https://docs.python.org/3/library/zipapp.html#python-api)

| Function | Purpose |
|----------|---------|
| `create_archive(source, target=None, …)` | Build or copy archive from directory, path, or file object |
| `get_interpreter(archive)` | Parse shebang from archive start; `None` if absent |

`filter=` callback receives each `Path` and returns whether to include the file. `main=` requires a directory source without an existing `__main__.py`.

```python
# Goal: build a minimal runnable archive and inspect shebang
import tempfile
import zipapp
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    app = Path(tmp) / "app"
    app.mkdir()
    (app / "__main__.py").write_text("RESULT = 'ok'\n")
    target = Path(tmp) / "demo.pyz"
    zipapp.create_archive(app, target, interpreter="/usr/bin/env python3")
    assert target.is_file()
    assert zipapp.get_interpreter(target) == "/usr/bin/env python3"
```

---

## Standalone applications — [Creating Standalone Applications with zipapp](https://docs.python.org/3/library/zipapp.html#creating-standalone-applications-with-zipapp)

Typical bundle steps:

1. Lay out application code with `__main__.py`.
2. `python -m pip install -r requirements.txt --target myapp`.
3. `python -m zipapp -p "interpreter" myapp`.

**Caveat:** packages with **C extensions** cannot run from inside the zip — exclude them and ship native wheels beside the archive, or adjust `sys.path` at startup.

---

## Archive format — [The Python Zip Application Archive Format](https://docs.python.org/3/library/zipapp.html#the-python-zip-application-archive-format)

| Part | Content |
|------|---------|
| Optional shebang | `b'#!'` + interpreter + newline (UTF-8 on Windows) |
| Zip payload | Standard zip data; **must** include root-level `__main__.py` |

The zip parent directory is prepended to `sys.path` at execution time.

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`/usr/bin/env python3`** shebang | Survives different install prefixes |
| Avoid **`python3.14`-style exact minors** | Breaks when users upgrade patch releases |
| Use **`filter=`** to omit tests and `__pycache__` | Smaller distributable |
| Test on target OS **launcher** behavior | Shebang semantics differ Windows vs POSIX |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Native extensions in zip | ImportError / loader failure | External wheels + path hack |
| Missing root `__main__.py` | Archive not executable | Add file or use `-m` |
| In-place shebang rewrite without backup | Corrupted archive on error | Write to temp then replace |

---

## See also

- [`__main__`](../../python-runtime-services/__main__-top-level-code-environment/index.md) — entry-point semantics
- [`zipfile`](../../data-compression-and-archiving/zipfile-work-with-zip-archives/index.md) — underlying archive format
- [Specifying the Interpreter](https://docs.python.org/3/library/zipapp.html#specifying-the-interpreter)
