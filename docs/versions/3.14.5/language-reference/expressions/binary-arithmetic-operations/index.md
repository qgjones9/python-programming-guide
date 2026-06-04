# [6.7. Binary arithmetic operations](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)

Binary arithmetic splits into **multiplicative** (`m_expr`) and **additive** (`a_expr`) levels. Multiplication binds tighter than addition.

```ebnf
m_expr: u_expr | m_expr "*" u_expr | m_expr "@" u_expr |
        m_expr "//" u_expr | m_expr "/" u_expr | m_expr "%" u_expr
a_expr: m_expr | a_expr "+" m_expr | a_expr "-" m_expr
```

| Operator | Meaning | Notes |
|----------|---------|-------|
| `*` | Multiplication or sequence repetition | `3 * "ab"` → `"ababab"` |
| `@` | Matrix multiplication | No built-in types implement it |
| `/` | True division | `int / int` → `float` |
| `//` | Floor division | `int // int` → `int` |
| `%` | Remainder or string formatting | Sign matches divisor |
| `+` | Addition or sequence concatenation | |
| `-` | Subtraction | |

```python
assert 10 / 4 == 2.5
assert 10 // 4 == 2
assert 10 % 3 == 1
assert 3 * "xy" == "xyxyxy"
assert [1, 2] + [3] == [1, 2, 3]

# Floor division and modulo satisfy: x == (x//y)*y + (x%y)
x, y = 10, 3
assert x == (x // y) * y + (x % y)
```

Identity: `divmod(x, y) == (x // y, x % y)` for numeric types that support both. Floor division, modulo, and `divmod` are undefined for `complex`.

Parent: [6. Expressions](../index.md)
