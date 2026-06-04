# [7.4. The pass statement](https://docs.python.org/3/reference/simple_stmts.html#the-pass-statement)

Notes on **7.4. The pass statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-pass-statement).

- `pass` is a null operation — syntactic filler where a statement is required.
- Common in empty function or class bodies until implementation arrives.

```python
# pass satisfies syntax without executing meaningful work.
def stub():
    pass


class Placeholder:
    pass


assert stub() is None
assert Placeholder.__name__ == "Placeholder"
```

Parent: [7. Simple statements](../index.md)
