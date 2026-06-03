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

### Short-circuiting (stops at first truthy result)

```python
seen = []

def positive(x):
    seen.append(x)
    return x > 0

assert any(positive(v) for v in [0, 0, 3, 99])
assert seen == [0, 0, 3]  # never evaluates positive(99)
```

## Best practices

- Pair `any()` with generator expressions for lazy, short-circuit evaluation.

  ```python
  seen = []

  def is_admin(user):
      seen.append(user["name"])
      return user["role"] == "admin"

  users = [{"name": "a", "role": "guest"}, {"name": "b", "role": "admin"}, {"name": "c", "role": "admin"}]
  assert any(is_admin(u) for u in users)
  assert seen == ["a", "b"]  # never checks user "c"
  ```

- `any()` is often clearer than a long `or` chain when conditions come from a collection.

  ```python
  errors = ["", "disk full", ""]
  assert any(errors)

  # awkward when the iterable is dynamic:
  # assert errors[0] or errors[1] or errors[2]
  ```

- Distinguish “none true” from “all false”—for empty iterables, `any([])` is `False`.

  ```python
  flags = []
  assert not any(flags)
  assert all(not f for f in flags)  # vacuously True — different meaning
  ```
