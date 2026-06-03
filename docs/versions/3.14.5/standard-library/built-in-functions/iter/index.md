# [iter()](https://docs.python.org/3/library/functions.html#iter)

## Description

With one argument, `iter(iterable)` returns an iterator object. With two arguments, `iter(callable, sentinel)` calls `callable` with no arguments until the return value equals `sentinel`.

## What problem it solves

Manual iteration starts with obtaining an iterator—whether from a collection or from repeated reads (fixed-size blocks, polling until done).

## Implementation options

### Iterator from a list

```python
it = iter([10, 20, 30])
assert next(it) == 10
assert list(it) == [20, 30]
```

### Callable plus sentinel for block reads

```python
from io import BytesIO

data = BytesIO(b"abcdefgh")
blocks = list(iter(lambda: data.read(3), b""))
assert blocks == [b"abc", b"def", b"gh"]
```

### Strings are iterable but not always iterators

```python
word = "abc"
assert list(iter(word)) == ["a", "b", "c"]
```

## Best practices

- Prefer `for item in iterable` when you do not need the iterator object itself.

  ```python
  total = 0
  for n in [10, 20, 30]:
      total += n
  assert total == 60
  ```

  ```python
  it = iter([10, 20, 30])
  assert next(it) == 10
  assert list(it) == [20, 30]
  ```

- The two-argument form is ideal for reading chunks until EOF without a manual while loop.

  ```python
  from io import BytesIO

  data = BytesIO(b"abcdefgh")
  blocks = list(iter(lambda: data.read(3), b""))
  assert blocks == [b"abc", b"def", b"gh"]
  ```

- Calling `iter()` on a generator returns the same generator object, not a fresh copy.

  ```python
  def gen():
      yield 1
      yield 2

  g = gen()
  assert iter(g) is g
  assert list(g) == [1, 2]
  assert list(g) == []  # exhausted; no rewind
  ```
