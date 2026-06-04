# [importlib.resources.abc – Abstract base classes for resources](https://docs.python.org/3/library/importlib.resources.abc.html)

[`importlib.resources.abc`](https://docs.python.org/3/library/importlib.resources.abc.html) defines the **protocols loaders implement** so [`importlib.resources`](../importlibresources-package-resource-reading-opening-and-access/index.md) can read package assets from the filesystem, zipfiles, or custom storage. **`TraversableResources`** (3.11+) is the current interface; **`ResourceReader`** is deprecated since 3.12. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/importlib.resources.abc.html).

---

## `Traversable` — [class Traversable](https://docs.python.org/3/library/importlib.resources.abc.html#importlib.resources.abc.Traversable)

Path-like API without requiring a real filesystem path:

| Member | Role |
|--------|------|
| `name` | Base name without parents |
| `iterdir()` | Yield child `Traversable` objects |
| `is_dir()` / `is_file()` | Type tests |
| `joinpath(*segments)` | Navigate; segments may contain `/` (3.11+) |
| `open(mode='r', ...)` | Binary or text stream |
| `read_bytes()` / `read_text()` | Convenience readers |
| `/` operator | Same as `joinpath(child)` |

```python
# Goal: stdlib FileLoader exposes TraversableResources via files()
from importlib import resources

trav = resources.files("zoneinfo")
assert trav.is_dir()
# zoneinfo ships tzdata as resources in modern Python
names = {p.name for p in trav.iterdir()}
assert len(names) > 0
```

---

## `TraversableResources` — [class TraversableResources](https://docs.python.org/3/library/importlib.resources.abc.html#importlib.resources.abc.TraversableResources)

| Method | Contract |
|--------|----------|
| `files()` | Return a `Traversable` representing the package root |

Loaders subclassing this ABC also satisfy the older **`ResourceReader`** interface through default adapters.

```python
# Goal: importlib.machinery.FileFinder sources implement the protocol
import importlib.util

spec = importlib.util.find_spec("json")
loader = spec.loader
reader = loader.get_resource_reader("json")
# json has no package resources — reader may be None
assert reader is None or hasattr(reader, "files")
```

---

## Deprecated `ResourceReader` (3.12+)

| Method | Replacement direction |
|--------|----------------------|
| `open_resource(resource)` | `files().joinpath(...).open('rb')` |
| `resource_path(resource)` | `as_file(files().joinpath(...))` |
| `is_resource(path)` | `joinpath(...).is_file()` |
| `contents()` | `iterdir()` names |

Implement **`TraversableResources`** on new loaders rather than `ResourceReader`.

---

## Custom loader sketch

```mermaid
flowchart LR
  L[Loader] --> TR[TraversableResources.files]
  TR --> T[Traversable tree]
  T --> IR[importlib.resources.files]
```

1. Subclass `importlib.abc.Loader` and `TraversableResources`.
2. Implement `files()` returning a traversable rooted at your storage.
3. Register the loader via a meta path finder or path entry finder.

For filesystem packages, CPython’s built-in loaders already implement this—you only need custom ABCs for novel storage (databases, object stores, etc.).
