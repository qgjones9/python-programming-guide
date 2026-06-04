# [typing — Support for type hints](https://docs.python.org/3/library/typing.html)

`typing` defines **annotation objects** and **runtime helpers** for static type checkers (mypy, pyright, PyCharm) and for limited runtime introspection. Annotations do not change runtime behavior unless you call helpers like `get_type_hints` or `cast`. Canonical reference: [typing.html](https://docs.python.org/3/library/typing.html).

---

## Purpose

Use `typing` to document **expected shapes** of data and callables: containers (`list[str]`), optional values (`str | None`), generic functions (`TypeVar`), structural protocols (`Protocol`), and configuration dicts (`TypedDict`). Prefer [`collections.abc`](https://docs.python.org/3/library/collections.abc.html) abstract bases for runtime `isinstance` checks; use `typing` for checker-facing contracts.

---

## Core constructs

| Construct | Role |
|-----------|------|
| `Optional[T]` / `T \| None` | Value may be missing |
| `Union[A, B]` / `A \| B` | One of several types (3.10+ prefers `\|`) |
| `Literal["a", "b"]` | Fixed set of values |
| `TypeVar`, `ParamSpec`, `TypeVarTuple` | Generic functions and classes |
| `Protocol` | Structural subtyping (duck typing for checkers) |
| `TypedDict` | Dict keys with required/optional typed fields |
| `Final`, `ClassVar`, `Annotated` | Immutability, class attributes, metadata |
| `cast`, `get_type_hints`, `overload` | Runtime hints and checker-only overloads |

---

## Example — generics and optional values

```python
from typing import TypeVar, Optional

T = TypeVar("T")

def first(items: list[T]) -> Optional[T]:
    return items[0] if items else None

assert first([1, 2, 3]) == 1
assert first([]) is None
```

---

## Example — `Protocol` for structural typing

```python
from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None: ...

def shutdown(resource: SupportsClose) -> None:
    resource.close()

class FileLike:
    def close(self) -> None:
        self.closed = True

f = FileLike()
shutdown(f)
assert f.closed is True
```

---

## Example — `TypedDict` for config blobs

```python
from typing import TypedDict, NotRequired

class ServerConfig(TypedDict):
    host: str
    port: int
    debug: NotRequired[bool]

cfg: ServerConfig = {"host": "localhost", "port": 8080}
assert cfg["port"] == 8080
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use `from __future__ import annotations` | Postpones evaluation; forward references need no quotes |
| Prefer built-in generics (`list[int]`) on 3.9+ | Shorter than `List[int]` from `typing` |
| Do not rely on `isinstance(x, list[str])` at runtime | Subscripted builtins may raise; use `list` or `collections.abc.Sequence` |
| Keep `cast` for checker appeasement only | No runtime validation; use libraries like `pydantic` when you need enforcement |
| Mark `@overload` bodies with `...` or `pass` | Only the last implementation runs at runtime |

---

## See also

- [`annotationlib`](https://docs.python.org/3/library/annotationlib.html) — introspecting annotations (3.14+)
- [PEP 484](https://peps.python.org/pep-0484/) — type hints specification
