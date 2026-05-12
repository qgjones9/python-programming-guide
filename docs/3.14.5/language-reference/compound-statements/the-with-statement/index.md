# [8.5. The with statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)

Scratch notes on **8.5. The with statement** within [*8. Compound statements*](https://docs.python.org/3/reference/compound_stmts.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```

Parent: [8. Compound statements](../index.md)
