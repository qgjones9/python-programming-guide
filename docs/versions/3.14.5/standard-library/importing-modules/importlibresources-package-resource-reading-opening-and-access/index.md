# [importlib.resources – Package resource reading, opening and access](https://docs.python.org/3/library/importlib.resources.html)

[`importlib.resources`](https://docs.python.org/3/library/importlib.resources.html) uses the import system to read **non-Python assets** shipped inside packages—data files, configs, images—whether they live on disk, in a **ZIP archive**, or behind a custom loader. The modern API centers on **`files()`** and **`Traversable`** objects; older one-shot helpers (`read_text`, `path`, …) remain for compatibility. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/importlib.resources.html).

---

## Modern API (3.9+)

| Function | Returns / behavior |
|----------|-------------------|
| `files(anchor=None)` | `Traversable` root for the anchor package or module |
| `as_file(traversable)` | Context manager yielding `pathlib.Path` (may extract from zip) |

**Anchor** (3.12+): `str` module name, module object, or omitted (caller’s module). Prefer positional anchor over deprecated `package=` keyword.

```python
# Goal: traverse package tree with files()
from importlib import resources

root = resources.files("importlib")
assert root.is_dir()
children = {p.name for p in root.iterdir()}
assert "__init__.py" in children or any(children)
```

```python
# Goal: read_text on a traversable file
from importlib import resources

init_py = resources.files("importlib").joinpath("__init__.py")
text = init_py.read_text(encoding="utf-8")
assert "importlib" in text
```

```python
# Goal: as_file yields a real path for APIs that need pathlib
from importlib import resources

trav = resources.files("importlib").joinpath("__init__.py")
with resources.as_file(trav) as path:
    assert path.is_file()
    assert path.read_text(encoding="utf-8")
```

---

## Functional helpers — [Functional API](https://docs.python.org/3/library/importlib.resources.html#functional-api)

| Function | Notes |
|----------|-------|
| `read_text(anchor, *path_names, encoding='utf-8')` | Multiple path segments since 3.13 |
| `read_binary(anchor, *path_names)` | Raw bytes |
| `open_text` / `open_binary` | Stream handles |
| `is_resource(anchor, *path_names)` | `True` only for files, not directories |
| `path(anchor, *path_names)` | Deprecated context manager; use `as_file(files(...))` |
| `contents(anchor, *path_names)` | Deprecated; use `iterdir()` |

```python
# Goal: read_binary loads bytes from a known stdlib file
from importlib import resources

data = resources.read_binary("importlib", "_bootstrap.py")
assert b"ModuleSpec" in data or len(data) > 100
```

---

## Security

Resources follow the same trust model as built-in **`open()`**: do not pass untrusted path segments to `joinpath` without validation.

---

## Loader contract

Loaders that support resources should implement **`get_resource_reader()`** or (preferred) **`TraversableResources.files()`** as described in [`importlib.resources.abc`](../importlibresourcesabc-abstract-base-classes-for-resources/index.md).

---

## Migration from `pkgutil.get_data`

| Old | New |
|-----|-----|
| `pkgutil.get_data(pkg, "r.txt")` | `resources.files(pkg).joinpath("r.txt").read_bytes()` |
| `pkg_resources` | `importlib.resources` + `importlib.metadata` |
