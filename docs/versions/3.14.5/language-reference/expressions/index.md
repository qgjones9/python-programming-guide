# [6. Expressions](https://docs.python.org/3/reference/expressions.html)

This chapter defines the **syntax and semantics of Python expressions**: atoms, operators, calls, comprehensions embedded in displays, and the order in which sub-expressions evaluate. Full normative prose and grammar live on [docs.python.org](https://docs.python.org/3/reference/expressions.html); these notes distill each section with runnable examples.

Related chapters: [Data model](../data-model/index.md) (objects and special methods), [Simple statements](../simple-statements/index.md) (expression statements), [Compound statements](../compound-statements/index.md) (`if`, `while`, comprehensions in statement context).

---

## Section overview

| Section | Topic |
|---------|-------|
| [6.1. Arithmetic conversions](arithmetic-conversions/index.md) | Common numeric type promotion before binary ops |
| [6.2. Atoms](atoms/index.md) | Names, literals, parentheses, displays |
| [6.3. Primaries](primaries/index.md) | Attribute, subscription, call |
| [6.4. Await expression](await-expression/index.md) | `await` in coroutines |
| [6.5. The power operator](the-power-operator/index.md) | `**` and right-to-left binding |
| [6.6. Unary arithmetic and bitwise operations](unary-arithmetic-and-bitwise-operations/index.md) | `-`, `+`, `~` |
| [6.7. Binary arithmetic operations](binary-arithmetic-operations/index.md) | `+`, `-`, `*`, `/`, `//`, `%`, `@` |
| [6.8. Shifting operations](shifting-operations/index.md) | `<<`, `>>` |
| [6.9. Binary bitwise operations](binary-bitwise-operations/index.md) | `&`, `^`, `\|` |
| [6.10. Comparisons](comparisons/index.md) | Chained comparisons, `in`, `is` |
| [6.11. Boolean operations](boolean-operations/index.md) | `and`, `or`, `not` short-circuit |
| [6.12. Assignment expressions](assignment-expressions/index.md) | Walrus `:=` (PEP 572) |
| [6.13. Conditional expressions](conditional-expressions/index.md) | `x if C else y` |
| [6.14. Lambdas](lambda/index.md) | Anonymous functions |
| [6.15. Expression lists](expression-lists/index.md) | Commas, tuples, `*` unpacking |
| [6.16. Evaluation order](evaluation-order/index.md) | Left-to-right rules |
| [6.17. Operator precedence](operator-precedence/index.md) | Binding table |

---

## Cross-cutting ideas

| Idea | Where it shows up |
|------|-------------------|
| Special methods | Most operators call `__add__`, `__getitem__`, etc. — see [Special method names](../data-model/special-method-names/index.md) |
| Short-circuit | `and`, `or`, chained comparisons, conditional expressions |
| Side effects vs value | Expression lists and calls may run user code while producing a value |
| Precedence vs evaluation order | Precedence groups syntax; evaluation order is mostly left-to-right among operands |

```python
# Goal: operator chain — multiplication before addition; comparison chains
assert 2 + 3 * 4 == 14
assert 0 < 1 < 2
assert (lambda x: x * 2)(5) == 10
```

## Sections in this repo

- [6.1. Arithmetic conversions](arithmetic-conversions/index.md)
- [6.2. Atoms](atoms/index.md)
- [6.3. Primaries](primaries/index.md)
- [6.4. Await expression](await-expression/index.md)
- [6.5. The power operator](the-power-operator/index.md)
- [6.6. Unary arithmetic and bitwise operations](unary-arithmetic-and-bitwise-operations/index.md)
- [6.7. Binary arithmetic operations](binary-arithmetic-operations/index.md)
- [6.8. Shifting operations](shifting-operations/index.md)
- [6.9. Binary bitwise operations](binary-bitwise-operations/index.md)
- [6.10. Comparisons](comparisons/index.md)
- [6.11. Boolean operations](boolean-operations/index.md)
- [6.12. Assignment expressions](assignment-expressions/index.md)
- [6.13. Conditional expressions](conditional-expressions/index.md)
- [6.14. Lambdas](lambda/index.md)
- [6.15. Expression lists](expression-lists/index.md)
- [6.16. Evaluation order](evaluation-order/index.md)
- [6.17. Operator precedence](operator-precedence/index.md)
