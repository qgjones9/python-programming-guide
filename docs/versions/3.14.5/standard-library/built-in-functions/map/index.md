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

### Option 4: Map a type method without a lambda

```python
words = ["  a ", "b", "  c  "]
trimmed = list(map(str.strip, words))
assert trimmed == ["a", "b", "c"]
```

## Best practices

- A list comprehension is often clearer for simple transforms; `map()` shines with an existing function like `int` or `str.strip`.

  ```python
  nums = ["1", "2", "3"]
  assert [int(n) for n in nums] == [1, 2, 3]
  assert list(map(int, nums)) == [1, 2, 3]
  ```

  ```python
  words = ["  a ", "b", "  c  "]
  assert list(map(str.strip, words)) == ["a", "b", "c"]
  ```

- `map()` returns an iterator—consume once or wrap with `list()`.

  ```python
  it = map(lambda x: x * 2, range(3))
  assert next(it) == 0
  assert list(it) == [2, 4]
  ```

- With parallel iterables of unequal length, iteration stops at the shortest; use `zip(..., strict=True)` when lengths must match.

  ```python
  pairs = list(map(lambda x, y: x + y, [1, 2, 3], [10, 20]))
  assert pairs == [11, 22]

  try:
      list(zip([1, 2, 3], [10, 20], strict=True))
  except ValueError:
      pass
  else:
      raise AssertionError("expected ValueError")
  ```
