# [sum()](https://docs.python.org/3/library/functions.html#sum)

## Description

`sum(iterable, /, start=0)` totals numeric items from left to right. The start value cannot be a string. Since 3.12, float summation uses a higher-accuracy algorithm on most builds.

## What problem it solves

Aggregating numbers—totals, counts weighted by value, running sums—without manual accumulator loops for the common case.

## Implementation options

### Sum a list of numbers

```python
values = [10, 20, 30, 5]
assert sum(values) == 65
```

### Provide a non-zero start (e.g. offset baseline)

```python
readings = [1.2, 0.8, -0.5]
assert round(sum(readings, start=100.0), 1) == 101.5
```

### Sum squares with a generator expression

```python
nums = [1, 2, 3, 4]
assert sum(x * x for x in nums) == 30
```

## Best practices

- Concatenate strings with `''.join(sequence)`, not `sum(strings, start='')`—that raises `TypeError`.

  ```python
  parts = ["hello", " ", "world"]
  assert "".join(parts) == "hello world"
  ```

  ```python
  # This will raise TypeError:
  # sum(["a", "b"], start="")
  ```

- For floating-point totals needing extra precision, consider `math.fsum()`.

  ```python
  import math

  values = [1e16, 1, -1e16, 1]
  assert math.fsum(values) == 2.0
  assert sum(values) == 1.0  # catastrophic cancellation in naive order
  ```

  ```python
  # sum() is fine for integers and many everyday float totals:
  assert sum([1, 2, 3]) == 6
  ```

- Chain iterables with `itertools.chain()` when summing multiple sources in one pass is clearer than nested loops.

  ```python
  from itertools import chain

  a, b = [1, 2], [3, 4]
  assert sum(chain(a, b)) == 10
  ```

  ```python
  # Nested loops work but are noisier when chaining is clearer:
  total = 0
  for group in ([1, 2], [3, 4]):
      for x in group:
          total += x
  assert total == 10
  ```
