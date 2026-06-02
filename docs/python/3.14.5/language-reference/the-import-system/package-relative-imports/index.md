# [5.7. Package Relative Imports](https://docs.python.org/3/reference/import.html#package-relative-imports)

Scratch notes on **5.7. Package Relative Imports** within [*5. The import system*](https://docs.python.org/3/reference/import.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/import.html#package-relative-imports)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/import.html#package-relative-imports)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

Parent: [5. The import system](../index.md)
