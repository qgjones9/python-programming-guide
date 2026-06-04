# [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)

[`venv`](https://docs.python.org/3/library/venv.html) creates **lightweight, disposable** Python environments: an isolated `site-packages` tree, a `pyvenv.cfg` pointing at the base interpreter, and launcher scripts under `bin/` (POSIX) or `Scripts/` (Windows). Tools like pip install into the active venv automatically. Canonical reference: [docs.python.org](https://docs.python.org/3/library/venv.html).

**Availability:** not Android, iOS, or WASI.

---

## Creating virtual environments — [Creating virtual environments](https://docs.python.org/3/library/venv.html#creating-virtual-environments)

```text
python -m venv /path/to/.venv
source /path/to/.venv/bin/activate   # POSIX
```

| CLI flag | Effect |
|----------|--------|
| `--system-site-packages` | Also see base interpreter's site-packages |
| `--symlinks` / `--copies` | Control whether the python binary is linked or copied |
| `--clear` | Empty an existing target directory first |
| `--upgrade` | Recreate env after in-place Python upgrade |
| `--without-pip` | Skip pip bootstrap |
| `--upgrade-deps` | Upgrade pip (and formerly setuptools) from PyPI |
| `--prompt NAME` | Custom activate prompt prefix |

Environments are **not** portable — recreate on the target machine rather than copying directories.

---

## How venvs work — [How venvs work](https://docs.python.org/3/library/venv.html#how-venvs-work)

| Component | Role |
|-----------|------|
| `pyvenv.cfg` | Records `home`, `include-system-site-packages`, version |
| `bin/python` (or `Scripts\python.exe`) | Launcher tied to base interpreter |
| `lib/pythonX.Y/site-packages/` | Isolated third-party installs |
| `activate` script | Adjusts `PATH` and `VIRTUAL_ENV` in a shell |

When active, `sys.prefix` points at the venv root and pip targets that tree without extra flags.

---

## API — [API](https://docs.python.org/3/library/venv.html#api)

| Symbol | Purpose |
|--------|---------|
| `venv.create(env_dir, …)` | Convenience wrapper around `EnvBuilder` |
| `venv.EnvBuilder` | Hookable builder (`create`, `ensure_directories`, `setup_python`, …) |
| `venv.EnvBuilder.create(env_dir)` | Materialize environment on disk |

Subclass `EnvBuilder` to customize post-create steps (for example installing extra wheels).

```python
# Goal: programmatic venv with pip skipped for speed
import tempfile
import venv
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    env_dir = Path(tmp) / "demo"
    builder = venv.EnvBuilder(with_pip=False, prompt="demo")
    builder.create(env_dir)
    cfg = (env_dir / "pyvenv.cfg").read_text()
    assert "home =" in cfg
    assert (env_dir / "bin" / "python").exists() or (env_dir / "Scripts" / "python.exe").exists()
```

---

## Extending EnvBuilder — [An example of extending EnvBuilder](https://docs.python.org/3/library/venv.html#an-example-of-extending-envbuilder)

Override `post_setup(context)` to run hooks after the skeleton exists — common for seeding config files or running `pip install -r requirements.txt` inside the new env.

---

## Best practices

| Practice | Why |
|----------|-----|
| Name env **`.venv`** and add to `.gitignore` | De facto convention; SCM ignore added by default (3.13+) |
| One venv **per project** | Avoids dependency cross-talk |
| Document **Python version** alongside requirements | venv ties to base interpreter ABI |
| Use **`--upgrade-deps`** on fresh envs** | Keeps pip current without manual step |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Checking venv into Git | Huge diffs, wrong paths for teammates | Ignore + document setup |
| `--system-site-packages` surprises | Base packages shadow venv pins | Default isolation unless intentional |
| Assuming copied venv works elsewhere | Hard-coded `home` path | `python -m venv .venv` on each machine |

---

## See also

- [`ensurepip`](../ensurepip-bootstrapping-the-pip-installer/index.md) — pip bootstrap inside new envs
- [`site`](../../python-runtime-services/site-site-specific-configuration-hook/index.md) — how venvs interact with site path hooks
- [PEP 405](https://peps.python.org/pep-0405/) — virtual environment specification
