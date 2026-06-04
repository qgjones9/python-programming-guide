# [7.14. The type statement](https://docs.python.org/3/reference/simple_stmts.html#the-type-statement)

Notes on **7.14. The type statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-type-statement).

- `type Name = expression` declares a type alias (`typing.TypeAliasType`), added in Python 3.12 (PEP 695).
- The RHS is evaluated lazily when `Name.__value__` is accessed (annotation scope).
- `type` is a soft keyword; generic aliases add a type parameter list after the name.

```python
# type aliases are TypeAliasType instances with lazy __value__.
type Point = tuple[float, float]

assert Point.__name__ == "Point"
assert Point.__value__ == tuple[float, float]

type IntMap = dict[str, int]
assert IntMap.__value__ == dict[str, int]
```

Parent: [7. Simple statements](../index.md)
