# [dict()](https://docs.python.org/3/library/functions.html#func-dict)

## Description

`dict()` creates a new dictionary. Call it with no arguments, keyword arguments, an existing mapping, an iterable of key-value pairs, or a combination of mapping plus keywords.

## What problem it solves

Mappings are the default associative structure in Python—configuration, JSON-like records, indexes, and caches. `dict()` normalizes many input shapes into a mutable hash map with fast lookup.

## Implementation options

### Keywords, pairs, and merging

```python
empty = dict()
assert empty == {}

user = dict(name="Ada", role="admin")
assert user["name"] == "Ada"

pairs = [("a", 1), ("b", 2)]
from_pairs = dict(pairs)
assert from_pairs == {"a": 1, "b": 2}

base = {"a": 1, "b": 2}
extended = dict(base, c=3)
assert extended == {"a": 1, "b": 2, "c": 3}
```

### Copying and updating from another mapping

```python
original = {"x": 10, "y": 20}
copy = dict(original)
copy["z"] = 30
assert original == {"x": 10, "y": 20}
assert copy == {"x": 10, "y": 20, "z": 30}
```

## Best practices

- Prefer `{**base, **extra}` or `base | extra` (3.9+) for merges; use `dict(mapping, **kw)` when converting unknown mappings.
- Dict comprehensions `{k: v for ...}` are often clearer than `dict()` with a generator of pairs.
- Keys must be hashable; values can be anything—watch mutable defaults in class attributes.
