# [5.4. Loading](https://docs.python.org/3/reference/import.html#loading)

Scratch notes on **5.4. Loading** within [*5. The import system*](https://docs.python.org/3/reference/import.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/import.html#loading)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/import.html#loading)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

Parent: [5. The import system](../index.md)
