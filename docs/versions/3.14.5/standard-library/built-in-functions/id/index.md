# [id()](https://docs.python.org/3/library/functions.html#id)

## Description

Returns an integer identity for an object, unique among simultaneously live objects (in CPython, typically the memory address).

## What problem it solves

You need to distinguish object identity from equality—two equal lists may be different objects, and aliases share the same `id`.

## Implementation options

### Option 1: Detect aliasing vs copies

```python
a = [1, 2, 3]
b = a
c = list(a)
assert id(a) == id(b)
assert id(a) != id(c)
assert a == c
```

### Option 2: Use identity for sentinel checks

```python
sentinel = object()
items = [1, sentinel, 3]
assert items[1] is sentinel
```

### Option 3: `is` agrees with `id` for live objects

```python
x = object()
y = x
assert id(x) == id(y)
assert x is y
```

### Option 4: Interned small strings may share identity (CPython)

```python
a = "hello"
b = "hello"
# CPython may reuse the same str object for equal literals
assert a == b
# identity is an implementation detail; do not rely on id() for strings
assert id(a) == id(b) or a == b
```

## Best practices

- Use `is` / `is not` for `None`, sentinels, and singleton checks—not `id()` comparisons in normal code.

  ```python
  value = None
  assert value is None

  sentinel = object()
  items = [1, sentinel, 3]
  assert items[1] is sentinel
  ```

  ```python
  a = [1, 2]
  b = [1, 2]
  # Wrong style for equality checks:
  # if id(a) == id(b): ...
  assert a == b
  assert a is not b
  ```

- Never rely on `id()` values persisting after an object is garbage-collected.

  ```python
  class Holder:
      pass

  obj = Holder()
  old_id = id(obj)
  del obj
  # Do not store old_id for later identity checks after the object is gone.
  assert isinstance(old_id, int)
  ```

- `id(a) == id(b)` implies `a is b` for live objects, but equal objects are not necessarily identical.

  ```python
  x = object()
  y = x
  assert id(x) == id(y)
  assert x is y

  a = [1, 2, 3]
  c = list(a)
  assert a == c
  assert id(a) != id(c)
  ```
