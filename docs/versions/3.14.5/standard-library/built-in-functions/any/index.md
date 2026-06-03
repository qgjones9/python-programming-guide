# [any()](https://docs.python.org/3/library/functions.html#any)

## Description

`any()` returns `True` if at least one element of the iterable is truthy. For an empty iterable it returns `False`.

## What problem it solves

Many policies are satisfied when *any* condition holds: error detection, optional feature flags, search-for-match problems. `any()` replaces hand-written loops that break on the first true value.

## Implementation options

### Detecting a match in a collection

```python
errors = ["", "", "disk full"]
assert any(errors)

flags = [False, False, False]
assert not any(flags)
assert not any([])  # empty iterable
```

### Existential checks with generators

```python
users = [{"role": "guest"}, {"role": "admin"}]
assert any(u["role"] == "admin" for u in users)

values = [0, 0, 0]
assert not any(v > 0 for v in values)
```

## Best practices

- Pair `any()` with generator expressions for lazy, short-circuit evaluation.
- `any()` and `all()` are often clearer than `or`/`and` chains over many dynamic conditions.
- Distinguish “none true” (`not any(...)`) from “all false”—for empty iterables, `any([])` is `False`.
