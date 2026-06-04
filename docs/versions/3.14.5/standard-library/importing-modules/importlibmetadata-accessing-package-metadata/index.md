# [importlib.metadata – Accessing package metadata](https://docs.python.org/3/library/importlib.metadata.html)

[`importlib.metadata`](https://docs.python.org/3/library/importlib.metadata.html) reads **installed distribution metadata**—version strings, dependencies, entry points, file lists—from `dist-info` / `egg-info` directories (typically under `site-packages`). It replaces the removed **`pkg_resources`** API for introspection. **Distribution names** (e.g. `PyYAML`) need not match **import names** (e.g. `yaml`); use `packages_distributions()` to map them. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/importlib.metadata.html).

---

## Functional API — [Functional API](https://docs.python.org/3/library/importlib.metadata.html#functional-api)

| Function | Returns |
|----------|---------|
| `version(distribution_name)` | Version string |
| `metadata(distribution_name)` | `PackageMetadata` (PEP 566 fields) |
| `entry_points(**select_params)` | `EntryPoints` collection (console scripts, etc.) |
| `files(distribution_name)` | `PackagePath` objects or `None` |
| `requires(distribution_name)` | Dependency specifiers |
| `distribution(distribution_name)` | `Distribution` instance |
| `packages_distributions()` | Map import top-level names → distribution names |
| `distributions()` | Iterate all installed distributions |

`PackageNotFoundError` (subclass of `ModuleNotFoundError`) is raised when a name is not installed.

```python
# Goal: list installed distributions and read a version
from importlib.metadata import distributions, version

names = sorted({d.metadata["Name"] for d in distributions() if d.metadata.get("Name")})
assert len(names) > 0
# pick any installed distribution for a smoke test
sample = names[0]
assert version(sample)  # non-empty string
```

```python
# Goal: entry_points supports group selection (3.10+)
from importlib.metadata import entry_points

eps = entry_points()
assert hasattr(eps, "select")
groups = sorted(eps.groups)
# every environment has at least one group or empty is ok
assert isinstance(groups, list)
```

```python
# Goal: packages_distributions maps import names to dist names
from importlib.metadata import packages_distributions

mapping = packages_distributions()
assert isinstance(mapping, dict)
# stdlib-only installs still return a dict (possibly empty values)
```

---

## `EntryPoint` objects

| Attribute | Meaning |
|-----------|---------|
| `name`, `group`, `value` | Entry point identity |
| `module`, `attr`, `extras` | Parsed `value` (`module:attr[extras]`) |
| `load()` | Import and return the referenced callable/object |

```python
# Goal: EntryPoint.load resolves callables when entry points exist
from importlib.metadata import entry_points

eps = entry_points().select(group="console_scripts")
if eps.names:
    ep = eps[next(iter(eps.names))]
    obj = ep.load()
    assert callable(obj) or obj is not None
```

---

## `Distribution` and discovery

| Topic | Detail |
|-------|--------|
| `Distribution.read_text("METADATA")` | Raw metadata file |
| `Distribution.locate_file(path)` | Absolute path for a packaged file |
| Custom providers | Subclass `Distribution` + implement `DistributionFinder.find_distributions` on a meta path finder |
| `sys.path` | Metadata search uses path entries (ignores `bytes` paths; accepts `pathlib.Path`) |

---

## vs import names

| Concept | Example |
|---------|---------|
| Distribution (pip name) | `importlib-metadata` |
| Import package | `importlib.metadata` |
| Many-to-one | Namespace `jaraco` → several distributions |

Use **`packages_distributions()`** before assuming `version("requests")` matches `import requests`.

---

## Related

| Module | Role |
|--------|------|
| [`importlib.resources`](../importlibresources-package-resource-reading-opening-and-access/index.md) | Assets **inside** importable packages |
| [`importlib`](../importlib-the-implementation-of-import/index.md) | Import hooks and `ModuleSpec` |
