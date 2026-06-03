# [reversed()](https://docs.python.org/3/library/functions.html#reversed)

## Description

`reversed()` returns a reverse iterator. The argument must support `__reversed__()` or the sequence protocol (`__len__` and `__getitem__` with integer indices starting at 0).

## What problem it solves

You want to walk a sequence from last to first without copying it into a new list or writing manual index arithmetic.

## Implementation options

### Reverse a list via iterator

```python
items = ["first", "second", "third"]
assert list(reversed(items)) == ["third", "second", "first"]
assert items == ["first", "second", "third"]  # original unchanged
```

### Reverse a string's characters

```python
word = "Python"
assert "".join(reversed(word)) == "nohtyP"
```

### Custom type with `__reversed__`

```python
class Stack:
    def __init__(self, values):
        self._values = list(values)

    def __reversed__(self):
        return iter(self._values[::-1])

assert list(reversed(Stack([1, 2, 3]))) == [3, 2, 1]
```

## Best practices

- `reversed()` returns an iterator—consume it once or wrap with `list()` if you need reuse.
- Prefer `reversed(seq)` over `seq[::-1]` when you do not need a materialized copy.
- Implement `__reversed__` on sequence types when reverse iteration is a common operation.
