# [6.10. Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)

Scratch notes on **6.10. Comparisons** within [*6. Expressions*](https://docs.python.org/3/reference/expressions.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/expressions.html#comparisons)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/expressions.html#comparisons)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

Parent: [6. Expressions](../index.md)
