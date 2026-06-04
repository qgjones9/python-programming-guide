# [6.11. Boolean operations](https://docs.python.org/3/reference/expressions.html#boolean-operations)

Boolean operators combine comparison expressions. Grammar:

```ebnf
or_test:  and_test | or_test "or" and_test
and_test: not_test | and_test "and" not_test
not_test: comparison | "not" not_test
```

### Truth values

In boolean contexts, these are **false**: `False`, `None`, numeric zero, empty strings, and empty containers. Everything else is true unless `__bool__` or `__len__` says otherwise.

### Short-circuit evaluation

| Expression | Behavior |
|------------|----------|
| `x and y` | If `x` is false, return `x` without evaluating `y`; else return `y` |
| `x or y` | If `x` is true, return `x` without evaluating `y`; else return `y` |
| `not x` | Always returns `True` or `False` |

**Important:** `and` / `or` return the **last evaluated operand**, not necessarily a `bool`. Only `not` always produces a boolean.

```python
assert (0 and 99) == 0
assert (1 and 99) == 99
assert (0 or 99) == 99
assert (1 or 99) == 1
assert not "" == True
assert not "hello" == False

# Default-value idiom: empty string is falsy.
name = ""
label = name or "anonymous"
assert label == "anonymous"
```

Parent: [6. Expressions](../index.md)
