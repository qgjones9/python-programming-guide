# [PendingDeprecationWarning](https://docs.python.org/3/library/exceptions.html#PendingDeprecationWarning)

`PendingDeprecationWarning` is for features that are **obsolete and expected to become deprecated**, but are not formally deprecated yet. It is rarely used; [`DeprecationWarning`](deprecationwarning/index.md) is preferred once deprecation is active. Canonical docs: [exceptions.html#PendingDeprecationWarning](https://docs.python.org/3/library/exceptions.html#PendingDeprecationWarning).

---

## Purpose

Give early notice to Python developers before an API enters active deprecation. The distinction is subtle—most projects skip straight to `DeprecationWarning`.

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Default filter | **Ignored** (`ignore::PendingDeprecationWarning`) |
| Development mode | Shown |
| Tests | Use `-Wd` / `PYTHONWARNINGS=default` or `simplefilter("always")` in unit tests |

---

## When to emit

Almost never in new code. Consider it only when you need a long runway before `DeprecationWarning` and your audience is exclusively other Python developers. If the feature is already deprecated, use `DeprecationWarning`.

---

## Best practices

- Prefer `DeprecationWarning` unless you have a documented multi-release “pending” phase.
- Same `stacklevel` and message clarity rules as other developer warnings.
- Document the timeline for promotion to `DeprecationWarning` or removal.

---

## Example — capture with an explicit filter

```python
import warnings

def experimental_api():
    warnings.warn(
        "experimental_api is obsolete and may be deprecated soon",
        PendingDeprecationWarning,
        stacklevel=2,
    )

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    experimental_api()
    assert issubclass(log[-1].category, PendingDeprecationWarning)
```

---

## See also

- [DeprecationWarning](../deprecationwarning/index.md)
- [PEP 387 — Deprecation policy](https://peps.python.org/pep-0387/)
