# [ZeroDivisionError](https://docs.python.org/3/library/exceptions.html#ZeroDivisionError)

Subclass of [`ArithmeticError`](../base-classes/arithmeticerror/index.md) raised when the **second operand of division or modulo is zero**. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#ZeroDivisionError).

---

## When it is raised

| Operation | Zero divisor |
|-----------|--------------|
| `/`, `//`, `%` | **`ZeroDivisionError`** |
| `divmod(a, 0)` | **`ZeroDivisionError`** |
| `1.0 / 0.0`, `1.0 % 0.0` | **`ZeroDivisionError`** (CPython; use `math.inf` if you need IEEE-style infinity) |

---

## Demonstrating raise and catch

```python
# Goal: integer division by zero raises ZeroDivisionError
caught = None
try:
    10 // 0
except ZeroDivisionError as exc:
    caught = type(exc).__name__
assert caught == 'ZeroDivisionError'
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| Pre-check divisor | User-supplied denominator before `/` or `%` |
| `except ZeroDivisionError` | Translate to domain error or return sentinel |
| `except ArithmeticError` | Single handler for overflow and division-by-zero |

Related: [`OverflowError`](overflowerror/index.md), [`ArithmeticError`](../base-classes/arithmeticerror/index.md).

---

## Best practices

- Validate divisors from user input before dividing.
- Catch [`ArithmeticError`](../base-classes/arithmeticerror/index.md) only when overflow and division-by-zero need the same handling.
