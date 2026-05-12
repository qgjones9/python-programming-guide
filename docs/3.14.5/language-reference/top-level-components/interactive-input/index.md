# [9.3. Interactive input](https://docs.python.org/3/reference/toplevel_components.html#interactive-input)

Scratch notes on **9.3. Interactive input** within [*9. Top-level components*](https://docs.python.org/3/reference/toplevel_components.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/toplevel_components.html#interactive-input)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/toplevel_components.html#interactive-input)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

Parent: [9. Top-level components](../index.md)
