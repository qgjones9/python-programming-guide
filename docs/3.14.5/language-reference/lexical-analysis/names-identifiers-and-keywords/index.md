# [2.3. Names (identifiers and keywords)](https://docs.python.org/3/reference/lexical_analysis.html#names-identifiers-and-keywords)

Scratch notes on **2.3. Names (identifiers and keywords)** within [*2. Lexical analysis*](https://docs.python.org/3/reference/lexical_analysis.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/lexical_analysis.html#names-identifiers-and-keywords)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/lexical_analysis.html#names-identifiers-and-keywords)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```

Parent: [2. Lexical analysis](../index.md)
