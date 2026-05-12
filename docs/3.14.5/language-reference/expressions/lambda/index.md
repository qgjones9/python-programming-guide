# [6.14. Lambdas](https://docs.python.org/3/reference/expressions.html#lambda)

Scratch notes on **6.14. Lambdas** within [*6. Expressions*](https://docs.python.org/3/reference/expressions.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/expressions.html#lambda)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/expressions.html#lambda)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Names bind to objects; multiple names may reference the same value (aliases).
nums = []
alias = nums
alias.append(1)
assert nums == [1]
```

Parent: [6. Expressions](../index.md)
