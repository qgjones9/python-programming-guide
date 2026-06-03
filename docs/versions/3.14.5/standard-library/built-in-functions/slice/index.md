# [slice()](https://docs.python.org/3/library/functions.html#slice)

## Description

`slice(stop)` or `slice(start, stop, step=None)` returns a slice object describing a range of indices—the same object produced by `seq[start:stop:step]` syntax. Attributes `start`, `stop`, and `step` are read-only.

## What problem it solves

You want to reuse the same slicing parameters across multiple sequences, pass slices as values, or build indexing logic programmatically.

## Implementation options

### Reuse one slice on different sequences

```python
every_other = slice(None, None, 2)
assert [0, 1, 2, 3, 4, 5][every_other] == [0, 2, 4]
assert "abcdef"[every_other] == "ace"
```

### Explicit start and stop

```python
window = slice(1, 5)
data = [10, 20, 30, 40, 50, 60]
assert data[window] == [20, 30, 40, 50]
assert window.start == 1 and window.stop == 5
```

### Store slices in a lookup table

```python
regions = {
    "head": slice(0, 3),
    "tail": slice(-3, None),
}
seq = list(range(10))
assert seq[regions["head"]] == [0, 1, 2]
assert seq[regions["tail"]] == [7, 8, 9]
```

## Best practices

- Slice objects are hashable (since 3.12) when `start`, `stop`, and `step` are hashable—useful as dict keys.

  ```python
  head = slice(0, 3)
  tail = slice(-3, None)
  regions = {head: "head", tail: "tail"}
  seq = list(range(10))
  assert seq[head] == [0, 1, 2]
  assert seq[tail] == [7, 8, 9]
  assert regions[head] == "head"
  ```

  ```python
  # Before 3.12, slice objects were not hashable—check your target Python version.
  ```

- Negative indices in slice objects behave like syntactic slicing when applied to sequences.

  ```python
  last_two = slice(-2, None)
  assert [10, 20, 30, 40][last_two] == [30, 40]
  ```

  ```python
  # Incorrect—negative stop is not "two from the end" like negative start:
  assert list(range(5))[slice(0, -2)] == [0, 1, 2]  # stops before index -2
  ```

- For lazy iteration over slices, consider `itertools.islice()` instead of materializing indices.

  ```python
  from itertools import islice

  data = range(10**6)
  first_five = list(islice(data, 5))
  assert first_five == [0, 1, 2, 3, 4]
  ```

  ```python
  # Materializes a huge sub-list when you only need a few items:
  # chunk = list(range(10**6))[100:200]
  ```
