# [enumerate()](https://docs.python.org/3/library/functions.html#enumerate)

## Description

`enumerate(iterable, start=0)` returns an iterator of `(index, value)` pairs. You get position and element together without manual counters or `range(len(...))`.

## What problem it solves

Plain `for item in items` hides position; indexing with `range(len(x))` fails on generators and is awkward. `enumerate()` is the idiomatic way to loop with a counter over any iterable.

## Implementation options

### Number lines in a report

```python
lines = ["alpha", "beta", "gamma"]
numbered = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
assert numbered[0] == "1: alpha"
assert numbered[-1] == "3: gamma"
```

### User-facing labels with `start=1`

```python
tasks = ["deploy", "verify", "rollback"]
labels = {i: name for i, name in enumerate(tasks, start=1)}
assert labels[1] == "deploy"
assert labels[3] == "rollback"
```

### Find index while scanning (unpack in the loop)

```python
names = ["ada", "grace", "linus"]
target = "grace"
for index, name in enumerate(names):
    if name == target:
        break
else:
    raise AssertionError("not found")
assert index == 1
```

## Best practices

- Prefer `enumerate` over `range(len(x))` when you need both index and element.

  ```python
  items = ["a", "b", "c"]

  # idiomatic
  pairs = list(enumerate(items))
  assert pairs == [(0, "a"), (1, "b"), (2, "c")]

  # awkward and fails on generators:
  # for i in range(len(items)):
  #     item = items[i]
  ```

- Use the `start` parameter for human-readable numbering (1-based lists, ranked output).

  ```python
  tasks = ["deploy", "verify"]
  labels = [f"{i}. {name}" for i, name in enumerate(tasks, start=1)]
  assert labels == ["1. deploy", "2. verify"]
  ```

- Unpack directly in the loop: `for i, item in enumerate(items)`.

  ```python
  names = ["ada", "grace"]
  for index, name in enumerate(names):
      if name == "grace":
          break
  assert index == 1
  ```
