# [6.6. Unary arithmetic and bitwise operations](https://docs.python.org/3/reference/expressions.html#unary-arithmetic-and-bitwise-operations)

Unary `-`, `+`, and `~` share the same precedence level:

```ebnf
u_expr: power | "-" u_expr | "+" u_expr | "~" u_expr
```

| Operator | Effect | Special method |
|----------|--------|----------------|
| `-x` | Numeric negation | `__neg__` |
| `+x` | Numeric identity (unchanged) | `__pos__` |
| `~x` | Bitwise inversion: `-(x + 1)` for integers | `__invert__` |

```python
assert -5 == 0 - 5
assert +5 == 5
assert ~0 == -1
assert ~1 == -2

# ~n is equivalent to -(n + 1) for integers.
n = 7
assert ~n == -(n + 1)
```

Wrong operand types raise `TypeError`. Custom classes can override the special methods above.

Parent: [6. Expressions](../index.md)
