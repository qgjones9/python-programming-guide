# [GeneratorExit](https://docs.python.org/3/library/exceptions.html#GeneratorExit)

Raised when a **generator or coroutine is closed** via `.close()`. It inherits from [`BaseException`](../base-classes/baseexception/index.md), not [`Exception`](../base-classes/exception/index.md), because closing is control flow—not a program error. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#GeneratorExit).

---

## When it is raised

| Trigger | Notes |
|---------|-------|
| `gen.close()` | Injects `GeneratorExit` into the generator frame |
| GC of unclosed generator | May close implicitly |
| Must not be swallowed | Re-raise or allow propagation |

---

## Demonstrating raise and catch

```python
# Goal: close() ends the generator via GeneratorExit
def gen():
    try:
        yield 1
    except GeneratorExit:
        return

g = gen()
assert next(g) == 1
g.close()  # completes without error
assert issubclass(GeneratorExit, BaseException)
assert not issubclass(GeneratorExit, Exception)
```

---

## Best practices

- Use `try` / `finally` inside generators for cleanup; treat `GeneratorExit` like a shutdown signal.
- Broad `except Exception` will **not** catch `GeneratorExit`—by design.
- Related: [`StopIteration`](stopiteration/index.md) for normal exhaustion.
