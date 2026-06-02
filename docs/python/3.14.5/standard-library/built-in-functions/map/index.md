# [map()](https://docs.python.org/3/library/functions.html#map)

## Description

`map(function, iterable, /, *iterables, strict=False)` returns an iterator that applies `function` to each item. With multiple iterables, `function` receives parallel items and iteration stops at the shortest unless `strict=True`.

## What problem it solves

Transform every element of a sequence—parse strings to ints, normalize records, combine parallel columns—without an explicit index loop.

## Implementation options

### Map a function over one iterable

```python
nums = ["1", "2", "3"]
assert list(map(int, nums)) == [1, 2, 3]
```

### Map with multiple iterables

```python
widths = [2, 3, 4]
heights = [5, 6, 7]
areas = list(map(lambda w, h: w * h, widths, heights))
assert areas == [10, 18, 28]
```

### Parallel iterables stop at the shortest

```python
a = list(map(lambda x, y: x + y, [1, 2, 3], [10, 20]))
assert a == [11, 22]
```

## Best practices

- A list comprehension is often clearer for simple transforms; `map` shines with an existing function like `int`.
- `map` returns an iterator—consume once or wrap with `list()`.
- In Python 3.14+, `strict=True` raises when parallel iterables differ in length.
