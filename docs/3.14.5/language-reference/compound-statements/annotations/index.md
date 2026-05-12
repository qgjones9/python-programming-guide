# [8.11. Annotations](https://docs.python.org/3/reference/compound_stmts.html#annotations)

Scratch notes on **8.11. Annotations** within [*8. Compound statements*](https://docs.python.org/3/reference/compound_stmts.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/compound_stmts.html#annotations)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#annotations)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

Parent: [8. Compound statements](../index.md)
