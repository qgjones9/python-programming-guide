# [1.1. Alternate Implementations](https://docs.python.org/3/reference/introduction.html#alternate-implementations)

Scratch notes on **1.1. Alternate Implementations** within [*1. Introduction*](https://docs.python.org/3/reference/introduction.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/introduction.html#alternate-implementations)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/introduction.html#alternate-implementations)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

Parent: [1. Introduction](../index.md)
