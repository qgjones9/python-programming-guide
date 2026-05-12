# [8.9. Coroutines](https://docs.python.org/3/reference/compound_stmts.html#coroutines)

Scratch notes on **8.9. Coroutines** within [*8. Compound statements*](https://docs.python.org/3/reference/compound_stmts.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/compound_stmts.html#coroutines)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#coroutines)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

Parent: [8. Compound statements](../index.md)
