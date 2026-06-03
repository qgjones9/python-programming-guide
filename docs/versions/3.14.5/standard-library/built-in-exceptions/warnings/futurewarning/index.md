# [FutureWarning](https://docs.python.org/3/library/exceptions.html#FutureWarning)

`FutureWarning` marks deprecated behavior aimed at **end users of applications** written in Python—people who run notebooks, scripts, or GUIs but may not maintain the library code. Since Python 3.7, it is distinguished from [`DeprecationWarning`](deprecationwarning/index.md) by **audience and default filters**, not by whether behavior is removed entirely. Canonical docs: [exceptions.html#FutureWarning](https://docs.python.org/3/library/exceptions.html#FutureWarning).

---

## Purpose

Notify application users that a default will change (pandas display options, CLI flags, file format handling) while keeping `DeprecationWarning` silent for library-to-library churn.

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Default filter | `"default"` — shown on first occurrence per location |
| Not in ignore list | Unlike `DeprecationWarning`, visible in typical app runs |
| Contrast | `DeprecationWarning` is ignored globally except `__main__` and dev mode |

---

## When to emit

- Application-facing APIs where the caller is not expected to be a package maintainer.
- Behavioral changes in high-level tools (data analysis, plotting, game mods).
- User-visible renames where the old name still works for one release.

Use `DeprecationWarning` when the consumer is another Python module that pins versions and runs tests with `-Wd`.

---

## Best practices

- State the new behavior, the release when the old path goes away, and how to opt in early.
- `warnings.warn(..., FutureWarning, stacklevel=2)` from public entry points.
- Document the category in user-facing release notes—not only in developer changelogs.

---

## Example — end-user API change

```python
import warnings

def read_table(path, *, engine="auto"):
    if engine == "legacy":
        warnings.warn(
            "engine='legacy' will be removed in 2.0; use engine='auto'",
            FutureWarning,
            stacklevel=2,
        )
    return f"loaded:{path}:{engine}"

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    read_table("data.csv", engine="legacy")
    assert issubclass(log[-1].category, FutureWarning)
    assert "2.0" in str(log[-1].message)
```

---

## See also

- [DeprecationWarning](../deprecationwarning/index.md)
- [Warning Categories — 3.7 change note](https://docs.python.org/3/library/warnings.html#warning-categories)
