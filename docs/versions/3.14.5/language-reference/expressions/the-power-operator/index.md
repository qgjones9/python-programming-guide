# [6.5. The power operator](https://docs.python.org/3/reference/expressions.html#the-power-operator)

The `**` operator raises its left operand to the power of its right operand. Grammar:

```ebnf
power: (await_expr | primary) ["**" u_expr]
```

**Binding:** `**` binds tighter than unary operators on its **left**, but looser than unary operators on its **right**. In a chain, evaluation proceeds **right to left** for `**` and unary `-`:

| Expression | Result | Why |
|------------|--------|-----|
| `2 ** 3 ** 2` | `512` | `3**2` first → `2**9` |
| `-1 ** 2` | `-1` | parsed as `-(1**2)` |
| `10 ** -2` | `0.01` | negative exponent → `float` |

```python
assert 2 ** 3 ** 2 == 512
assert -1 ** 2 == -1
assert (-1) ** 2 == 1
assert 10 ** 2 == 100
assert 10 ** -2 == 0.01
```

For `int` operands the result is usually `int`, except when the exponent is negative (then operands convert to `float`). `0.0 ** negative` raises `ZeroDivisionError`. Negative base to a fractional exponent yields `complex`.

Parent: [6. Expressions](../index.md)
