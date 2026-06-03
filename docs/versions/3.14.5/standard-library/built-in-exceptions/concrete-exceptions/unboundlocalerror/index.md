# [UnboundLocalError](https://docs.python.org/3/library/exceptions.html#UnboundLocalError)

Subclass of [`NameError`](nameerror/index.md) raised when a **local variable is referenced before assignment** in a function or method. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#UnboundLocalError).

---

## When it is raised

| Pattern | Why |
|---------|-----|
| Read before assign in same function | Python treats name as local because of later assignment |
| `global` / `nonlocal` omitted | Inner function shadows outer binding incorrectly |
| Conditional assignment | Reference in branch where assign never ran |

Classic example: using a counter before `count += 1` without initializing `count = 0`.

---

## Demonstrating raise and catch

```python
# Goal: UnboundLocalError when local is read before bind
def broken():
    print(x)
    x = 1

caught = None
try:
    broken()
except UnboundLocalError as exc:
    caught = type(exc).__name__
assert caught == 'UnboundLocalError'
assert issubclass(UnboundLocalError, NameError)
```

---

## Best practices

- Initialize locals before use; use `nonlocal` when mutating enclosing scope.
- Catch `NameError` (base) if you want both unbound-local and undefined-global failures.
- Parent: [`NameError`](nameerror/index.md).
