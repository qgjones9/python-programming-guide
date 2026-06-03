# [Type Annotation Types — Generic Alias, Union](https://docs.python.org/3/library/stdtypes.html#type-annotation-types-generic-alias-union)

Runtime support for modern **type hints** centers on two built-in constructs: **`GenericAlias`** (parameterized types like `list[int]`) and **union** objects (`int | str`). They exist primarily for **annotations** and introspection— the interpreter does **not** enforce them at runtime. Full specification remains on [docs.python.org](https://docs.python.org/3/library/stdtypes.html#type-annotation-types-generic-alias-union); this page explains how they behave in code.

---

## Role in Python’s typing story

| Construct | Syntax example | Static checker | Runtime |
|-----------|----------------|----------------|---------|
| **Generic alias** | `list[float]`, `dict[str, int]` | Element/key/value types | `types.GenericAlias` proxy; no element checking |
| **Union** | `int \| str`, `str \| None` | Accept any member type | `typing.Union` instance (3.14+); limited `isinstance` |

See [PEP 484](https://peps.python.org/pep-0484/) (type hints), [PEP 585](https://peps.python.org/pep-0585/) (built-in generics), and [PEP 604](https://peps.python.org/pep-0604/) (`X | Y` unions). User-defined generics are documented under [**Generics**](https://docs.python.org/3/library/typing.html#generics) in the **`typing`** module.

---

## [Generic Alias Type](https://docs.python.org/3/library/stdtypes.html#generic-alias-type)

<a id="generic-alias-type"></a>

**`GenericAlias`** objects are usually created by **subscripting** a class: `list[int]`, `dict[str, list[int]]`. They act as a **proxy** for a parameterized generic— mainly for annotations and reflection.

!!! note
    Subscripting requires the class to implement **`__class_getitem__()`** (standard library containers since 3.9).

### Containers vs non-containers

| Pattern | Meaning | Example |
|---------|---------|---------|
| Container subscription | Element (or key/value) types | `set[bytes]`, `dict[str, int]` |
| Non-container subscription | Return types of methods | `re.Match[str]` vs `re.Match[bytes]` |

```python
import re

x = re.search('foo', 'foo')
y = re.search(b'bar', b'bar')
assert x.group(0) == 'foo'
assert y.group(0) == b'bar'
# Annotations: re.Match[str] and re.Match[bytes]
```

`GenericAlias` instances are instances of **`types.GenericAlias`**. User-defined generic specializations may use different classes but expose similar attributes.

---

### `T[X, Y, ...]` — parameterized types

Subscripting **`T`** with type arguments builds a **`GenericAlias`** describing a parameterized **`T`**.

```python
def average(values: list[float]) -> float:
    return sum(values) / len(values)

assert average([1.0, 2.0, 3.0]) == 2.0

def send_post_request(url: str, body: dict[str, int]) -> None:
    assert url.startswith('http')
    assert isinstance(body, dict)

send_post_request('https://example.com', {'retries': 3})
```

---

### Runtime behavior (no enforcement)

Annotations and generic aliases are **not enforced** by the interpreter. Calling a **`GenericAlias`** constructs a normal object; type parameters are **erased**.

```python
from types import GenericAlias

alias = list[str]
assert isinstance(alias, GenericAlias)
assert alias([1, 2, 3]) == [1, 2, 3]  # discouraged but legal
assert type(alias()) is list
```

**`isinstance()`** and **`issubclass()`** reject a **`GenericAlias`** as the second argument:

```python
try:
    isinstance([1, 2], list[str])
except TypeError:
    pass
```

**`repr()`** / **`str()`** show the parameterized form:

```python
assert repr(list[int]) == 'list[int]'
assert str(dict[str, int]) == 'dict[str, int]'
```

Double subscripting plain aliases is an error (`dict[str][str]`), but **type-variable** substitution is allowed when the index arity matches **`__args__`**:

```python
from typing import TypeVar

try:
    dict[str][str]
except TypeError:
    pass

Y = TypeVar('Y')
assert dict[str, Y][int] == dict[str, int]
```

> **Added in version 3.9:** PEP 585 built-in generic syntax.

---

### Standard generic classes (non-exhaustive)

These standard-library types support **`__class_getitem__`** and runtime parameterization:

| Module | Classes |
|--------|---------|
| *(built-in)* | `tuple`, `list`, `dict`, `set`, `frozenset`, `type` |
| **`asyncio`** | `Future`, `Task` |
| **`collections`** | `deque`, `defaultdict`, `OrderedDict`, `Counter`, `ChainMap` |
| **`collections.abc`** | `Awaitable`, `Coroutine`, `AsyncIterable`, `AsyncIterator`, `AsyncGenerator`, `Iterable`, `Iterator`, `Generator`, `Reversible`, `Container`, `Collection`, `Callable`, `Set`, `MutableSet`, `Mapping`, `MutableMapping`, `Sequence`, `MutableSequence`, `ByteString`, `MappingView`, `KeysView`, `ItemsView`, `ValuesView` |
| **`contextlib`** | `AbstractContextManager`, `AbstractAsyncContextManager` |
| **`dataclasses`** | `Field` |
| **`functools`** | `cached_property`, `partialmethod` |
| **`os`** | `PathLike` |
| **`queue`** | `LifoQueue`, `Queue`, `PriorityQueue`, `SimpleQueue` |
| **`re`** | `Pattern`, `Match` |
| **`shelve`** | `BsdDbShelf`, `DbfilenameShelf`, `Shelf` |
| **`types`** | `MappingProxyType` |
| **`weakref`** | `WeakKeyDictionary`, `WeakMethod`, `WeakSet`, `WeakValueDictionary` |

---

### Special attributes of `GenericAlias`

| Attribute | Meaning |
|-----------|---------|
| [`__origin__`](#genericalias__origin__) | Bare generic class (`list` for `list[int]`) |
| [`__args__`](#genericalias__args__) | Tuple of type arguments passed to `__class_getitem__` |
| [`__parameters__`](#genericalias__parameters__) | Lazy tuple of unique **`TypeVar`** objects in `__args__` |
| [`__unpacked__`](#genericalias__unpacked__) | `True` if unpacked with `*` ([**TypeVarTuple**](https://docs.python.org/3/library/typing.html#typing.TypeVarTuple), 3.11+) |

<a id="genericalias__origin__"></a>

### `genericalias.__origin__`

```python
assert list[int].__origin__ is list
```

<a id="genericalias__args__"></a>

### `genericalias.__args__`

```python
assert dict[str, list[int]].__args__ == (str, list[int])
```

<a id="genericalias__parameters__"></a>

### `genericalias.__parameters__`

```python
from typing import TypeVar

T = TypeVar('T')
assert list[T].__parameters__ == (T,)
```

!!! note
    Aliases with **`typing.ParamSpec`** parameters may report incorrect **`__parameters__`** after substitution— **`ParamSpec`** is mainly for static checkers.

<a id="genericalias__unpacked__"></a>

### `genericalias.__unpacked__`

Boolean: `True` when the alias was unpacked with `*`. See [**TypeVarTuple**](https://docs.python.org/3/library/typing.html#typing.TypeVarTuple).

> **Added in version 3.11.**

---

## [Union Type](https://docs.python.org/3/library/stdtypes.html#union-type)

<a id="union-type"></a>

A **union object** is the result of **`X | Y | ...`** on type objects (PEP 604). It means “**X or Y or …**” and is equivalent to **`typing.Union[X, Y, …]`** for annotation purposes.

```python
def square(number: int | float) -> int | float:
    return number ** 2

assert square(2) == 4
assert square(2.5) == 6.25
```

!!! note
    **`X | Y`** cannot be built at runtime when a member is a **forward reference** (for example `int | "Foo"` before `Foo` exists). Use a string annotation: `"int | Foo"`.

> **Added in version 3.10.**

> **Changed in version 3.14:** Union objects are instances of **`typing.Union`**. Previously they used **`types.UnionType`**, which remains an alias for **`typing.Union`**.

---

### Union equality and normalization

| Rule | Example |
|------|---------|
| Nested unions flatten | `(int \| str) \| float == int \| str \| float` |
| Duplicate members removed | `int \| str \| int == int \| str` |
| Order ignored | `int \| str == str \| int` |
| Matches `typing.Union` | `int \| str == typing.Union[int, str]` |
| Optional spelling | `str \| None == typing.Optional[str]` |

```python
import sys
import types
import typing

assert (int | str) | float == int | str | float
assert int | str | int == int | str
assert int | str == str | int
assert int | str == typing.Union[int, str]
if sys.version_info >= (3, 14):
    assert type(int | str) is typing.Union
else:
    assert type(int | str) is types.UnionType
assert str | None == typing.Optional[str]
```

---

### `isinstance()` and `issubclass()` with unions

Unions work as the **second** argument to **`isinstance()`** / **`issubclass()`** when members are plain types. **Parameterized generics** inside a union still cannot be checked.

```python
import sys
import types
import typing

assert isinstance('', int | str)
assert isinstance(1, int | list[int])  # short-circuits on int

try:
    isinstance([1], int | list[int])
except TypeError:
    pass

if sys.version_info >= (3, 14):
    assert isinstance(int | str, typing.Union)
else:
    assert isinstance(int | str, types.UnionType)

try:
    typing.Union()
except TypeError:
    pass
```

Test whether an object **is a union type** with **`isinstance(obj, typing.Union)`** (3.14+) or **`isinstance(obj, types.UnionType)`** (3.10–3.13). **`typing.Union()`** itself cannot be instantiated.

---

### Metaclass `__or__` override

Type **`__or__`** enables **`X | Y`**. A metaclass may override **`__or__`** on the left operand only:

```python
class M(type):
    def __or__(self, other):
        return 'Hello'

class C(metaclass=M):
    pass

assert C | int == 'Hello'
assert type(int | C) is type(int | str)
```

---

## Related topics in this guide

| Subject | Description |
|---------|-------------|
| [Built-in Types](../index.md) | Container types (`list`, `dict`, `set`, …) that support `T[...]` parameterization. |
| [Mapping Types — dict](../mapping-types-dict/index.md) | Runtime `dict` behavior; `dict[str, int]` is annotation-only at runtime. |
| [Set Types — set, frozenset](../set-types-set-frozenset/index.md) | `set[T]` and hashable-element rules for generic sets. |

**See also:** [PEP 484](https://peps.python.org/pep-0484/) · [PEP 585](https://peps.python.org/pep-0585/) · [PEP 604](https://peps.python.org/pep-0604/) · [`typing` — Generics](https://docs.python.org/3/library/typing.html#generics)
