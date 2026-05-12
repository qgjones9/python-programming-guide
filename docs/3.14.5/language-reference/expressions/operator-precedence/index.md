# [6.17. Operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)

Scratch notes on **6.17. Operator precedence** within [*6. Expressions*](https://docs.python.org/3/reference/expressions.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/expressions.html#operator-precedence)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/expressions.html#operator-precedence)** — especially footnotes about implementation.
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

Parent: [6. Expressions](../index.md)
