# [6.10. Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)

All comparison operators share one precedence level (below arithmetic and bitwise ops). Unlike C, chained forms like `a < b < c` mean `a < b and b < c`, evaluating each middle operand **once**.

```ebnf
comparison:    or_expr (comp_operator or_expr)*
comp_operator: "<" | ">" | "==" | ">=" | "<=" | "!="
               | "is" ["not"] | ["not"] "in"
```

Comparisons yield `bool` values (custom rich comparison methods may return other types; `bool()` is applied in boolean contexts).

### [6.10.1. Value comparisons](https://docs.python.org/3/reference/expressions.html#value-comparisons)

`<`, `>`, `==`, etc. compare **values** via rich comparison methods. Default `==` uses **identity** for user instances; order comparisons on arbitrary objects raise `TypeError` unless customized.

| Type family | Equality | Ordering |
|-------------|----------|----------|
| Numbers | Cross-type numeric compare | `complex` has no order |
| `str` / `bytes` | Lexicographic by code point / byte value | Yes within type |
| Sequences | Element-wise; types must match | Lexicographic |
| `dict` | Key-value pairs equal | No ordering |
| `set` / `frozenset` | Set equality | Subset tests only |

```python
assert (1, 2) < (1, 3)
assert [1, 2] == [1, 2]
assert {"a": 1} == {"a": 1}
assert {1, 2} == {2, 1}

# Chained: y evaluated once; z skipped if x < y is false.
x, y, z = 1, 2, 99
assert x < y < z
```

`float('NaN')` breaks reflexivity: `NaN != NaN` is true. Compare singletons with `is`, not `==`.

### [6.10.2. Membership test operations](https://docs.python.org/3/reference/expressions.html#membership-test-operations)

`x in s` tests membership; `x not in s` is the negation. For sequences, equivalent to `any(x is e or x == e for e in s)`. For strings, `x in y` tests substring containment.

```python
assert 2 in [1, 2, 3]
assert "ell" in "hello"
assert "z" not in "hello"
assert "key" in {"key": 1}
```

### [6.10.3. Identity comparisons](https://docs.python.org/3/reference/expressions.html#identity-comparisons)

`x is y` is true only when `x` and `y` are the **same object** (`id(x) == id(y)`). Use for `None`, `True`, `False`, and sentinel checks—not for value equality.

```python
a = []
b = a
c = []
assert a is b
assert a is not c
assert a == c  # equal values, different objects
```

Parent: [6. Expressions](../index.md)
