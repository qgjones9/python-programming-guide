# [5.1. importlib](https://docs.python.org/3/reference/import.html#importlib)

Scratch notes on **5.1. importlib** within [*5. The import system*](https://docs.python.org/3/reference/import.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/import.html#importlib)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/import.html#importlib)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

Parent: [5. The import system](../index.md)
