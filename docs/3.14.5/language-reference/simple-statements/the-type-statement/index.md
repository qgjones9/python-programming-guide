# [7.14. The type statement](https://docs.python.org/3/reference/simple_stmts.html#the-type-statement)

Scratch notes on **7.14. The type statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/simple_stmts.html#the-type-statement)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-type-statement)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

Parent: [7. Simple statements](../index.md)
