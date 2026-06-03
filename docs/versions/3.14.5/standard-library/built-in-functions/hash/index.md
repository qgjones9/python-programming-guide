# [hash()](https://docs.python.org/3/library/functions.html#hash)

## Description

Returns the integer hash value of an object, used for fast dict and set lookups; equal objects must have equal hashes.

## What problem it solves

Hash tables need a stable integer key derived from an object so membership and lookup stay O(1) on average.

## Implementation options

### Option 1: Build a set of hashable keys

```python
keys = [("a", 1), ("b", 2), ("a", 1)]
unique = {hash(k): k for k in keys}
assert len(unique) == 2
```

### Option 2: Hash strings for bucketing

```python
buckets = {}
for word in ["apple", "apricot", "banana"]:
    bucket = hash(word) % 3
    buckets.setdefault(bucket, []).append(word)
assert len(buckets) <= 3
```

## Best practices

- Only immutable, hashable types (str, int, tuple of hashables, frozenset) belong in sets and dict keys.
- User-defined classes are hashable by default unless they define `__eq__` without `__hash__`.
- Hash values may differ between Python runs (hash randomization); never persist `hash()` across processes.
