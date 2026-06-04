# [site — Site-specific configuration hook](https://docs.python.org/3/library/site.html)

The [`site`](https://docs.python.org/3/library/site.html) module runs during **startup** (unless `-S` is passed) to append **site-packages** directories to `sys.path`, enable user-site (`~/.local/...`), and execute optional **`sitecustomize`** / **`usercustomize`** hooks. Reference: [docs.python.org](https://docs.python.org/3/library/site.html).

---

## Startup behavior

| Step | Effect |
|------|--------|
| `site.main()` | Called automatically after `sys.path` initialization |
| `addsitepackages(known_paths, …)` | Adds lib-dynload and site-packages paths |
| `addsitedir(path, known_paths=…)` | Process `.pth` files in a directory |
| `ENABLE_USER_SITE` | Toggle whether user site is used |
| `sitecustomize` / `usercustomize` modules | Distributor or user hooks if importable |

Pass **`-S`** to `python` to skip all site processing (isolated mode).

---

## Path helpers

| Function | Role |
|----------|------|
| `getsitepackages()` | List of global site-package dirs |
| `getusersitepackages()` | User-specific site dir |
| `getuserbase()` | Base dir for user installs |

Virtual environments adjust paths via `pyvenv.cfg`; see [`venv`](../../software-packaging-and-distribution/venv-creation-of-virtual-environments/index.md).

```python
# Goal: read site path configuration
import site

paths = site.getsitepackages()
assert isinstance(paths, list)
assert all(isinstance(p, str) for p in paths)
user = site.getusersitepackages()
assert isinstance(user, str)
assert site.ENABLE_USER_SITE in (True, False, None)
```

---

## `.pth` files

Lines in `*.pth` under site-packages can append paths or import modules (lines starting with `import`). Malicious `.pth` files are a supply-chain risk — protect write access to site-packages.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`python -m venv`** instead of manual `PYTHONPATH` | Leverages site machinery correctly |
| Avoid **`usercustomize` in production images** | Hidden global imports |
| Prefer **`pip install --prefix`** understanding site layout | Know where `site.addsitedir` will look |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `-S` breaks installed packages | Nothing on sys.path from site | Install into explicit path or use venv |
| Editable installs + stale `.pth` | Import wrong version | Reinstall package |
| Assuming site runs in embedded interpreters | May be disabled | Call `site.main()` if needed |

---

## See also

- [`sysconfig`](../sysconfig-provide-access-to-pythons-configuration-information/index.md) — install scheme paths
- [`sys`](../sys-system-specific-parameters-and-functions/index.md) — `sys.path` after site runs
