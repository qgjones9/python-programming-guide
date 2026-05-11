# [A First Look at Classes](https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes)

Condensed notes for **§9.3** of [Classes](https://docs.python.org/3/tutorial/classes.html): class objects, instance objects, method objects, and how **`__init__`** wires initial state.

```python
class Point:
    """Minimal class: instances carry `x` and `y` on `self`."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


p = Point(3, 4)
assert p.x * p.x + p.y * p.y == 25
```

## Sections in this repo

- [Class Definition Syntax](class-definition-syntax/index.md)
- [Class Objects](class-objects/index.md)
- [Instance Objects](instance-objects/index.md)
- [Method Objects](method-objects/index.md)
- [Class and Instance Variables](class-and-instance-variables/index.md)

Parent: [Classes](../index.md)
