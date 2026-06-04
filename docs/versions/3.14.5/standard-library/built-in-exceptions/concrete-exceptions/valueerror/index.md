# [ValueError](https://docs.python.org/3/library/exceptions.html#ValueError)

Raised when an argument has the **correct type but an inappropriate value**, and no more specific exception applies. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#ValueError).

---

## ValueError vs related types

| Situation | Exception |
|-----------|-----------|
| Wrong type | [`TypeError`](../typeerror/index.md) |
| Wrong value (general) | **`ValueError`** |
| Bad sequence index | [`IndexError`](../indexerror/index.md) |
| Bad mapping key | [`KeyError`](../keyerror/index.md) |
| Unicode codec failure | [`UnicodeError`](../unicodeerror/index.md) subclass |

---

## When it is raised

| API | Example |
|-----|----------|
| `int('abc')` | Non-numeric string |
| `list.index(x)` | Value not in list |
| `struct.unpack` | Buffer wrong size |
| `datetime` constructors | Invalid date components |

---

## Demonstrating raise and catch

```python
# Goal: ValueError for bad value; TypeError for bad type
messages = {}
try:
    int('not-a-number')
except ValueError as exc:
    messages['int'] = type(exc).__name__
try:
    int([1, 2])
except TypeError as exc:
    messages['type'] = type(exc).__name__
assert messages == {'int': 'ValueError', 'type': 'TypeError'}
```

---

## Best practices

- Raise `ValueError` with messages that say **what was wrong** and **what was expected**.
- Subclass `ValueError` for domain-specific validation (`EmailFormatError`, etc.).
