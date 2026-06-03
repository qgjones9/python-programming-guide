# [range()](https://docs.python.org/3/library/functions.html#func-range)

## Description

`range` is an immutable sequence type (not a function) that represents an arithmetic progression of integers. It stores only start, stop, and step, so it uses constant memory even for huge spans.

## What problem it solves

You need to repeat an action a known number of times, generate index values, or slice another sequence without allocating a full list of every integer in memory.

## Implementation options

### Stop-only form (0 through stop − 1)

```python
indices = list(range(5))
assert indices == [0, 1, 2, 3, 4]
```

### Start, stop, and step (including reverse iteration)

```python
evens = list(range(2, 11, 2))
assert evens == [2, 4, 6, 8, 10]

backwards = list(range(10, 0, -2))
assert backwards == [10, 8, 6, 4, 2]
```

### Pair with `enumerate` for index/value loops

```python
names = ["alpha", "beta", "gamma"]
pairs = [(i, name) for i, name in enumerate(names)]
assert pairs == [(0, "alpha"), (1, "beta"), (2, "gamma")]
```

## Best practices

- Prefer `range(n)` over `list(range(n))` when you only need iteration or indexing.
- Remember the stop value is exclusive: `range(3)` yields `0`, `1`, `2`.
- Use a negative `step` to count down; `start` must be greater than `stop` in that case.
- For very large ranges, rely on lazy iteration—do not materialize the whole sequence unless required.
