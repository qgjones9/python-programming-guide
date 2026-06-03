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

## Best practices

- Use `frozenset` when you need hashable, immutable uniqueness—dict keys, set elements, or frozen dataclass fields.
- Convert with `frozenset(mutable_set)` before storing in structures that require hashable members.
- For large mutable collections, a plain `set` is fine until you need immutability or hashing.
