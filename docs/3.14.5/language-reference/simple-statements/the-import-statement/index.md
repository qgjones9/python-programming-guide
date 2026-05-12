# [7.11. The import statement](https://docs.python.org/3/reference/simple_stmts.html#the-import-statement)

Scratch notes on **7.11. The import statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/simple_stmts.html#the-import-statement)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-import-statement)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

Parent: [7. Simple statements](../index.md)
