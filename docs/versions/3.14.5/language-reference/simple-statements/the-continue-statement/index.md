# [7.10. The continue statement](https://docs.python.org/3/reference/simple_stmts.html#the-continue-statement)

Notes on **7.10. The continue statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-continue-statement).

- `continue` skips the rest of the current loop body and starts the next iteration.
- Like `break`, it may appear only directly inside `for`/`while` (not inside nested defs in the loop).
- Enclosing `try`/`finally` still runs the `finally` suite before the next cycle begins.

```python
# continue skips to the next iteration without finishing the body.
evens = []
for n in range(6):
    if n % 2:
        continue
    evens.append(n)
assert evens == [0, 2, 4]
```

Parent: [7. Simple statements](../index.md)
