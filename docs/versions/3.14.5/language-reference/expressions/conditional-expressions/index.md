# [6.13. Conditional expressions](https://docs.python.org/3/reference/expressions.html#conditional-expressions)

Also called the **ternary operator**, `x if C else y` is an expression that picks one of two values (PEP 308). The **condition** `C` is evaluated first; only then is `x` or `y` evaluated.

```ebnf
conditional_expression: or_test ["if" or_test "else" expression]
```

Unlike an `if` statement, this form **returns a value** and can nest inside other expressions. The `else` branch binds less tightly than conditional expressions to its left (see [Operator precedence](../operator-precedence/index.md)).

```python
def sign(n):
    return "positive" if n > 0 else "non-positive"


assert sign(3) == "positive"
assert sign(-1) == "non-positive"
assert sign(0) == "non-positive"

# Condition checked before branches; only one branch runs.
x = 0
result = (1 / x) if False else "safe"
assert result == "safe"
```

Parent: [6. Expressions](../index.md)
