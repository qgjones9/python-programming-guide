# [Type parameter lists](https://docs.python.org/3/reference/compound_stmts.html#type-parameter-lists)

**Type parameter lists** (3.12+, defaults 3.13 / PEP 696) declare generic **`def`**, **`class`**, and **`type`** aliases: names in square brackets after the object name are **`typing.TypeVar`**, **`TypeVarTuple`**, or **`ParamSpec`** instances exposed on **`__type_params__`**. They are primarily for static checkers; at runtime, generics behave like non-generic counterparts except for metadata. Reference: [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#type-parameter-lists).

Parent: [Compound statements](../index.md)

---

## Syntax kinds

| Form | Runtime object |
|------|----------------|
| `T` | `typing.TypeVar("T", …)` |
| `T: int` | TypeVar with bound (lazy eval) |
| `T = default` | TypeVar with default (`__default__`) |
| `*Ts` | `TypeVarTuple` |
| `**P` | `ParamSpec` |

Bounds, constraints, and defaults are evaluated in **annotation scopes** when their `__bound__`, `__constraints__`, or `__default__` attributes are accessed — not necessarily at class/function creation.

---

## Scoping rules (summary)

| Name | Visible where |
|------|----------------|
| `T` in `def f[T](): ...` | Inside `f`’s annotations/body scope, not module scope |
| Decorators on generic `def` | Evaluated outside type-parameter scope |
| Generic class bases | Evaluated inside type-parameter scope |

---

## Best practices

| Practice | Why |
|----------|-----|
| Read `__type_params__` for introspection | Module-level `T` does not exist after `def f[T]` |
| Use defaults (PEP 696) for optional type args | Cleaner than overload-only patterns |
| Keep bounds/constraints simple | Lazy evaluation still runs your expressions when accessed |
| Pair with `typing.Generic` patterns mentally | Desugaring is roughly `annotation-def` wrapper |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Referencing `T` at module level after `class C[T]` | `NameError` | Use `C.__type_params__` |
| Assuming eager evaluation of bounds | Side effects delayed | Avoid side effects in bounds |
| Mixing legacy `Generic[T]` and new syntax | Two styles coexist | Prefer one style per codebase |
| `ParamSpec` without callable use | Checker noise | Use in `Callable[P, R]` annotations |

```python
# Goal: __type_params__ exposes declared type variables
def identity[T](value: T) -> T:
    return value


params = identity.__type_params__
assert len(params) == 1
assert params[0].__name__ == "T"
assert identity(3) == 3
```

```python
# Goal: generic class carries type params on the class object
class Box[T]:
    def __init__(self, item):
        self.item = item


assert Box.__type_params__[0].__name__ == "T"
assert Box("x").item == "x"
```

```python
# Goal: type alias statement with parameter (3.12+)
type Pair[T] = tuple[T, T]

alias_params = Pair.__type_params__
assert alias_params[0].__name__ == "T"
assert Pair[int] == tuple[int, int] or str(Pair).startswith("Pair")
```
