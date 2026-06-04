# [3.2. The standard type hierarchy](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy)

Python ships with a fixed set of **built-in types** arranged in a hierarchy. Extension modules (typically C extensions) may define additional types. §3.2 lists every intrinsic type, its operations, and special attributes—this page summarizes the structure; see the [official hierarchy](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy) for full per-type detail.

## Top-level built-in categories

| Category | Types | Role |
|----------|-------|------|
| **Singleton sentinels** | `NoneType`, `NotImplemented`, `Ellipsis` (`...`) | Absence of value, deferred operation, placeholder |
| **Numbers** | `bool`, `int`, `float`, `complex` | Numeric literals and arithmetic |
| **Sequences** | `str`, `tuple`, `bytes` (immutable); `list`, `bytearray` (mutable) | Ordered, indexed collections |
| **Sets** | `set`, `frozenset` | Unordered collections of hashable, unique items |
| **Mappings** | `dict` | Key–value associations (insertion-ordered since 3.7) |
| **Callables** | Functions, methods, classes, `staticmethod`, `classmethod`, lambdas | Invoked with `()` |
| **Modules** | `module` | Namespace for import system |
| **Classes & instances** | `type`, user classes | `type` is the metaclass of most classes |
| **I/O** | File objects | Often context managers; wrap OS streams |
| **Internal** | Code objects, frames, tracebacks, etc. | Interpreter introspection |

## Numbers

`bool` is a **subtype** of `int`; `False` and `True` behave like `0` and `1` in numeric contexts but stringify to `"False"` / `"True"`.

```python
assert issubclass(bool, int)
assert True + True == 2
assert str(True) == "True"
```

All numeric types are **immutable**. `int` has arbitrary precision; `float` and `complex` use machine doubles.

## Sequences

Sequences support `len()`, indexing `a[i]`, and slicing `a[start:stop:step]`. Negative indices count from the end.

| Kind | Mutable? | Notes |
|------|----------|-------|
| `str` | No | Sequence of Unicode code points; no separate `char` type |
| `tuple` | No | `(x,)` needs a trailing comma; `()` is empty |
| `bytes` | No | Integers 0–255 |
| `list` | Yes | Arbitrary objects; `[]` literal |
| `bytearray` | Yes | Mutable bytes; unhashable |

```python
s = "hi"
assert s[-1] == "i"
assert ord("A") == 65 and chr(65) == "A"
```

## Sets and mappings

Set elements must be **hashable** and **immutable** (in the hash sense). `1` and `1.0` compare equal and cannot both appear in one set.

Dict keys follow the same hash rules. **Insertion order** is preserved (language guarantee since 3.7).

```python
d = {}
d[1] = "one"
d[1.0] = "float key"  # same slot as 1
assert list(d) == [1]
assert d[1] == "float key"
```

## Callable types

| Callable kind | Created by | Notes |
|---------------|------------|-------|
| User function | `def` / `lambda` | Has `__code__`, defaults, closure cells |
| Method | Attribute lookup on instance/class | Bound methods set `__self__` |
| Built-in function | C API | e.g. `len`, `print` |
| Class | `class` statement | Calling it creates an instance |
| Generator / coroutine | `yield` / `async def` | See [Coroutines](../coroutines/index.md) |

## Modules, classes, and instances

- **Modules** expose `__dict__`, `__name__`, and import-related attributes; prefer `__spec__` for loader metadata in new code.
- **Classes** are objects too (`type` or a metaclass). Attribute lookup uses the **MRO** (C3 linearization).
- **Instances** store attributes in `__dict__` unless restricted by `__slots__`.

```python
class C:
    x = 1

assert C.x == 1
obj = C()
assert obj.x == 1
assert type(obj) is C
assert type(C) is type
```

## `NotImplemented` and `Ellipsis`

| Name | Truth value (3.14+) | Typical use |
|------|---------------------|-------------|
| `NotImplemented` | Evaluating in boolean context raises `TypeError` | Return from unsupported rich comparisons / numeric ops |
| `Ellipsis` (`...`) | `True` | Placeholder in slicing; typing stubs |

```python
assert ... is Ellipsis
# NotImplemented must not be used in boolean tests (TypeError since 3.14)
```

## Best practices

| Practice | Why |
|----------|-----|
| Use `isinstance(obj, cls)` for type checks | Respects inheritance; `type(x) is cls` ignores subclasses |
| Know hashability rules before using sets/dict keys | Lists and dicts are unhashable |
| Prefer `__spec__` over legacy module attributes | `__loader__`, `__package__` are deprecated |
| Read special attributes as implementation hooks | Names like `__dict__` on modules are for introspection |

Parent: [3. Data model](../index.md)
