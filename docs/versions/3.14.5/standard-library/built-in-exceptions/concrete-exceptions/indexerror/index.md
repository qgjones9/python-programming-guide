# [IndexError](https://docs.python.org/3/library/exceptions.html#IndexError)

Raised when a **sequence subscript is out of range**. Subclass of [`LookupError`](../base-classes/lookuperror/index.md). See [docs.python.org](https://docs.python.org/3/library/exceptions.html#IndexError).

---

## When it is raised

| Operation | Out-of-range behavior |
|-----------|----------------------|
| `seq[i]` | **`IndexError`** when `i` is invalid |
| `seq[i:j]` slice | **Silent** clamping—no exception |
| Non-integer index | [`TypeError`](typeerror/index.md) |

---

## Demonstrating raise and catch

```python
# Goal: IndexError on bad index; slice does not raise
items = [10, 20, 30]
caught = None
try:
    items[99]
except IndexError:
    caught = 'index'
assert caught == 'index'
assert items[1:100] == [20, 30]
```

---

## Related exceptions

| Type | When |
|------|------|
| [`KeyError`](keyerror/index.md) | Mapping key missing |
| [`LookupError`](../base-classes/lookuperror/index.md) | Catch either |
| [`ValueError`](valueerror/index.md) | Wrong value, not bad index |

---

## Best practices

- Prefer checking bounds or using `.get`-style APIs when failure is expected.
- Use `except LookupError` when one handler covers both sequences and mappings.
- Negative indices that are in range are valid; only out-of-range indices raise.
