# [6.16. Evaluation order](https://docs.python.org/3/reference/expressions.html#evaluation-order)

Python evaluates expressions **from left to right**. For assignment, the **right-hand side** is evaluated before the left-hand side binds names.

The reference lists these patterns (suffixes show evaluation order relative to operators, not numeric values):

| Pattern | Order note |
|---------|------------|
| `expr1, expr2, expr3, expr4` | Left to right |
| `(expr1, expr2, expr3, expr4)` | Left to right inside |
| `{expr1: expr2, expr3: expr4}` | Keys and values left to right |
| `expr1 + expr2 * (expr3 - expr4)` | Operands before operators bind |
| `expr1(expr2, expr3, *expr4, **expr5)` | Callable, then arguments left to right |
| `expr3, expr4 = expr1, expr2` | RHS tuple first, then unpack to LHS |

```python
order = []


def mark(label):
    order.append(label)
    return label


# Comma-separated: left to right.
mark("a"), mark("b"), mark("c")
assert order == ["a", "b", "c"]

order.clear()
# Assignment: RHS fully evaluated before LHS names bind.
lhs_a, lhs_b = mark("rhs1"), mark("rhs2")
assert order == ["rhs1", "rhs2"]
assert lhs_a == "rhs1" and lhs_b == "rhs2"
```

Parent: [6. Expressions](../index.md)
