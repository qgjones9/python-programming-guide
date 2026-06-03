# [enumerate()](https://docs.python.org/3/library/functions.html#enumerate)

## Description

Returns an iterator of `(index, value)` pairs while looping over any iterable, with an optional start index.

## What problem it solves

Plain `for item in items` loops hide position information; manual counters with `range(len(...))` are awkward and fail for generators.

## Implementation options

### Option 1: Number lines in a report

```python
lines = ["alpha", "beta", "gamma"]
numbered = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
assert numbered[0] == "1: alpha"
```

### Option 2: Start counting at one for user-facing labels

```python
tasks = ["deploy", "verify", "rollback"]
labels = {i: name for i, name in enumerate(tasks, start=1)}
assert labels[1] == "deploy"
assert labels[3] == "rollback"
```

## Best practices

- Prefer `enumerate` over `range(len(x))` when you need both index and element.
- Use the `start` parameter for human-readable numbering (1-based lists, ranked output).
- Unpack directly in the loop: `for i, item in enumerate(items)`.
