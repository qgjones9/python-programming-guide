# [2.1. Line structure](https://docs.python.org/3/reference/lexical_analysis.html#line-structure)

Scratch notes on **2.1. Line structure** within [*2. Lexical analysis*](https://docs.python.org/3/reference/lexical_analysis.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/lexical_analysis.html#line-structure)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/lexical_analysis.html#line-structure)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

Parent: [2. Lexical analysis](../index.md)
