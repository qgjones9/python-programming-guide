# [4.2. Naming and binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)

Scratch notes on **4.2. Naming and binding** within [*4. Execution model*](https://docs.python.org/3/reference/executionmodel.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

Parent: [4. Execution model](../index.md)
