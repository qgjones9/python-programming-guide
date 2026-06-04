# [Warning](https://docs.python.org/3/library/exceptions.html#Warning)

`Warning` is the root of all built-in warning categories and the required base for user-defined warning classes. It inherits from [`Exception`](../../base-classes/exception/index.md), so warnings can be turned into errors by the filter. Canonical prose is on [docs.python.org](https://docs.python.org/3/library/exceptions.html#Warning); this page covers hierarchy, defaults, and custom categories.

---

## Purpose

Warning categories are labels for the [`warnings`](https://docs.python.org/3/library/warnings.html) machinery. They do not mean “something crashed”—they classify *what kind* of recoverable condition was detected so filters can treat developer deprecations differently from end-user notices.

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| `warnings.warn()` default | Uses [`UserWarning`](../userwarning/index.md), not bare `Warning` |
| Matching filters | Specs use `category=Warning` to match **any** warning subclass |
| `"error"` action | Raises `category(message)` because `Warning` is an `Exception` subclass |

---

## When to emit

Subclass `Warning` (almost always via `UserWarning` or a specific built-in) when you define a reusable category for your package. Emit with [`warnings.warn()`](https://docs.python.org/3/library/warnings.html#warnings.warn) and pass your class as `category`. Do not raise `Warning` directly for control flow—use the warnings API so filters apply.

---

## Best practices

- Subclass `Warning` (or `UserWarning`) for custom categories; never use a bare `Exception` as a warning category.
- Pass an explicit `category=` to `warnings.warn()`; relying on the `UserWarning` default is fine for ad hoc messages.
- Use `stacklevel=2+` in helper functions so the reported line is the caller’s code (see [`warnings.warn` docs](https://docs.python.org/3/library/warnings.html#warnings.warn)).
- Prefer a specific built-in category ([`DeprecationWarning`](../deprecationwarning/index.md), [`FutureWarning`](../futurewarning/index.md), etc.) when one fits; reserve custom subclasses for repeated, filterable families of messages.

---

## Custom category and hierarchy

```python
import warnings

class MyLibWarning(Warning):
    pass

assert issubclass(MyLibWarning, Warning)
assert issubclass(Warning, Exception)
assert issubclass(UserWarning, Warning)

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    warnings.warn("check", MyLibWarning)
    assert log[-1].category is MyLibWarning
```

---

## See also

- [Warnings overview](../index.md)
- [`warnings` module — Warning Categories](https://docs.python.org/3/library/warnings.html#warning-categories)
