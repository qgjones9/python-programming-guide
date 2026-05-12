# [1.2. Notation](https://docs.python.org/3/reference/introduction.html#notation)

Scratch notes on **1.2. Notation** within [*1. Introduction*](https://docs.python.org/3/reference/introduction.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/introduction.html#notation)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/introduction.html#notation)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```

Parent: [1. Introduction](../index.md)
