# [len()](https://docs.python.org/3/library/functions.html#len)

## Description

`len(object)` returns the length—the number of items—of a sequence or collection. Custom types may implement `__len__()` to participate.

## What problem it solves

Bounds checks, progress reporting, validating input size, and choosing algorithms that depend on how many elements you have.

## Implementation options

### Common built-in types

```python
assert len([1, 2, 3]) == 3
assert len("hello") == 5
assert len({"a": 1, "b": 2}) == 2
assert len({1, 2, 3}) == 3
```

### Custom container with `__len__`

```python
class Queue:
    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

assert len(Queue(["x", "y"])) == 2
```

### Empty versus non-empty checks

```python
pending = []
assert len(pending) == 0
if not pending:
    pending.append("task")
assert len(pending) == 1
```

## Best practices

- For emptiness tests, `if not seq:` is idiomatic; use `len()` when you need the actual count.

  ```python
  pending = []
  if not pending:
      pending.append("task")
  assert pending == ["task"]
  assert len(pending) == 1
  ```

- `len()` is O(1) for list, tuple, str, dict, and set in CPython.

  ```python
  data = {"a": 1, "b": 2, "c": 3}
  assert len(data) == 3
  assert len("hello") == 5
  ```

- Very large theoretical ranges may raise `OverflowError`—rare in everyday code.

  ```python
  huge = range(10**100)
  try:
      len(huge)
  except OverflowError:
      pass
  else:
      raise AssertionError("expected OverflowError")
  ```
