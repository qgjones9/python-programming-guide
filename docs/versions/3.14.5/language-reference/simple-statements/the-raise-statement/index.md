# [7.8. The raise statement](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement)

Notes on **7.8. The raise statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement).

- `raise` with no expression re-raises the active exception inside an `except` block.
- `raise exc from cause` sets explicit exception chaining (`__cause__`); `from None` suppresses context display.
- The first expression must be a `BaseException` subclass or instance.

```python
# Raise and catch a fresh exception.
try:
    raise ValueError("bad input")
except ValueError as exc:
    assert str(exc) == "bad input"

# Re-raise preserves the active exception after handling.
seen = []
try:
    try:
        raise KeyError("missing")
    except KeyError:
        seen.append("handled")
        raise
except KeyError:
    seen.append("propagated")
assert seen == ["handled", "propagated"]
```

Parent: [7. Simple statements](../index.md)
