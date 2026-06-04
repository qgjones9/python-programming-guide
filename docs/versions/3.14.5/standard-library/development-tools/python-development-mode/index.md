# [Python Development Mode](https://docs.python.org/3/library/devmode.html)

**Development Mode** turns on a bundle of **extra runtime checks** intended for local debugging—not production. Enable it with **`python -X dev`**, the environment variable **`PYTHONDEVMODE=1`**, or [`sys.flags.dev_mode`](https://docs.python.org/3/library/sys.html#sys.flags). Canonical reference: [devmode.html](https://docs.python.org/3/library/devmode.html).

---

## What it enables

| Check | Effect |
|-------|--------|
| [`warnings` default action](https://docs.python.org/3/library/devmode.html#devmode-default-warning-action) | `DeprecationWarning` and `ResourceWarning` shown by default |
| [`faulthandler`](https://docs.python.org/3/library/faulthandler.html) | Enabled on startup (tracebacks on fatal errors) |
| [`asyncio` debug mode](https://docs.python.org/3/library/asyncio-dev.html) | Slow callback warnings when asyncio runs |
| Memory allocator debug hooks | Extra validation in debug builds of CPython |
| [`sys.settrace` / auditing](https://docs.python.org/3/library/sys.html#sys.addaudithook) | Compatible with dev tooling |

Development Mode is **not** the same as [`Py_DEBUG`](https://docs.python.org/3/c-api/init.html) builds; it works on standard release binaries.

---

## Example — detect dev mode at runtime

```python
import sys

# In normal scripts this is False unless -X dev / PYTHONDEVMODE=1
is_dev = sys.flags.dev_mode
assert isinstance(is_dev, bool)
```

---

## Example — ResourceWarning surfaces in dev mode

```python
import warnings

# Simulate what dev mode emphasizes: always show ResourceWarning
with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always", ResourceWarning)
    warnings.warn("unclosed file", ResourceWarning)
    assert any(w.category is ResourceWarning for w in log)
```

---

## When to use

| Scenario | Recommendation |
|----------|----------------|
| Local application development | Enable `-X dev` in IDE run configs |
| CI test jobs | Pair with `-W error::DeprecationWarning` for strict upgrades |
| Production deployments | Leave dev mode **off**; configure logging and warnings explicitly |
| Library authors | Test with dev mode; avoid relying on warnings being silent |

---

## See also

- [`-X dev` command-line option](https://docs.python.org/3/using/cmdline.html#cmdoption-X)
- [`faulthandler`](../debugging-and-profiling/faulthandler-dump-the-python-traceback/index.md)
- [`warnings`](https://docs.python.org/3/library/warnings.html)
