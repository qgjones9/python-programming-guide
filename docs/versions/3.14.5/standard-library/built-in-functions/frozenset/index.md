# [frozenset()](https://docs.python.org/3/library/functions.html#func-frozenset)

## Description

Returns an immutable set built from an optional iterable; supports set operations but cannot be modified after creation.

## What problem it solves

Sets are useful for membership tests and deduplication, but mutable sets cannot be dict keys or elements of other sets.

## Implementation options

### Option 1: Use as a dictionary key for cached lookups

```python
cache = {}
key = frozenset(["read", "write"])
cache[key] = "editor-role"
assert cache[frozenset(["write", "read"])] == "editor-role"
```

### Option 2: Store a fixed tag collection on a dataclass

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Record:
    tags: frozenset

r = Record(frozenset(["urgent", "billing"]))
assert "urgent" in r.tags
assert len(r.tags) == 2
```

### Option 3: Set algebra without copying members

```python
a = frozenset({1, 2, 3})
b = frozenset({3, 4})
assert a | b == frozenset({1, 2, 3, 4})
assert a & b == frozenset({3})
assert a - b == frozenset({1, 2})
```

### Option 4: Nested in another frozenset

```python
outer = frozenset([frozenset([1, 2]), frozenset([2, 3])])
assert len(outer) == 2
assert frozenset([2, 1]) in outer
```

## Best practices

- Use `frozenset` when you need hashable, immutable uniqueness—dict keys, set elements, or frozen dataclass fields.

  ```python
  cache = {}
  key = frozenset(["read", "write"])
  cache[key] = "editor-role"
  assert cache[frozenset(["write", "read"])] == "editor-role"
  ```

  ```python
  tags = {"urgent", "billing"}
  try:
      {tags: "value"}  # mutable set is unhashable
  except TypeError:
      pass
  else:
      raise AssertionError("expected TypeError")
  ```

- Convert with `frozenset(mutable_set)` before storing in structures that require hashable members.

  ```python
  permissions = {"read", "write"}
  frozen = frozenset(permissions)
  permissions.add("delete")  # original set still mutable
  assert frozen == frozenset({"read", "write"})
  assert "delete" in permissions
  ```

- For everyday deduplication, a plain `set` is fine until you need immutability or hashing.

  ```python
  seen = set()
  for word in ["a", "b", "a", "c"]:
      seen.add(word)
  assert seen == {"a", "b", "c"}
  ```
