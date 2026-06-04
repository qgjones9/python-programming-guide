# [OverflowError](https://docs.python.org/3/library/exceptions.html#OverflowError)

Subclass of [`ArithmeticError`](../../base-classes/arithmeticerror/index.md) raised when an arithmetic result is **too large to represent** in the target type. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#OverflowError).

---

## When it is raised

| Situation | Raises? |
|-----------|---------|
| Huge Python `int` arithmetic | **No** — arbitrary precision; may raise [`MemoryError`](../memoryerror/index.md) |
| `int` → fixed C type conversion | **Yes** when out of range |
| Most float ops in CPython | **Rarely checked** (platform-dependent) |

---

## Demonstrating raise and catch

```python
import sys

# Goal: int too large for C long raises OverflowError (when applicable)
caught = None
try:
    n = sys.maxsize * sys.maxsize * sys.maxsize
    n * n  # may succeed as big int
    raise OverflowError('simulated fixed-width overflow')
except OverflowError:
    caught = 'overflow'
assert caught == 'overflow'
assert issubclass(OverflowError, ArithmeticError)
```

---

## Related exceptions

| Type | When |
|------|------|
| [`ZeroDivisionError`](../zerodivisionerror/index.md) | Division by zero |
| [`FloatingPointError`](../floatingpointerror/index.md) | Reserved, rarely used |
| [`ArithmeticError`](../../base-classes/arithmeticerror/index.md) | Catch all three |

---

## Best practices

- Do not expect `OverflowError` from ordinary `int` math in Python 3.
- Validate ranges before converting to C APIs, `struct`, or `array` types.
