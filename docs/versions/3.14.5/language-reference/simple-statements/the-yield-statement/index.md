# [7.7. The yield statement](https://docs.python.org/3/reference/simple_stmts.html#the-yield-statement)

Notes on **7.7. The yield statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-yield-statement).

- `yield_stmt` is semantically the same as a parenthesized yield *expression* statement.
- Using `yield` (or `yield from`) in a `def` makes that function a generator function.
- See [Yield expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions) for full semantics.

```python
def countdown(n):
    while n:
        yield n
        n -= 1


def flatten(nested):
    for part in nested:
        yield from part


assert list(countdown(3)) == [3, 2, 1]
assert list(flatten([[1, 2], [3]])) == [1, 2, 3]
```

Parent: [7. Simple statements](../index.md)
