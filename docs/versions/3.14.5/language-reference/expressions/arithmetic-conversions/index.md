# [6.1. Arithmetic conversions](https://docs.python.org/3/reference/expressions.html#arithmetic-conversions)

When an arithmetic operator description says numeric arguments are **converted to a common real type**, built-in numeric types follow the rules in [Numeric Types](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) of the standard library. Extensions and non-numeric operands (for example a string left operand to `%`) define their own conversion behavior.

| Situation | Typical outcome |
|-----------|-----------------|
| `int` and `float` mixed | `int` promoted to `float` |
| `int` and `complex` mixed | Both operands become `complex` |
| String `%` formatting | Left operand stays `str`; right side drives conversion |

```python
# Mixed int/float: common type is float before the operation runs.
assert 3 + 0.5 == 3.5
assert type(3 + 0.5) is float

# int + complex promotes the int side.
result = 2 + 3j
assert result == (2 + 3j)
assert type(result) is complex
```

Parent: [6. Expressions](../index.md)
