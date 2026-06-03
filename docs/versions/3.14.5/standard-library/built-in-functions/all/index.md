# [all()](https://docs.python.org/3/library/functions.html#all)

## Description

`all()` returns `True` if every element of the iterable is truthy. An empty iterable is vacuously true—`all([])` is `True`.

## What problem it solves

Validation and guard checks often require “every condition holds.” Instead of writing a loop that returns early on the first falsy value, `all()` expresses that intent in one readable expression, often combined with a generator.

## Implementation options

### Validating a sequence of flags

```python
permissions = [True, True, True]
assert all(permissions)

checks = [True, False, True]
assert not all(checks)
assert all([])  # empty: vacuous truth
```

### Short-circuit checks with a generator

```python
records = [{"active": True}, {"active": True}, {"active": False}]
assert not all(r["active"] for r in records)

scores = [88, 91, 79]
assert all(s >= 60 for s in scores)
```

### Combining with `any()` for range checks

```python
values = [3, 7, 12]
assert all(0 <= v <= 100 for v in values)
assert not all(v < 10 for v in values)
assert any(v > 10 for v in values)
```

## Best practices

- Use generator expressions inside `all()` to avoid building intermediate lists and to short-circuit on the first falsy item.

  ```python
  records = [{"ok": True}, {"ok": False}, {"ok": True}]
  # idiomatic: stops at the first falsy check
  assert not all(r["ok"] for r in records)

  # wasteful: builds a full list even after the first False
  assert not all([r["ok"] for r in records])
  ```

- Do not confuse “all true” with “non-empty”: `all([])` is `True`; combine with length checks when you need at least one element.

  ```python
  flags = []
  assert all(flags)  # vacuously True — not “someone checked”

  def all_nonempty(items):
      return bool(items) and all(items)

  assert not all_nonempty(flags)
  assert all_nonempty([True, True])
  ```

- Remember truthiness, not identity: `0`, `""`, and `None` count as false.

  ```python
  values = [1, 2, 0, 4]
  assert not all(values)  # 0 is falsy

  # explicit test when zero is valid data
  assert all(v >= 0 for v in values)
  ```
