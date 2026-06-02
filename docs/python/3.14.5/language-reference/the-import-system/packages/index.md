# [5.2. Packages](https://docs.python.org/3/reference/import.html#packages)

Scratch notes on **5.2. Packages** within [*5. The import system*](https://docs.python.org/3/reference/import.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/import.html#packages)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/import.html#packages)** — especially footnotes about implementation.
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

Parent: [5. The import system](../index.md)
