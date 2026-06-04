# [6.15. Expression lists](https://docs.python.org/3/reference/expressions.html#expression-lists)

Comma-separated expressions form **expression lists**. Outside list/set displays, **two or more** items (or a trailing comma after one item) produce a **tuple**.

```ebnf
expression_list: expression ("," expression)* [","]
starred_expression: "*" or_expr | expression
```

| Form | Yields |
|------|--------|
| `1, 2, 3` | Tuple `(1, 2, 3)` |
| `1,` | One-item tuple `(1,)` |
| `1` (no comma) | The integer `1`, not a tuple |
| `()` | Empty tuple |

`*iterable` **unpacks** into the surrounding list, tuple, set, or call (PEP 448).

```python
assert (1, 2, 3) == (1, 2, 3)
assert (1,) == (1,)
assert 1 == 1
assert () == tuple()

first, *rest = [1, 2, 3, 4]
assert first == 1
assert rest == [2, 3, 4]

merged = (0, *[1, 2], 3)
assert merged == (0, 1, 2, 3)
```

Parent: [6. Expressions](../index.md)
