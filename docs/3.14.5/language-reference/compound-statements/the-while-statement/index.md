# [8.2. The while statement](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)

Scratch notes on **8.2. The while statement** within [*8. Compound statements*](https://docs.python.org/3/reference/compound_stmts.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Names bind to objects; multiple names may reference the same value (aliases).
nums = []
alias = nums
alias.append(1)
assert nums == [1]
```

Parent: [8. Compound statements](../index.md)
