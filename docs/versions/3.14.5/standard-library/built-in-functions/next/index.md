# [next()](https://docs.python.org/3/library/functions.html#next)

## Description

`next(iterator, default=None)` calls the iterator's `__next__()` method. Without `default`, exhausted iterators raise `StopIteration`; with `default`, that value is returned instead.

## What problem it solves

Manual iterator control—pull one item at a time, peek-adjacent patterns, or safe iteration when exhaustion is expected.

## Implementation options

### Advance an iterator step by step

```python
it = iter([1, 2, 3])
assert next(it) == 1
assert next(it) == 2
assert next(it) == 3
```

### Default when iterator is empty

```python
it = iter([])
assert next(it, None) is None
assert next(it, "done") == "done"
```

### Manual loop using next

```python
it = iter(["a", "b"])
items = []
while True:
    item = next(it, None)
    if item is None:
        break
    items.append(item)
assert items == ["a", "b"]
```

## Best practices

- Prefer `for` loops for full iteration; use `next()` for streaming or parser-style logic.

  ```python
  items = ["a", "b", "c"]
  collected = []
  for item in items:
      collected.append(item)
  assert collected == ["a", "b", "c"]
  ```

  ```python
  # Manual next() is for parser-style pull-one-at-a-time logic:
  it = iter("abc")
  assert next(it) == "a"
  ```

- Always provide `default` when exhaustion is normal, not exceptional.

  ```python
  it = iter([])
  assert next(it, None) is None  # exhaustion is expected
  ```

  ```python
  it = iter([])
  # This will raise StopIteration when empty:
  # next(it)
  ```

- Do not catch `StopIteration` outside generator protocol code—it has special meaning inside generators.

  ```python
  def read_one(it):
      return next(it, None)  # prefer default over bare except

  assert read_one(iter([1])) == 1
  assert read_one(iter([])) is None
  ```

  ```python
  # Incorrect in application code—use default= instead:
  # try:
  #     next(it)
  # except StopIteration:
  #     ...
  ```
