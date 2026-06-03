# [UserWarning](https://docs.python.org/3/library/exceptions.html#UserWarning)

`UserWarning` is the default category for [`warnings.warn()`](https://docs.python.org/3/library/warnings.html#warnings.warn) and the usual base for application-level notices that are not deprecations or resource leaks. Full reference text is on [docs.python.org](https://docs.python.org/3/library/exceptions.html#UserWarning).

---

## Purpose

Use `UserWarning` for conditions worth surfacing to someone running the program—configuration quirks, ambiguous inputs, or soft validation failures—when you do **not** need a distinct filter bucket. Libraries often subclass `UserWarning` (e.g. `MyPackageWarning`) so callers can `filterwarnings("ignore", category=MyPackageWarning)`.

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Default filter | `"default"` — first occurrence per `(message, category, module, lineno)` is shown |
| Not in the ignored-by-default set | Unlike `DeprecationWarning`, messages are visible in normal runs |
| `"error"` | Raises `UserWarning(message)` |

---

## When to emit

- Optional or discouraged API paths that still work.
- Data quality issues that do not warrant an exception.
- Generic notices when no more specific built-in category applies.

Prefer [`DeprecationWarning`](deprecationwarning/index.md) or [`FutureWarning`](futurewarning/index.md) for API removals, [`ResourceWarning`](resourcewarning/index.md) for unclosed resources, and [`RuntimeWarning`](runtimewarning/index.md) for suspicious numeric or interpreter behavior.

---

## Best practices

- Omit `category` only when `UserWarning` is truly correct; otherwise pass the specific class explicitly.
- Set `stacklevel=2` (or higher) when `warn()` is called from a wrapper so the line number matches the public API surface.
- Keep messages actionable: what happened, what to do instead.
- In tests, capture with `catch_warnings(record=True)` and `simplefilter("always")`.

---

## Example — default category and capture

```python
import warnings

def soft_validate(value):
    if value < 0:
        warnings.warn("negative value clamped to 0", stacklevel=2)
    return max(0, value)

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    assert soft_validate(-3) == 0
    assert len(log) == 1
    assert issubclass(log[0].category, UserWarning)
    assert "negative" in str(log[0].message)
```

---

## See also

- [Warning](../warning/index.md) — root base class
- [`warnings.warn()`](https://docs.python.org/3/library/warnings.html#warnings.warn)
