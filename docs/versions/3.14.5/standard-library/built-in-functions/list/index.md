# [list()](https://docs.python.org/3/library/functions.html#func-list)

## Description

`list()` returns a new list. With an iterable argument, it copies elements into a mutable sequence. `list` is a built-in type supporting append, extend, sort, and more.

## What problem it solves

You need an ordered, changeable collection—accumulating results, reordering data, or materializing an iterator for reuse.

## Implementation options

### Empty list and literal equivalent

```python
empty = list()
assert empty == []
```

### Copy from an iterable

```python
assert list("abc") == ["a", "b", "c"]
assert list((1, 2)) == [1, 2]
assert sorted(list({3, 1, 2})) == [1, 2, 3]
```

### Build from a generator expression

```python
squares = list(x * x for x in range(5))
assert squares == [0, 1, 4, 9, 16]
```

## Best practices

- Use `[]` for empty lists in application code; `list()` is useful when shadowing hides the name `list`.
- `list(iterable)` copies—mutating the list does not affect the source iterable.
- For large streams, consider keeping a generator instead of materializing everything.
