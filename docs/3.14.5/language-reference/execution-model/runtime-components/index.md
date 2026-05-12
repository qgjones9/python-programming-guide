# [4.4. Runtime Components](https://docs.python.org/3/reference/executionmodel.html#runtime-components)

Scratch notes on **4.4. Runtime Components** within [*4. Execution model*](https://docs.python.org/3/reference/executionmodel.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/executionmodel.html#runtime-components)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/executionmodel.html#runtime-components)** — especially footnotes about implementation.
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

Parent: [4. Execution model](../index.md)
