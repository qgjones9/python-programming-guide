# [More on Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions)

Condensed notes for **§4.9** of [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html): defaults, keyword args, **`/`** and **`*`**, varargs, unpacking, **`lambda`**, docstrings, and annotations.

```python
# Default arguments are evaluated once at function definition time — avoid mutable defaults.
def append_ok(item, target=None):
    if target is None:
        target = []  # fresh list each call
    target.append(item)
    return target


assert append_ok(1) == [1] and append_ok(2) == [2]
```

## Sections in this repo

- [Default Argument Values](default-argument-values/index.md)
- [Keyword Arguments](keyword-arguments/index.md)
- [Special parameters](special-parameters/index.md)
- [Arbitrary Argument Lists](arbitrary-argument-lists/index.md)
- [Unpacking Argument Lists](unpacking-argument-lists/index.md)
- [Lambda Expressions](lambda-expressions/index.md)
- [Documentation Strings](documentation-strings/index.md)
- [Function Annotations](function-annotations/index.md)

Parent: [More Control Flow Tools](../index.md)
