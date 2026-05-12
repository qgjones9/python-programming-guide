# [6.4. Await expression](https://docs.python.org/3/reference/expressions.html#await-expression)

Scratch notes on **6.4. Await expression** within [*6. Expressions*](https://docs.python.org/3/reference/expressions.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/expressions.html#await-expression)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/expressions.html#await-expression)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

Parent: [6. Expressions](../index.md)
