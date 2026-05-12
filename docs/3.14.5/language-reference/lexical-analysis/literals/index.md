# [2.4. Literals](https://docs.python.org/3/reference/lexical_analysis.html#literals)

Scratch notes on **2.4. Literals** within [*2. Lexical analysis*](https://docs.python.org/3/reference/lexical_analysis.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/lexical_analysis.html#literals)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/lexical_analysis.html#literals)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

Parent: [2. Lexical analysis](../index.md)
