# [zip()](https://docs.python.org/3/library/functions.html#zip)

## Description

`zip(*iterables, strict=False)` returns an iterator of tuples—the i-th tuple contains the i-th element from each input. By default iteration stops at the shortest input; with `strict=True`, mismatched lengths raise `ValueError`.

## What problem it solves

Loop over aligned columns (names and scores, keys and values from parallel lists) without manual index arithmetic, and transpose rows into columns.

## Implementation options

### Pair two sequences

```python
names = ["Ada", "Grace", "Alan"]
years = [1815, 1906, 1912]
pairs = list(zip(names, years))
assert pairs == [("Ada", 1815), ("Grace", 1906), ("Alan", 1912)]
```

### Enforce equal length with `strict=True`

```python
keys = ["a", "b", "c"]
vals = [1, 2, 3]
assert list(zip(keys, vals, strict=True)) == [("a", 1), ("b", 2), ("c", 3)]
```

### Unzip with `zip(*...)`

```python
pairs = [(1, "x"), (2, "y"), (3, "z")]
nums, letters = zip(*pairs)
assert list(nums) == [1, 2, 3]
assert list(letters) == ["x", "y", "z"]
```

## Best practices

- Use `strict=True` when unequal lengths indicate a bug, not intentional truncation.
- Default `zip` silently drops trailing items from longer iterables—verify lengths when that matters.
- For padding shorter iterables, use `itertools.zip_longest()` instead of manual loops.
