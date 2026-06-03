# [RecursionError](https://docs.python.org/3/library/exceptions.html#RecursionError)

Subclass of [`RuntimeError`](runtimeerror/index.md) raised when the interpreter exceeds **maximum recursion depth** ([`sys.getrecursionlimit()`](https://docs.python.org/3/library/sys.html#sys.getrecursionlimit)). Added in Python 3.5 ([docs.python.org](https://docs.python.org/3/library/exceptions.html#RecursionError)).

---

## When it is raised

| Cause | Fix |
|-------|-----|
| Infinite recursion | Add base case |
| Deep but finite recursion | Rewrite iteratively or increase limit cautiously |
| Mutual recursion without base | Restructure algorithm |

---

## Demonstrating raise and catch

```python
# Goal: deep recursion raises RecursionError
def recurse(n):
    return recurse(n - 1) if n else 0

caught = None
try:
    recurse(10_000_000)
except RecursionError:
    caught = 'limit'
assert caught == 'limit'
assert issubclass(RecursionError, RuntimeError)
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| Fix base case / use iteration | Preferred over raising recursion limit |
| `except RecursionError` | Guard dynamic user code (eval, plugins) |
| `sys.setrecursionlimit()` | Last resort after algorithm review |

Related: [`RuntimeError`](runtimeerror/index.md).

---

## Best practices

- Fix the algorithm rather than raising `sys.setrecursionlimit()` without analysis.
- Parent: [`RuntimeError`](runtimeerror/index.md).
