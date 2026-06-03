# [5.6. Replacing the standard import system](https://docs.python.org/3/reference/import.html#replacing-the-standard-import-system)

Scratch notes on **5.6. Replacing the standard import system** within [*5. The import system*](https://docs.python.org/3/reference/import.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/import.html#replacing-the-standard-import-system)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/import.html#replacing-the-standard-import-system)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

Parent: [5. The import system](../index.md)
