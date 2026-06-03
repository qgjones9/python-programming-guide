# [NotImplementedError](https://docs.python.org/3/library/exceptions.html#NotImplementedError)

Subclass of [`RuntimeError`](runtimeerror/index.md) for abstract methods that subclasses must override, or placeholders during development. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#NotImplementedError). **Not** the same as the singleton [`NotImplemented`](https://docs.python.org/3/library/constants.html#NotImplemented).

---

## When to raise it

| Situation | Correct signal |
|-----------|------------------|
| Abstract method in base class | **`NotImplementedError`** |
| Operation never supported on this type | Leave method undefined or set to `None` |
| Wrong operand types | [`TypeError`](typeerror/index.md) |
| Supported in principle but not yet coded | **`NotImplementedError`** |

---

## Demonstrating raise and catch

```python
# Goal: base class stub raises NotImplementedError
class Shape:
    def area(self):
        raise NotImplementedError('subclasses must implement area')

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

caught = None
try:
    Shape().area()
except NotImplementedError:
    caught = 'stub'
assert caught == 'stub'
assert Square(3).area() == 9
```

---

## Best practices

- Prefer `abc.ABC` and `@abstractmethod` for formal abstract APIs.
- Do not use for “wrong type” cases—that is [`TypeError`](typeerror/index.md).
- Parent: [`RuntimeError`](runtimeerror/index.md).
