# [Special parameters](https://docs.python.org/3/tutorial/controlflow.html#special-parameters)

Condensed notes for **§4.9.3** of [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html): positional-only (**`/`**), positional-or-keyword, and keyword-only (**`*`** or bare **`*`** with no name) parameter kinds.

```python
def f(a, /, b, *, c):
    return a + b + c


# `a` is positional-only; `b` can be positional or keyword; `c` must be passed by name.
assert f(1, 2, c=3) == 6
```

## Sections in this repo

- [Positional-or-Keyword Arguments](positional-or-keyword-arguments/index.md)
- [Positional-Only Parameters](positional-only-parameters/index.md)
- [Keyword-Only Arguments](keyword-only-arguments/index.md)
- [Function Examples](function-examples/index.md)
- [Recap](recap/index.md)

Parent: [More on Defining Functions](../index.md)
