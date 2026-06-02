# [set()](https://docs.python.org/3/library/functions.html#func-set)

## Description

`set()` returns a new set object, optionally populated from an iterable. Sets store unique hashable items and support fast membership tests and algebraic operations (union, intersection, difference).

## What problem it solves

You need to remove duplicates, test membership in O(1) average time, or compute relationships between collections (shared items, unique items, etc.).

## Implementation options

### Deduplicate an iterable

```python
raw = ["a", "b", "a", "c", "b"]
assert sorted(set(raw)) == ["a", "b", "c"]
```

### Set algebra for tag overlap

```python
tags_a = {"python", "docs", "tutorial"}
tags_b = {"python", "api", "docs"}
assert tags_a & tags_b == {"python", "docs"}
assert tags_a - tags_b == {"tutorial"}
assert tags_a | tags_b == {"python", "docs", "tutorial", "api"}
```

### Build a set with a comprehension

```python
words = ["apple", "banana", "apricot", "blueberry"]
starts_with_a = {word for word in words if word.startswith("a")}
assert starts_with_a == {"apple", "apricot"}
```

## Best practices

- Use `set` for membership checks on large collections instead of scanning a list.
- Choose `frozenset` when you need an immutable, hashable set (e.g. dict keys).
- Remember sets are unordered—do not rely on iteration order for logic.
