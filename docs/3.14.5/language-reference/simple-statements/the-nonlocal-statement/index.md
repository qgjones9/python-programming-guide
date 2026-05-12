# [7.13. The nonlocal statement](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement)

Scratch notes on **7.13. The nonlocal statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

Parent: [7. Simple statements](../index.md)
