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

### Option 3: Equal objects share hash values

```python
a = (1, 2, 3)
b = (1, 2, 3)
assert a == b
assert hash(a) == hash(b)
```

### Option 4: Unhashable mutable types

```python
lst = [1, 2]
try:
    hash(lst)
except TypeError as exc:
    assert "unhashable" in str(exc)
```

## Best practices

- Only immutable, hashable types belong in sets and dict keys; mutable containers raise `TypeError`.

  ```python
  valid_keys = {("a", 1), frozenset([1, 2])}
  assert ("a", 1) in valid_keys

  try:
      {[1, 2]: "value"}
  except TypeError:
      pass
  else:
      raise AssertionError("expected TypeError")
  ```

- Defining `__eq__` without `__hash__` makes instances unhashable—restore `__hash__` or set `__hash__ = None` intentionally.

  ```python
  class Point:
      __slots__ = ("x", "y")

      def __init__(self, x, y):
          self.x, self.y = x, y

      def __eq__(self, other):
          return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

  p = Point(1, 2)
  try:
      hash(p)
  except TypeError:
      pass
  else:
      raise AssertionError("expected TypeError")
  ```

- Hash values may differ between Python runs (hash randomization); never persist `hash()` across processes.

  ```python
  value = "session-key"
  bucket = hash(value) % 8
  assert 0 <= bucket < 8
  # Do not store `hash(value)` in a database for long-lived lookup keys.
  ```
