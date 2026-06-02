# [2.6. Numeric literals](https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals)

When Python’s lexer scans source code, it groups digits and related characters into a single [`NUMBER`](../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#core-tokens-names-literals-and-generic-operators) token. That token is a **numeric literal**: text in your program that denotes a fixed numeric value. Like other [literals](../literals/index.md), numeric literals are evaluated during lexical analysis and become concrete values when the code runs.

Python defines three kinds of numeric literal. Each maps to a built-in type:

| Kind | Examples | Runtime type |
|------|----------|--------------|
| **Integer** | `42`, `0xFF`, `0b1010`, `1_000_000` | [`int`](../../../standard-library/built-in-functions/int/index.md) |
| **Floating-point** | `3.14`, `1.5e-3`, `.5` | [`float`](../../../standard-library/built-in-functions/float/index.md) |
| **Imaginary** | `4.2j`, `7J` | [`complex`](../../../standard-library/built-in-functions/complex/index.md) (zero real part) |

The lexer classifies a `NUMBER` token using this rule:

```ebnf
NUMBER: integer | floatnumber | imagnumber
```

There is no separate “complex literal” token. A value such as `3+4.2j` is an **expression**—an integer literal, the `+` operator, and an imaginary literal—not one lexical unit.

## How literals become values

The value of a numeric literal matches what you would get by passing the **same text** to the matching constructor:

```python
int('42') == 42          # from integer literal 42
float('3.14') == 3.14    # from float literal 3.14
complex('4.2j') == 4.2j  # from imaginary literal 4.2j
```

Constructors accept more input shapes than the lexer does. For example, `int(' 42 ')` succeeds, but a literal cannot contain leading spaces. If a string works in `int()`, `float()`, or `complex()` but is not valid source syntax, it is not a legal literal.

## Signs are operators, not part of the literal

A leading minus is **not** part of the `NUMBER` token. The lexer emits the unary `-` operator and a separate positive literal:

```python
# Two tokens: '-' and '1'
-1

x = -42   # unary minus applied to the literal 42
```

So `-1` is an expression built from an operator and the literal `1`, not a single “negative literal” token. The same rule applies to `+` in numeric contexts (for example `+3.14`).
