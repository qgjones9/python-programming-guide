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

## Best practices

- Use `is` / `is not` for `None`, sentinels, and singleton checks—not `id()` comparisons in normal code.
- Never rely on `id()` values persisting after an object is garbage-collected.
- `id(a) == id(b)` implies `a is b` for live objects, but the converse reasoning about equality is wrong.
