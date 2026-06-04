# [zipimport — Import modules from Zip archives](https://docs.python.org/3/library/zipimport.html)

[`zipimport`](https://docs.python.org/3/library/zipimport.html) lets the import machinery load **`.py` and `.pyc` modules** (and packages) from **ZIP-format archives** on `sys.path`. You rarely import `zipimport` explicitly—adding `something.zip` to `sys.path` is enough. Dynamic extension modules (`.so`, `.pyd`) inside ZIPs are **not** supported. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/zipimport.html).

---

## How ZIP entries appear on `sys.path`

| `sys.path` entry | Lookup behavior |
|------------------|-----------------|
| `example.zip` | Modules at archive root |
| `example.zip/lib/` | Only under `lib/` inside the archive |

ZIP64 and archives with comments are supported (3.8+ / 3.13+). Without `.pyc` files inside the archive, imports may be slower because Python will not write bytecode into the ZIP.

---

## `zipimporter` — [zipimporter Objects](https://docs.python.org/3/library/zipimport.html#zipimporter-objects)

| Attribute / method | Role |
|--------------------|------|
| `archive`, `prefix` | ZIP file path and subpath within it |
| `find_spec(fullname, target=None)` | PEP 451 finder hook |
| `get_code` / `get_source` / `get_data` | Access module bytecode, source, or raw bytes |
| `is_package(fullname)` | Whether `fullname` is a package |
| `invalidate_caches()` | Clear internal file-info cache (3.10+) |
| `ZipImportError` | Subclass of `ImportError` for ZIP-specific failures |

```python
# Goal: import a module from a temporary zip on sys.path
import os
import sys
import tempfile
import zipfile
import zipimport

code = "VALUE = 'from_zip'\n"
with tempfile.TemporaryDirectory() as tmp:
    zpath = os.path.join(tmp, "demo.zip")
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("demo_mod.py", code)
    importer = zipimport.zipimporter(zpath)
    assert importer.is_package("demo_mod") is False
    source = importer.get_source("demo_mod")
    assert "from_zip" in source
    sys.path.insert(0, zpath)
    try:
        import demo_mod
        assert demo_mod.VALUE == "from_zip"
        assert demo_mod.__file__.startswith(zpath)
    finally:
        sys.path.remove(zpath)
        sys.modules.pop("demo_mod", None)
```

```python
# Goal: get_data reads arbitrary bytes from the archive
import os
import tempfile
import zipfile
import zipimport

with tempfile.TemporaryDirectory() as tmp:
    zpath = os.path.join(tmp, "data.zip")
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("readme.txt", b"hello zip")
    imp = zipimport.zipimporter(zpath)
    assert imp.get_data("readme.txt") == b"hello zip"
```

---

## Integration with `importlib`

Modern loaders implement `create_module` / `exec_module` and `find_spec` rather than deprecated `load_module` (removed in 3.12). Custom meta path finders should follow the same protocols documented under [`importlib`](../importlib-the-implementation-of-import/index.md).

---

## Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Expecting `.so` inside ZIP | Ship extensions on the filesystem or use a different layout |
| No `.pyc` in archive | Accept slower imports or pre-compile into the ZIP |
| Stale cache after ZIP rebuild | Call `invalidate_caches()` on the importer |
