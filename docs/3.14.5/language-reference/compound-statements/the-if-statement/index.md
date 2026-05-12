# [8.1. The if statement](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement)

Scratch notes on **8.1. The if statement** within [*8. Compound statements*](https://docs.python.org/3/reference/compound_stmts.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Statements execute for effect; expressions inside them still follow semantics.
seen = []

def record():
    seen.append(True)
    return "done"


record()
assert seen == [True]
```

Parent: [8. Compound statements](../index.md)
