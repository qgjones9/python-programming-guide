# [StopIteration](https://docs.python.org/3/library/exceptions.html#StopIteration)

Raised by [`next()`](https://docs.python.org/3/library/functions.html#next) and an iterator's `__next__()` to signal **no further items**. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#StopIteration).

---

## When it is raised

| Context | Behavior |
|---------|----------|
| Exhausted iterator | Normal control flow for `for` loops |
| Generator `return value` | Becomes `StopIteration(value)` (3.3+) |
| `raise StopIteration` inside generator | Converted to [`RuntimeError`](../runtimeerror/index.md) (PEP 479, 3.7+) |

---

## The `value` attribute

| Source | `StopIteration.value` |
|--------|----------------------|
| Bare `raise StopIteration` | `None` |
| `return expr` in generator | `expr` |

---

## Demonstrating raise and catch

```python
# Goal: next() raises StopIteration; for-loop consumes it
it = iter([1, 2])
assert next(it) == 1
assert next(it) == 2
caught = None
try:
    next(it)
except StopIteration as exc:
    caught = exc.value
assert caught is None

def gen():
    yield 1
    return 99

g = gen()
assert next(g) == 1
try:
    next(g)
except StopIteration as exc:
    assert exc.value == 99
```

---

## Best practices

- Do not catch `StopIteration` around `for` loops—the loop handles it.
- Related: [`StopAsyncIteration`](../stopasynciteration/index.md), [`GeneratorExit`](../generatorexit/index.md).
