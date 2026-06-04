# [faulthandler — Dump the Python traceback](https://docs.python.org/3/library/faulthandler.html)

`faulthandler` dumps **Python tracebacks** on fatal errors, **Unix signals** (when enabled), or **explicit request**—useful when processes hang or crash without a clean exception. Enabled automatically in [Development Mode](../../development-tools/python-development-mode/index.md). Canonical reference: [faulthandler.html](https://docs.python.org/3/library/faulthandler.html).

---

## Purpose

When C extensions abort or threads deadlock, normal `traceback` output may never run. `faulthandler` writes stack dumps to stderr (or a file) from low-level hooks.

---

## Key functions

| Function | Role |
|----------|------|
| `enable(file=..., all_threads=True)` | Register fatal and signal handlers |
| `disable()` | Unregister handlers |
| `dump_traceback(file=..., all_threads=True)` | Dump stacks on demand |
| `dump_traceback_later(timeout, repeat=False)` | Dump after N seconds (watchdog) |
| `cancel_dump_traceback_later()` | Cancel pending watchdog dump |

---

## Example — dump current traceback to StringIO

```python
import faulthandler
import tempfile

with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as f:
    faulthandler.dump_traceback(file=f, all_threads=False)
    f.flush()
    f.seek(0)
    text = f.read()
assert "File" in text
```

---

## Example — enable and disable

```python
import faulthandler

faulthandler.enable()
assert faulthandler.is_enabled() is True
faulthandler.disable()
assert faulthandler.is_enabled() is False
```

---

## C stack extension

On supported platforms, `faulthandler` can also dump the **native C stack** (see upstream section *Dumping the C stack*). Useful when debugging extension modules mixed with Python frames.

---

## Best practices

| Practice | Why |
|----------|-----|
| Enable in long-running services | Speeds diagnosis of stuck workers |
| Use `dump_traceback_later` in CI on hangs | Converts deadlocks into actionable logs |
| Avoid logging secrets in thread stacks | Dumps include local variable frames in some configs |

---

## See also

- [Python Development Mode](../../development-tools/python-development-mode/index.md)
- [`traceback`](https://docs.python.org/3/library/traceback.html)
