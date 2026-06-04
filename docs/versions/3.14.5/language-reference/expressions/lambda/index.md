# [6.14. Lambdas](https://docs.python.org/3/reference/expressions.html#lambda)

**Lambda expressions** create anonymous function objects:

```ebnf
lambda_expr: "lambda" [parameter_list] ":" expression
```

A lambda is equivalent to `def _lambda(params): return expression` but cannot contain statements, annotations, or assignment statements in the body.

```python
square = lambda x: x * x
assert square(5) == 25

pairs = [(1, "b"), (0, "a"), (2, "c")]
sorted_pairs = sorted(pairs, key=lambda item: item[0])
assert sorted_pairs == [(0, "a"), (1, "b"), (2, "c")]

# Default arguments work like in def.
scale = lambda x, factor=2: x * factor
assert scale(3) == 6
assert scale(3, factor=10) == 30
```

Use a regular `def` when the function needs multiple statements, docstrings, or annotations.

Parent: [6. Expressions](../index.md)
