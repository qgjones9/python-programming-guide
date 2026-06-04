# [7.13. The nonlocal statement](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement)

Notes on **7.13. The nonlocal statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement).

- `nonlocal name` binds assignments to the nearest enclosing function scope (not globals).
- If no enclosing binding exists, `SyntaxError` is raised at compile time.
- Like `global`, it applies to the entire function body and is a parser directive.

```python
def make_counter(start=0):
    count = start

    def inc():
        nonlocal count
        count += 1
        return count

    return inc


step = make_counter(10)
assert step() == 11 and step() == 12
```

Parent: [7. Simple statements](../index.md)
