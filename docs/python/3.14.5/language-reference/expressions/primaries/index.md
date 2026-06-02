# [6.3. Primaries](https://docs.python.org/3/reference/expressions.html#primaries)

Scratch notes on **6.3. Primaries** within [*6. Expressions*](https://docs.python.org/3/reference/expressions.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/expressions.html#primaries)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/expressions.html#primaries)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```

Parent: [6. Expressions](../index.md)
