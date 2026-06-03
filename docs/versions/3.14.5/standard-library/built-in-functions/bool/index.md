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

### Normalizing a list of mixed inputs

```python
raw = [1, 0, "", "yes", None]
flags = [bool(v) for v in raw]
assert flags == [True, False, False, True, False]
```

## Best practices

- Remember `bool("0")` is `True`—for string configs, parse explicitly.

  ```python
  raw = "0"
  assert bool(raw)  # non-empty string is truthy

  enabled = raw.lower() in {"1", "true", "yes", "on"}
  assert not enabled
  ```

- Prefer `if x:` over `if bool(x):` when you only need branching; use `bool()` when storing or serializing a boolean.

  ```python
  items = [1, 2, 3]

  if items:
      first = items[0]
  assert first == 1

  payload = {"active": bool(items)}
  assert payload == {"active": True}
  ```

- `True` and `False` subclass `int` (`True == 1`), but use them for logic, not arithmetic.

  ```python
  assert True == 1  # surprising but true
  count = sum([True, False, True])  # works, but obscures intent
  assert count == 2
  votes = sum(1 for v in [True, False, True] if v)  # clearer
  assert votes == 2
  ```
