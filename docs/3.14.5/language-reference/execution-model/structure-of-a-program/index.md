# [4.1. Structure of a program](https://docs.python.org/3/reference/executionmodel.html#structure-of-a-program)

Scratch notes on **4.1. Structure of a program** within [*4. Execution model*](https://docs.python.org/3/reference/executionmodel.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/executionmodel.html#structure-of-a-program)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/executionmodel.html#structure-of-a-program)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

Parent: [4. Execution model](../index.md)
