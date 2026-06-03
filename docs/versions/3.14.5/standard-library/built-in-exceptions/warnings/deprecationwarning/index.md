# [DeprecationWarning](https://docs.python.org/3/library/exceptions.html#DeprecationWarning)

`DeprecationWarning` marks APIs that are deprecated for **other Python developers**—library authors, framework maintainers, and test suites—not for casual end users of a finished application. Policy details are in [PEP 387](https://peps.python.org/pep-0387/) and filter behavior in [PEP 565](https://peps.python.org/pep-0565/). Canonical docs: [exceptions.html#DeprecationWarning](https://docs.python.org/3/library/exceptions.html#DeprecationWarning).

---

## Purpose

Tell maintainers that an interface will be removed or changed in a future version. Distinct from [`FutureWarning`](futurewarning/index.md), which targets people *using* applications written in Python (data scientists, CLI users, etc.).

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Global default | **Ignored** (`ignore::DeprecationWarning`) |
| `__main__` module | **Shown** (`default::DeprecationWarning:__main__`) — scripts and REPL code in `__main__` see deprecations |
| Development mode | Shown (see [devmode](https://docs.python.org/3/library/devmode.html)) |
| Tests | Run with `-Wd` or `PYTHONWARNINGS=default` to surface ignored warnings |

This default prevents end users of packaged apps from seeing low-level library deprecations on every startup while still alerting authors working in `__main__` or CI.

---

## When to emit

- Removing or renaming public API in a library or the standard library.
- Behavior that still works but will change in a future major/minor release per your project's policy.
- Internals of frameworks consumed by other Python packages.

Use [`FutureWarning`](futurewarning/index.md) when the primary audience is someone running an application, not importing your module as a dependency.

---

## Best practices

- `warnings.warn("message with migration path", DeprecationWarning, stacklevel=2)` from wrapper functions.
- Python 3.13+: consider [`@warnings.deprecated`](https://docs.python.org/3/library/warnings.html#warnings.deprecated) for functions and classes.
- Include version or replacement in the message; silence is not consent—test with warnings enabled.
- Do not subclass `DeprecationWarning` for unrelated notices; filter rules target this exact category.

---

## Example — ignored by default, visible under `"always"`

```python
import warnings

def legacy_sort(items):
    warnings.warn(
        "legacy_sort() is deprecated; use sorted(items)",
        DeprecationWarning,
        stacklevel=2,
    )
    return sorted(items)

# Built-in filters ignore DeprecationWarning (record=True does not capture ignored warnings)
with warnings.catch_warnings(record=True) as log:
    legacy_sort([3, 1, 2])
    assert len(log) == 0

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    result = legacy_sort([3, 1, 2])
    assert result == [1, 2, 3]
    assert issubclass(log[-1].category, DeprecationWarning)
```

---

## See also

- [FutureWarning](../futurewarning/index.md) — end-user deprecations
- [`warnings` — Updating code for new dependency versions](https://docs.python.org/3/library/warnings.html#updating-code-for-new-versions-of-dependencies)
