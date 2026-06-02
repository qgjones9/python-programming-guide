# [3.1. Objects, values and types](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types)

Scratch notes on **3.1. Objects, values and types** within [*3. Data model*](https://docs.python.org/3/reference/datamodel.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Names bind to objects; multiple names may reference the same value (aliases).
nums = []
alias = nums
alias.append(1)
assert nums == [1]
```

Parent: [3. Data model](../index.md)
