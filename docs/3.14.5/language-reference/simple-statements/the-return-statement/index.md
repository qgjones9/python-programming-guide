# [7.6. The return statement](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement)

Scratch notes on **7.6. The return statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

Parent: [7. Simple statements](../index.md)
