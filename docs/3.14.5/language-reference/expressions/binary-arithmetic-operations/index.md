# [6.7. Binary arithmetic operations](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)

Scratch notes on **6.7. Binary arithmetic operations** within [*6. Expressions*](https://docs.python.org/3/reference/expressions.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

Parent: [6. Expressions](../index.md)
