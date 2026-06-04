# [warnings — Warning control](https://docs.python.org/3/library/warnings.html)

The [`warnings`](https://docs.python.org/3/library/warnings.html) module implements Python's **warning subsystem**: emit `Warning` subclasses, apply filters (`default`, `ignore`, `error`, …), and integrate with `-W` CLI options via `sys.warnoptions`. Unlike exceptions, warnings default to printing once and continuing. Reference: [docs.python.org](https://docs.python.org/3/library/warnings.html).

Related exception docs: [Built-in Exceptions — warnings](../built-in-exceptions/warnings/index.md).

---

## Core API

| Function / class | Role |
|------------------|------|
| `warn(message, category=UserWarning, …)` | Emit a warning (respects filters + stacklevel) |
| `warn_explicit(...)` | Fully specified warning (for re-warnings) |
| `simplefilter(action, category=Warning, …)` | Easy filter install |
| `filterwarnings(...)` | Regex-based filter rules |
| `catch_warnings(*, record=False, …)` | Context manager for temporary filter changes |
| `showwarning` / `formatwarning` | Display hook customization |

---

## Filters — [Describing Warning Filters](https://docs.python.org/3/library/warnings.html#describing-warning-filters)

Filter tuples match `(action, message, category, module, lineno)`. **First match wins.** Default filter (since 3.7) ignores some deprecation categories in `__main__` and shows `DeprecationWarning`/`PendingDeprecationWarning` once elsewhere unless `-W` overrides.

| Action | Effect |
|--------|--------|
| `default` | First occurrence per location |
| `ignore` | Suppress |
| `error` | Turn into exception |
| `always` | Show every time |
| `module` | Once per module |
| `once` | Once globally |

```python
# Goal: capture and assert on a emitted warning
import warnings

def risky():
    warnings.warn("legacy API", DeprecationWarning, stacklevel=2)

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    risky()
    assert len(log) == 1
    assert issubclass(log[0].category, DeprecationWarning)
    assert "legacy" in str(log[0].message)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Set **`stacklevel=2+`** in library wrappers | Points blame at caller line |
| Use **`catch_warnings` in tests** | Deterministic warning assertions |
| Promote **`DeprecationWarning` to error in CI** | `-W error::DeprecationWarning` catches regressions early |
| Prefer **`warnings` over print** for soft deprecations | Respects user filters |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Duplicate filter rules | Unpredictable first-match behavior | `resetwarnings()` in tests |
| Catching `Exception` around `warn(..., category=X)` | Misses promoted warnings | Catch specific warning types when using `error` action |
| Relying on repeated suppression without reading criteria | Surprised when warning reappears | See [Repeated Warning Suppression Criteria](https://docs.python.org/3/library/warnings.html#repeated-warning-suppression-criteria) |

---

## See also

- [`BytesWarning`](../built-in-exceptions/warnings/byteswarning/index.md) — binary/text misuse
- [`sys`](../sys-system-specific-parameters-and-functions/index.md) — `warnoptions` from `-W`
