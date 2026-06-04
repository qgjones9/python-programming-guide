# [6.17. Operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)

When parentheses are omitted, Python binds operators from **highest** to **lowest** precedence. Operators in the same row group **left to right**, except `**` and conditional expressions (`if`–`else`), which group **right to left**.

| Precedence (high → low) | Operators | Description |
|-------------------------|-----------|-------------|
| 1 | `(...)`, `[...]`, `{...}` | Binding, displays |
| 2 | `x[i]`, `x[i:j]`, `x(...)`, `x.attr` | Subscription, call, attribute |
| 3 | `await x` | Await |
| 4 | `**` | Exponentiation |
| 5 | `+x`, `-x`, `~x` | Unary |
| 6 | `*`, `@`, `/`, `//`, `%` | Multiplicative |
| 7 | `+`, `-` | Additive |
| 8 | `<<`, `>>` | Shifts |
| 9 | `&` | Bitwise AND |
| 10 | `^` | Bitwise XOR |
| 11 | `\|` | Bitwise OR |
| 12 | `in`, `not in`, `is`, `is not`, comparisons | Includes chained `<` |
| 13 | `not` | Boolean NOT |
| 14 | `and` | Boolean AND |
| 15 | `or` | Boolean OR |
| 16 | `if`–`else` | Conditional (right-associative) |
| 17 | `lambda` | Lambda |
| 18 | `:=` | Walrus (lowest) |

```python
# Multiplication before addition without parentheses.
assert 1 + 2 * 3 == 7
assert (1 + 2) * 3 == 9

# Exponentiation groups right: 2**(3**2) == 512.
assert 2 ** 3 ** 2 == 512

# Conditional binds less tightly than or; and binds tighter than or.
assert True or False and False is True
assert (True or False) and False is False
```

Comparisons, membership, and identity tests share precedence and support **chaining** (see [Comparisons](../comparisons/index.md)).

Parent: [6. Expressions](../index.md)
