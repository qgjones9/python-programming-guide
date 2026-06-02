# [3.2. The standard type hierarchy](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy)

Scratch notes on **3.2. The standard type hierarchy** within [*3. Data model*](https://docs.python.org/3/reference/datamodel.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

Parent: [3. Data model](../index.md)
