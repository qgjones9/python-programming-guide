# [2.2. Other tokens](https://docs.python.org/3/reference/lexical_analysis.html#other-tokens)

Scratch notes on **2.2. Other tokens** within [*2. Lexical analysis*](https://docs.python.org/3/reference/lexical_analysis.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/lexical_analysis.html#other-tokens)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/lexical_analysis.html#other-tokens)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

Parent: [2. Lexical analysis](../index.md)
