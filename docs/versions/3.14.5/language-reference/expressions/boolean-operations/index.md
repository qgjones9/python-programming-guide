# [6.11. Boolean operations](https://docs.python.org/3/reference/expressions.html#boolean-operations)

Boolean operations evaluate to either `True` or `False`. They are used to combine conditions in [`if`](../../compound-statements/the-if-statement/index.md) statements and other control flow structures.

```ebnf
boolean_expr ::= comparison_expr
                | boolean_expr "and" comparison_expr
                | boolean_expr "or" comparison_expr
                | "not" boolean_expr
```

Here's how they work:

```python
# Names bind to objects; multiple names may reference the same value (aliases).
nums = []
alias = nums
alias.append(1)
assert nums == [1]
```


**Examples:**

```python
x = 10
if x > 0 and x < 10:
    print("x is between 0 and 10")
elif x > 10 and x < 20:
    print("x is between 10 and 20")
else:
    print("x is not between 0 and 20")
```

