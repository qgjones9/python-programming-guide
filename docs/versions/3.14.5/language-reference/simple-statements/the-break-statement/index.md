# [7.9. The break statement](https://docs.python.org/3/reference/simple_stmts.html#the-break-statement)

Notes on **7.9. The break statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-break-statement).

- `break` exits the nearest enclosing `for` or `while` loop, skipping an optional `else` suite.
- If the loop target variable was bound by `for`, it keeps its value at the break point.
- A `finally` clause on an enclosing `try` runs before the loop is actually left.

```python
# break exits early; for-target keeps its last value.
total = 0
for n in range(10):
    if n == 5:
        last = n
        break
    total += n
assert total == 10 and last == 5
```

Parent: [7. Simple statements](../index.md)
