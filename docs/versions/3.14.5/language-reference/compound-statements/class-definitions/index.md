# [Class definitions](https://docs.python.org/3/reference/compound_stmts.html#class-definitions)

A **`class` statement** executes its suite in a new local namespace, then creates a **class object** from the inheritance list and that namespace, binding the class name in the surrounding scope. Class attributes are defined in the body; instance attributes are typically set on `self` in methods. Metaclasses and [type parameter lists](../type-parameter-lists/index.md) customize creation. Reference: [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#class-definitions).

Parent: [Compound statements](../index.md)

---

## Execution model

| Step | Effect |
|------|--------|
| Evaluate decorators | Outermost first; must return callable applied to class |
| Build inheritance list | Each base must allow subclassing |
| Run suite in new frame | Names become class attributes (order preserved in `__dict__`) |
| Create class object | Bases + namespace; name bound in outer scope |
| `class Foo:` with no bases | Equivalent to `class Foo(object):` |

---

## Class vs instance attributes

| Kind | Defined | Access |
|------|---------|--------|
| Class attribute | In class body (`x = 1`) | Shared by instances unless shadowed |
| Instance attribute | `self.name =` in methods | Per instance |
| Descriptor | `__get__` on class attribute | Controls attribute access |

Using **mutable class attributes** as per-instance defaults causes shared state across instances.

---

## Best practices

| Practice | Why |
|----------|-----|
| Put immutable defaults on the class; mutable per instance in `__init__` | Avoid shared list/dict on the class |
| Use `__slots__` only when memory/layout warrants it | Restricts dynamic attributes |
| Decorate classes like functions (PEP 3129) | Registration, ABC enforcement, dataclass transforms |
| Read `__match_args__` when supporting `match` on your type | Enables positional class patterns |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `class C: items = []` then `self.items.append` | All instances share list | Set `self.items = []` in `__init__` |
| Assuming method dict order before 3.7 | Insertion order now guaranteed for class body | Still do not rely on reordering at runtime |
| Decorator expects instance methods on class | Class not fully built yet | Use metaclass or `__init_subclass__` |
| Multiple inheritance MRO surprises | Method resolution order | Understand C3 linearization ([data model](../../data-model/index.md)) |

```python
# Goal: class attribute vs instance shadowing
class Counter:
    total = 0

    def __init__(self):
        self.total = 1


a, b = Counter(), Counter()
assert Counter.total == 0
assert a.total == 1 and b.total == 1
```

```python
# Goal: class decorator registers subclasses
registry = []

def register(cls):
    registry.append(cls.__name__)
    return cls


@register
class Alpha:
    pass


@register
class Beta:
    pass


assert registry == ["Alpha", "Beta"]
```

```python
# Goal: __match_args__ enables positional class patterns (3.10+)
class Point:
    __match_args__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y


def origin_if_zero(p):
    match p:
        case Point(0, 0):
            return True
        case Point(x, y):
            return False


assert origin_if_zero(Point(0, 0)) is True
assert origin_if_zero(Point(1, 0)) is False
```
