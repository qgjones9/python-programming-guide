# [ensurepip — Bootstrapping the pip installer](https://docs.python.org/3/library/ensurepip.html)

[`ensurepip`](https://docs.python.org/3/library/ensurepip.html) bootstraps a **bundled snapshot of pip** into the current interpreter or virtual environment. It does **not** access the network — wheels ship inside CPython. Most users never call it directly because venv and installers bootstrap pip by default; use it when pip was skipped or removed. Full options and availability notes are on [docs.python.org](https://docs.python.org/3/library/ensurepip.html).

**Availability:** not Android, iOS, or WASI. Optional on some distributor builds.

---

## Command-line interface — [Command-line interface](https://docs.python.org/3/library/ensurepip.html#command-line-interface)

| Flag | Effect |
|------|--------|
| (none) | Install pip if missing; no-op if already present |
| `--upgrade` | Ensure pip is at least as new as the bundled version |
| `--root DIR` | Install relative to an alternate root |
| `--user` | User site-packages (disallowed inside an active venv) |
| `--altinstall` | Skip the unversioned `pipX` script |
| `--default-pip` | Also install a `pip` script |

```text
python -m ensurepip --upgrade
```

Prefer the CLI in a **subprocess** — bootstrapping mutates `sys.path` and `os.environ` when invoked in-process.

---

## Module API — [Module API](https://docs.python.org/3/library/ensurepip.html#module-api)

| Function | Purpose |
|----------|---------|
| `ensurepip.version()` | Bundled pip version string available for bootstrap |
| `ensurepip.bootstrap(...)` | Programmatic install with `root`, `upgrade`, `user`, script flags |

`bootstrap()` raises an auditing event `ensurepip.bootstrap`. Setting both `altinstall` and `default_pip` raises `ValueError`.

```python
# Goal: inspect bundled pip version without installing
import ensurepip

bundled = ensurepip.version()
assert isinstance(bundled, str) and bundled[0].isdigit()
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Run **`python -m ensurepip`** in CI recovery scripts | Clear subprocess boundary avoids path pollution |
| Follow with **`python -m pip install --upgrade pip`** | Bundled version may lag PyPI |
| Use **`--user`** only outside venvs | venv rejects user-scheme installs |
| Do not rely on ensurepip-installed deps | pip's own dependencies may change between releases |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Calling `bootstrap()` in a running app | Side effects on import path | Subprocess CLI instead |
| Expecting latest pip from ensurepip alone | Only guarantees bundled minimum | Upgrade via pip afterward |
| Missing optional module on distro Python | ImportError or absent `-m ensurepip` | Install distro `python3-ensurepip` package |

---

## See also

- [`venv`](../venv-creation-of-virtual-environments/index.md) — creates environments with pip by default
- [Installing Python packages (PyPA guide)](https://packaging.python.org/en/latest/tutorials/installing-packages/)
- [PEP 453](https://peps.python.org/pep-0453/) — explicit pip bootstrapping rationale
