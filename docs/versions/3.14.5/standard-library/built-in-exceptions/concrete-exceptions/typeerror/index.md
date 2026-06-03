# [TypeError](https://docs.python.org/3/library/exceptions.html#TypeError)

Raised when an operation or function is applied to an object of **inappropriate type**. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#TypeError).

---

## TypeError vs ValueError

| Mistake | Exception |
|---------|-----------|
| Wrong type (list where int expected) | **`TypeError`** |
| Right type, bad value (negative where positive required) | **`ValueError`** |
| Operation not supported at all | **`TypeError`** or undefined method |
| Supported but not implemented yet | [`NotImplementedError`](notimplementederror/index.md) |

---

## When it is raised

| Cause | Example |
|-------|----------|
| Unsupported operand types | `'a' + 1` |
| Wrong number of arguments | `range()` called with strings |
| Unhashable key | `d[[1]] = 2` |
| Object does not support attribute protocol | Some C types |

---

## Demonstrating raise and catch

```python
# Goal: wrong types raise TypeError; wrong values raise ValueError
caught_type = None
caught_value = None
try:
    'a' + 1
except TypeError:
    caught_type = 'type'
try:
    int('not a number')
except ValueError:
    caught_value = 'value'
assert caught_type == 'type'
assert caught_value == 'value'
```

---

## Best practices

- Raise `TypeError` from APIs when the **type** is wrong; document expected types in docstrings.
- Related: [`AttributeError`](attributeerror/index.md), [`ValueError`](valueerror/index.md).
