# [sysconfig — Provide access to Python's configuration information](https://docs.python.org/3/library/sysconfig.html)

[`sysconfig`](https://docs.python.org/3/library/sysconfig.html) exposes **installation layout** from the build that produced the running interpreter: standard paths, Makefile-style config variables, and named **installation schemes** (posix_prefix, venv, etc.). Use it when packaging tools need `include`/`stdlib` locations without hard-coding. Reference: [docs.python.org](https://docs.python.org/3/library/sysconfig.html).

---

## Path schemes

| Function | Returns |
|----------|---------|
| `get_path(name, scheme=…, vars=…)` | Single path (`stdlib`, `platstdlib`, `purelib`, `platlib`, …) |
| `get_paths(scheme=…, vars=…)` | Dict of all path names for a scheme |
| `get_scheme_names()` | Available scheme keys |
| `get_default_scheme()` | Scheme selected for this platform/context |

Inside an active venv, defaults follow the **venv scheme** automatically.

---

## Build variables

| Function | Returns |
|----------|---------|
| `get_config_var(name)` | One Makefile variable (`prefix`, `VERSION`, …) |
| `get_config_vars(*names)` | Dict of variables |
| `get_platform()` | Platform string used at build time |
| `get_python_version()` | `major.minor` string |

```python
# Goal: discover stdlib path and version for the running interpreter
import sysconfig

paths = sysconfig.get_paths()
assert "stdlib" in paths and paths["stdlib"]
version = sysconfig.get_python_version()
assert version.count(".") == 1
prefix = sysconfig.get_config_var("prefix")
assert prefix
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Pass **`vars={'base': …, 'platbase': …}`** when cross-compiling layouts | Substitutions in path templates |
| Use **`get_default_scheme()`** instead of hard-coded `posix_prefix` | Correct on Windows and in venvs |
| Prefer **`sysconfig`** over parsing `sys.path` heuristics | Matches how CPython was installed |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Assuming `purelib == platlib` | Split on some POSIX layouts | Query both when installing |
| Embedding paths from build machine | Broken relocatable installs | Re-query on target interpreter |

---

## See also

- [`sys`](../sys-system-specific-parameters-and-functions/index.md) — runtime `prefix` and path
- [`venv`](../../software-packaging-and-distribution/venv-creation-of-virtual-environments/index.md) — venv scheme integration
- [`site`](../site-site-specific-configuration-hook/index.md) — runtime site-packages augmentation
