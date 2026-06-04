# [6.8. Shifting operations](https://docs.python.org/3/reference/expressions.html#shifting-operations)

Bit shifts have lower priority than additive arithmetic:

```ebnf
shift_expr: a_expr | shift_expr ("<<" | ">>") a_expr
```

| Operator | Meaning | Equivalent |
|----------|---------|------------|
| `<< n` | Left shift by `n` bits | multiply by `2**n` |
| `>> n` | Right shift by `n` bits | floor division by `2**n` |

Both operands must be integers (or types overriding `__lshift__` / `__rshift__`).

```python
assert 1 << 3 == 8
assert 8 >> 2 == 2
assert 1 << 3 == 1 * pow(2, 3)
assert 8 >> 2 == 8 // pow(2, 2)

# Large shifts follow integer semantics; watch overflow on left shift.
assert (-1 >> 1) == -1  # arithmetic right shift toward negative infinity
```

Parent: [6. Expressions](../index.md)
