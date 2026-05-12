# [9.2. File input](https://docs.python.org/3/reference/toplevel_components.html#file-input)

Scratch notes on **9.2. File input** within [*9. Top-level components*](https://docs.python.org/3/reference/toplevel_components.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/toplevel_components.html#file-input)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/toplevel_components.html#file-input)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

Parent: [9. Top-level components](../index.md)
