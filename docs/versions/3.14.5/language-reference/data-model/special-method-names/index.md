# [3.3. Special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names)

Classes customize Python syntax and built-ins by defining methods whose names begin and end with double underscores (**dunder methods**). For example, `x[i]` roughly calls `type(x).__getitem__(x, i)`. §3.3 catalogs every special name; this page groups them for study. Full semantics—including **special method lookup** rules—are in the [official section](https://docs.python.org/3/reference/datamodel.html#special-method-names).

## Core rules

| Rule | Effect |
|------|--------|
| **Missing method** | Operation raises `AttributeError` or `TypeError` |
| **Set method to `None`** | Operation is explicitly unsupported (no fallback) |
| **Return `NotImplemented`** | Rich comparison / numeric op may try reflected or alternate implementation |
| **`__init__` return value** | Must be `None`; otherwise `TypeError` at runtime |

```python
class NoIter:
    __iter__ = None

assert not hasattr(NoIter(), "__iter__") or NoIter.__iter__ is None
try:
    iter(NoIter())
except TypeError:
    pass
else:
    raise AssertionError("expected TypeError")
```

## Basic customization

| Method | Triggered by |
|--------|--------------|
| `__new__(cls, ...)` | Object creation (before `__init__`) |
| `__init__(self, ...)` | After `__new__`; initializes instance |
| `__del__(self)` | Finalizer (avoid for critical cleanup) |
| `__repr__(self)` | `repr()`, fallback for `str()` |
| `__str__(self)` | `str()`, `print()`, default `format()` |
| `__bytes__(self)` | `bytes()` |
| `__format__(self, format_spec)` | `format()`, f-strings, `str.format()` |
| `__lt__`, `__le__`, `__eq__`, `__ne__`, `__gt__`, `__ge__` | Rich comparisons |
| `__hash__(self)` | `hash()`; must agree with `__eq__` if defined |
| `__bool__(self)` | `bool()`, truth-value testing |

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)


p = Point(1, 2)
assert repr(p) == "Point(1, 2)"
assert p == Point(1, 2)
```

## Attribute access

| Method | When it runs |
|--------|--------------|
| `__getattr__(self, name)` | Normal lookup failed |
| `__getattribute__(self, name)` | Every attribute access (easy to recurse—delegate to `object`) |
| `__setattr__(self, name, value)` | Attribute assignment |
| `__delattr__(self, name)` | `del obj.name` |
| `__dir__(self)` | `dir(obj)` |

**Descriptors** (`__get__`, `__set__`, `__delete__` on the descriptor class) participate in attribute lookup on instances and classes—see §3.3.2.2 in the upstream docs.

## Container and iteration protocols

| Protocol | Required methods | Syntax / built-in |
|----------|------------------|-------------------|
| **Sequence / mapping** | `__getitem__`, optionally `__setitem__`, `__delitem__`, `__len__` | `x[i]`, `del x[i]`, `len(x)` |
| **Iterable** | `__iter__` | `iter(x)`, `for` loops |
| **Iterator** | `__iter__`, `__next__` | Consumes stream; raises `StopIteration` |
| **Reversible** | `__reversed__` | `reversed(x)` |
| **Container** | `__contains__` | `x in y` |

```python
class Tags:
    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items


t = Tags(["a", "b"])
assert t[0] == "a" and len(t) == 2 and "b" in t
```

## Numeric and in-place operators

Binary operators map to `__add__`, `__sub__`, etc.; reflected forms use `__radd__`, …; in-place `+=` tries `__iadd__` first. Bitwise, matrix (`@`), and augmented assignment follow the same pattern (§3.3.7–§3.3.8 upstream).

## Context managers and buffers

| Method | Used with |
|--------|-----------|
| `__enter__`, `__exit__` | `with` statement |
| `__buffer__` | [PEP 688](https://peps.python.org/pep-0688/) buffer protocol (3.12+) |

## Emulating built-ins

When modeling a built-in type, implement only the protocols that make sense—a read-only sequence might support `__getitem__` but not slicing. Setting unused special methods to `None` documents unsupported operations clearly.

## Best practices

| Practice | Why |
|----------|-----|
| Return `NotImplemented` for unknown operand types | Lets Python try reversed ops or report `TypeError` |
| Keep `__eq__` and `__hash__` consistent | Equal objects must have equal hashes if hashable |
| Use `__repr__` that is unambiguous and ideally round-trippable | Aids debugging and doctest |
| Avoid heavy work in `__del__` | Finalizers run at unpredictable times; use `contextlib.closing` or `weakref.finalize` |
| Call `super()` in `__getattribute__` / `__setattr__` overrides | Prevents infinite recursion |

Parent: [3. Data model](../index.md)
