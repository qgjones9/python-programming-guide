# [bool()](https://docs.python.org/3/library/functions.html#bool)

## Description

`bool()` converts a value to `True` or `False` using Python's truth-testing rules. Called with no argument (or a falsy argument), it returns `False`; otherwise `True`. The `bool` type is a final subclass of `int` whose only instances are the singletons `True` and `False`.

## What problem it solves

APIs and conditionals need explicit boolean normalization—form input, JSON fields, or numeric flags that should read as yes/no. `bool()` applies the same rules as `if x:` in a single call.

## Implementation options

### Truth-testing common values

```python
assert bool(0) is False
assert bool(1) is True
assert bool("") is False
assert bool("hi") is True
assert bool([]) is False
assert bool([0]) is True
assert bool(None) is False
```

### Normalizing user or config input

```python
def enabled(raw) -> bool:
    return bool(raw)

assert enabled(0) is False
assert enabled("0") is True  # non-empty string is truthy
assert enabled([]) is False
```

## Best practices

- Remember `bool("0")` is `True`—for string configs, parse explicitly (`raw.lower() in {"1", "true", "yes"}`).
- Prefer `if x:` over `if bool(x):` when you only need branching; use `bool()` when storing or serializing a boolean.
- `True` and `False` subclass `int` (`True == 1`), but use them for logic, not arithmetic.
