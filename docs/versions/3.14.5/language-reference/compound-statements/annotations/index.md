# [Annotations](https://docs.python.org/3/reference/compound_stmts.html#annotations)

**Annotations** attach expressions to parameters (`name: expr`), returns (`-> expr`), and variables (`name: expr = value`). They are conventionally **type hints** but may be any expression. By default (3.14+), annotations are **lazily evaluated** in annotation scopes; they do not change runtime behavior unless introspected ([`dataclasses`](https://docs.python.org/3/library/dataclasses.html), [`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch), [`annotationlib`](https://docs.python.org/3/library/annotationlib.html)). Reference: [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#annotations).

Parent: [Compound statements](../index.md)

---

## Forms

| Location | Syntax |
|----------|--------|
| Parameter | `def f(x: expr, *args: expr, **kw: expr)` |
| Return | `def f() -> expr:` |
| Variable | `x: expr = value` |
| Star unpack annotation | `*ts: *tuple[int, ...]` (PEP 646) |

Annotations do not alter argument passing or assignment semantics by themselves.

---

## Evaluation models

| Mode | Runtime storage |
|------|-----------------|
| Default (3.14+) | Lazy descriptors; evaluate via `annotationlib` / attribute access |
| `from __future__ import annotations` | String form in `__annotations__` (deprecated path; PEP 749) |

Function **defaults** and **decorators** are evaluated in the definition scope, not the lazy annotation scope.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use `annotationlib.get_annotations()` for reliable introspection | Handles lazy and string forms |
| Prefer `typing.get_type_hints()` for resolved types | Follows `__wrapped__` chains |
| Quote forward references only when needed | Lazy eval often removes `NameError` at def time |
| Keep annotation expressions side-effect free | Evaluation timing is easy to misunderstand |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Inspecting `__annotations__` strings with future import | Values are `'int'`, not `int` | `get_type_hints` / `annotationlib` |
| Heavy work inside annotations | Runs when tools evaluate hints | Use string aliases or lazy imports in stubs |
| Assuming annotations enforce types | Python ignores them at runtime | Use checkers or `isinstance` tests |
| Mixing annotation scope with default expressions | Defaults evaluated eagerly at `def` | Do not reference undefined globals in defaults |

```python
# Goal: annotations stored without evaluating forward refs at def time
def later() -> "MyType":
    return MyType()


class MyType:
    pass


obj = later()
assert isinstance(obj, MyType)
assert later.__annotations__["return"] != "MyType" or isinstance(
    later.__annotations__["return"], str
)
```

```python
# Goal: variable annotation creates __annotations__ on module-like namespaces
ns = {}

def load():
    ns["x"] = 1


exec(
    """
x: int = 1
""",
    ns,
    ns,
)
assert ns["x"] == 1
assert ns.get("__annotations__", {}).get("x") is not None or "x" in ns
```

```python
# Goal: resolve annotations for introspection (typing.get_type_hints)
import typing

def add(a: int, b: int) -> int:
    return a + b


hints = typing.get_type_hints(add)
assert hints["a"] is int and hints["return"] is int
assert add(2, 3) == 5
```
