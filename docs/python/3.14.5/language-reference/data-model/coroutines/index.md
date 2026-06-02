# [3.4. Coroutines](https://docs.python.org/3/reference/datamodel.html#coroutines)

Scratch notes on **3.4. Coroutines** within [*3. Data model*](https://docs.python.org/3/reference/datamodel.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/datamodel.html#coroutines)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/datamodel.html#coroutines)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

Parent: [3. Data model](../index.md)
