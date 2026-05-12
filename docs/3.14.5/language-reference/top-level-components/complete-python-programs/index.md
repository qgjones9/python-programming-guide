# [9.1. Complete Python programs](https://docs.python.org/3/reference/toplevel_components.html#complete-python-programs)

Scratch notes on **9.1. Complete Python programs** within [*9. Top-level components*](https://docs.python.org/3/reference/toplevel_components.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/toplevel_components.html#complete-python-programs)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/toplevel_components.html#complete-python-programs)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

Parent: [9. Top-level components](../index.md)
