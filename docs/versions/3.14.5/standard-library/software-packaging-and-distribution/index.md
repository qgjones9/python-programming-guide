# [Software Packaging and Distribution](https://docs.python.org/3/library/distribution.html)

The **Software Packaging and Distribution** section covers stdlib tools for **installing**, **isolating**, and **shipping** Python code. These modules work with PyPI or private indexes, but also support offline or local-only workflows. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/distribution.html); this hub orients you to each module and typical workflows.

Related material elsewhere: [`importlib.metadata`](../import-and-export-modules/importlib-metadata/index.md) for reading installed package metadata, [`distutils`](https://docs.python.org/3/library/distutils.html) (legacy build helpers), and the [Python Packaging User Guide](https://packaging.python.org/).

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`ensurepip`](ensurepip-bootstrapping-the-pip-installer/index.md) | Bootstrap a bundled `pip` into an environment (offline, no network) |
| [`venv`](venv-creation-of-virtual-environments/index.md) | Create lightweight per-project virtual environments |
| [`zipapp`](zipapp-manage-executable-python-zip-archives/index.md) | Build executable `.pyz` zip archives for distribution |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Isolate project dependencies from system Python | [`venv`](venv-creation-of-virtual-environments/index.md) |
| Restore `pip` after a minimal install or uninstall | [`ensurepip`](ensurepip-bootstrapping-the-pip-installer/index.md) |
| Ship a single-file runnable app (pure Python) | [`zipapp`](zipapp-manage-executable-python-zip-archives/index.md) |
| Install packages from PyPI inside a venv | `python -m pip install …` (after venv + ensurepip bootstrap) |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Commit **requirements** or **`pyproject.toml`**, not the venv | Environments are disposable; lock files belong in source control |
| Use **`python -m pip`** instead of bare `pip` | Guarantees pip matches the interpreter you intend |
| Pin **interpreter shebangs** in zipapps for portability | `/usr/bin/env python3` beats a hard-coded minor version |
| Treat **ensurepip** as bootstrap only | Upstream bundles a snapshot; upgrade with `pip install --upgrade pip` |
| Exclude **C-extension wheels** from zipapps when needed | Native `.so`/`.pyd` cannot load from inside a zip |

```python
# Goal: typical workflow — venv creation without pip side effects in this demo
import tempfile
import venv
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    env = Path(tmp) / ".venv"
    venv.EnvBuilder(with_pip=False).create(env)
    assert (env / "pyvenv.cfg").read_text().startswith("home =")
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Copying a venv to another machine | Broken paths in `pyvenv.cfg` | Recreate with same Python version on target |
| Assuming ensurepip hits the network | It does not — bundled wheels only | Use `pip` after bootstrap for PyPI access |
| Packing extension modules into `.pyz` | OS loader cannot map code from zip | Ship wheels beside the archive or use PyInstaller |
| Running ensurepip in-process | Mutates `sys.path` / `os.environ` | Prefer `python -m ensurepip` in a subprocess |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [ensurepip — Bootstrapping the pip installer](ensurepip-bootstrapping-the-pip-installer/index.md) | Offline pip bootstrap CLI and module API |
| [venv — Creation of virtual environments](venv-creation-of-virtual-environments/index.md) | `EnvBuilder`, activation, isolation flags |
| [zipapp — Manage executable Python zip archives](zipapp-manage-executable-python-zip-archives/index.md) | `.pyz` format, shebang, standalone bundles |
