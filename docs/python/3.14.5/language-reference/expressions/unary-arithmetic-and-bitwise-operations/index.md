# [6.6. Unary arithmetic and bitwise operations](https://docs.python.org/3/reference/expressions.html#unary-arithmetic-and-bitwise-operations)

Scratch notes on **6.6. Unary arithmetic and bitwise operations** within [*6. Expressions*](https://docs.python.org/3/reference/expressions.html); language lawyers should keep the **[official §](https://docs.python.org/3/reference/expressions.html#unary-arithmetic-and-bitwise-operations)** open.

- Normative wording lives at **[docs.python.org](https://docs.python.org/3/reference/expressions.html#unary-arithmetic-and-bitwise-operations)** — especially footnotes about implementation.
- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.
- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

Parent: [6. Expressions](../index.md)
