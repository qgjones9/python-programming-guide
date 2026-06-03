# [AssertionError](https://docs.python.org/3/library/exceptions.html#AssertionError)

Raised when an `assert` statement evaluates to false. Full reference: [docs.python.org](https://docs.python.org/3/library/exceptions.html#AssertionError). Assertions are for **internal consistency checks**, not for validating user input or external data.

---

## When it is raised

| Situation | Example |
|-----------|----------|
| Condition is false | `assert x > 0` when `x` is negative |
| Optional message | `assert items, 'need at least one item'` |
| Disabled with `-O` | Assertions stripped at compile time when Python runs with optimization |

---

## Demonstrating raise and catch

```python
# Goal: failed assert raises AssertionError
caught = None
try:
    assert 2 + 2 == 5, 'math broke'
except AssertionError as exc:
    caught = str(exc)
assert caught == 'math broke'
```

---

## Best practices

- Use `assert` only for conditions that **must** hold if the program is correct; use `if` / `raise ValueError` for user-facing validation.
- Never rely on assertions for security or I/O correctness—they disappear under `python -O`.
- In tests, prefer `unittest` / `pytest` assertion helpers over bare `assert` when you need rich failure output.

---

## Related exceptions

| Type | Relationship |
|------|--------------|
| [`Exception`](../base-classes/exception/index.md) | Direct base class |
| [`ValueError`](valueerror/index.md) | Prefer for invalid user arguments |
