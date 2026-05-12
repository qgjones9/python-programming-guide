# [3.3. Special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names)

Scratch notes on **3.3. Special method names** within [*3. Data model*](https://docs.python.org/3/reference/datamodel.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/datamodel.html#special-method-names)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/datamodel.html#special-method-names)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

Parent: [3. Data model](../index.md)
