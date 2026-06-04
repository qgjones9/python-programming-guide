# [6.9. Binary bitwise operations](https://docs.python.org/3/reference/expressions.html#binary-bitwise-operations)

Bitwise operators each have a distinct precedence level (tighter than comparisons):

```ebnf
and_expr: shift_expr | and_expr "&" shift_expr
xor_expr: and_expr | xor_expr "^" and_expr
or_expr:  xor_expr | or_expr "|" xor_expr
```

From tightest to loosest: `&` (AND), `^` (XOR), `|` (OR). Operands must be integers or objects implementing the corresponding special methods.

| Operator | Name | Example |
|----------|------|---------|
| `&` | Bitwise AND | `0b1100 & 0b1010` → `0b1000` |
| `^` | Bitwise XOR | `0b1100 ^ 0b1010` → `0b110` |
| `\|` | Bitwise OR | `0b1100 \| 0b1010` → `0b1110` |

```python
a, b = 0b1100, 0b1010
assert (a & b) == 0b1000
assert (a ^ b) == 0b0110
assert (a | b) == 0b1110

# AND clears bits; OR sets them; XOR toggles where exactly one side has a bit.
mask = 0b1111
assert (a & mask) == a
```

Parent: [6. Expressions](../index.md)
