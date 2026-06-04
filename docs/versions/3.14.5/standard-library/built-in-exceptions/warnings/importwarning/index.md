# [ImportWarning](https://docs.python.org/3/library/exceptions.html#ImportWarning)

`ImportWarning` flags **probable mistakes in module imports**—ambiguous package layout, deprecated import hooks, or loader edge cases. Canonical docs: [exceptions.html#ImportWarning](https://docs.python.org/3/library/exceptions.html#ImportWarning).

---

## Purpose

Help Python developers catch import-system footguns during development without alarming application end users on every import.

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Default filter | **Ignored** (`ignore::ImportWarning`) |
| Development mode | Shown |
| Tests | Enable with `-Wd`, `PYTHONWARNINGS=default`, or `simplefilter("always")` in test runners |

---

## When to emit

- Custom importers and meta path finders detecting suspicious patterns.
- Standard library import machinery (rare in user code).
- Package maintenance tools warning about namespace or `__init__.py` layout issues.

Most application code never emits `ImportWarning` directly; prefer clear errors for user-facing import failures ([`ImportError`](../../concrete-exceptions/importerror/index.md)).

---

## Best practices

- Reserve for import-system maintainers; message should name the module and suggested fix.
- Run import-heavy test suites with developer warnings visible.
- Use `stacklevel=2` when wrapping import utilities.

---

## Example — simulating an import maintainer notice

```python
import warnings

def load_plugin(name):
    if name.endswith(".py"):
        warnings.warn(
            f"importing {name!r} with .py suffix is unnecessary",
            ImportWarning,
            stacklevel=2,
        )
    return f"plugin:{name}"

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    load_plugin("audio.py")
    assert issubclass(log[-1].category, ImportWarning)
```

---

## See also

- [ImportError](../../concrete-exceptions/importerror/index.md)
- [`warnings` — default filter list](https://docs.python.org/3/library/warnings.html#default-warning-filter)
