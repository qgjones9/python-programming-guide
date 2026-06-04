# [6.3. Primaries](https://docs.python.org/3/reference/expressions.html#primaries)

**Primaries** are the most tightly bound expression forms. Grammar:

```ebnf
primary: atom | attributeref | subscription | call
```

### [6.3.1. Attribute references](https://docs.python.org/3/reference/expressions.html#attribute-references)

`primary.name` asks the object for attribute `name` via `__getattribute__`, falling back to `__getattr__` on `AttributeError`.

```python
class Point:
    x = 10


p = Point()
assert p.x == 10
```

### [6.3.2. Subscriptions and slicings](https://docs.python.org/3/reference/expressions.html#subscriptions-and-slicings)

`primary[subscript]` calls `__getitem__` (or `__class_getitem__` for type parameters). Slices build a `slice` object; multiple subscripts become a tuple.

```python
colors = ["red", "blue", "green", "black"]
assert colors[1] == "blue"
assert colors[1:3] == ["blue", "green"]
assert colors[::2] == ["red", "green"]

digits = {"one": 1, "two": 2}
assert digits["two"] == 2
```

Subscriptions can be assignment targets (`__setitem__`, `__delitem__`).

```python
items = [0, 1, 2]
items[0] = 99
assert items == [99, 1, 2]
```

### [6.3.3. Calls](https://docs.python.org/3/reference/expressions.html#calls)

`callable(...)` evaluates the callable and all arguments first, then binds parameters. `*iterable` and `**mapping` unpack into positional and keyword arguments.

```python
def greet(name, punctuation="!"):
    return f"Hello, {name}{punctuation}"


assert greet("world") == "Hello, world!"
assert greet(punctuation="?", name="Ada") == "Hello, Ada?"

extra = ("!",)
assert greet("Bob", *extra) == "Hello, Bob!"
```

Parent: [6. Expressions](../index.md)
