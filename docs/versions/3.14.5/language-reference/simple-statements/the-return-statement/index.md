# [7.6. The return statement](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement)

Notes on **7.6. The return statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement).

- `return` may appear only inside a function definition (not nested class bodies at module level rules).
- Bare `return` or `return` with no expression list yields `None`.
- In generators, `return value` finishes the iterator; `StopIteration.value` carries the value (3.3+).

```python
def add(a, b):
    return a + b


assert add(2, 3) == 5
def implicit_none():
    return


assert implicit_none() is None
```

Parent: [7. Simple statements](../index.md)
