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
- Always provide `default` when exhaustion is normal, not exceptional.
- Do not catch `StopIteration` outside generator protocol code—it has special meaning inside generators.
