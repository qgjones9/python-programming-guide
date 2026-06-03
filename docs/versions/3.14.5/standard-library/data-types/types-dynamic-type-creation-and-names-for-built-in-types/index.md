# [types — Dynamic type creation and names for built-in types](https://docs.python.org/3/library/types.html)

The [`types`](https://docs.python.org/3/library/types.html) module supplies **utilities for dynamic class creation**, names for interpreter-internal types (`FunctionType`, `ModuleType`, …), and helpers like `SimpleNamespace` and `@types.coroutine`. Use it for metaclass tooling, introspection, and lightweight attribute bags. Full dynamic creation flow (`prepare_class`, PEP 560) is on [docs.python.org](https://docs.python.org/3/library/types.html).

---

## Dynamic class creation — [Dynamic Type Creation](https://docs.python.org/3/library/types.html#dynamic-type-creation)

| Function | Role |
|----------|------|
| `new_class(name, bases=(), kwds=None, exec_body=None)` | Build class with correct metaclass |
| `prepare_class(name, bases=(), kwds=None)` | Returns `(metaclass, namespace, kwds)` |
| `resolve_bases(bases)` | Expands `__mro_entries__` (PEP 560) |
| `get_original_bases(cls)` | Bases before MRO entry resolution (3.12+) |

```python
# Goal: create a class at runtime with a body callback
import types

def populate(ns):
    ns["greet"] = lambda self: f"hi {self.name}"
    ns["name"] = "world"

Dynamic = types.new_class("Dynamic", (), {}, populate)
obj = Dynamic()
assert obj.greet() == "hi world"
```

---

## Standard interpreter types — [Standard Interpreter Types](https://docs.python.org/3/library/types.html#standard-interpreter-types)

| Name | Typical `isinstance` target |
|------|----------------------------|
| `FunctionType` / `LambdaType` | User-defined functions |
| `MethodType` | Bound instance methods |
| `ModuleType` | Imported modules |
| `GeneratorType` | Generator iterators |
| `CoroutineType` / `AsyncGeneratorType` | Async generators/coroutines |
| `CodeType` | `compile()` results |
| `GenericAlias` | `list[int]`, `dict[str, int]` |
| `UnionType` | `int | str` (alias for `typing.Union`, 3.14) |
| `MappingProxyType` | Read-only dict views (`types.MappingProxyType`) |
| `SimpleNamespace` | Arbitrary attribute namespace |
| `NoneType`, `EllipsisType`, `NotImplementedType` | Singleton types |

```python
# Goal: lightweight attribute bag and mapping proxy
import types

cfg = types.SimpleNamespace(host="localhost", port=8080)
assert cfg.host == "localhost"

data = {"a": 1}
view = types.MappingProxyType(data)
data["b"] = 2
assert view["b"] == 2
assert isinstance(view, types.MappingProxyType)
```

---

## Coroutine utilities

| Function | Role |
|----------|------|
| `@types.coroutine` | Mark generator as generator-based coroutine |
| `DynamicClassAttribute` | Route class-level access to `__getattr__` (Enum pattern) |

Prefer `async def` for new coroutines; `@types.coroutine` remains for legacy bridges.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`SimpleNamespace`** instead of empty classes for ad hoc records | Meaningful `repr`, easy attribute add/remove |
| Prefer **`typing` generics** over manual `GenericAlias` | Clearer annotations |
| **`MappingProxyType`** for exposing read-only config | Prevents accidental mutation |
| **`get_original_bases`** for generic introspection tools | Shows `list[str]` not bare `list` |
| Avoid instantiating **`CodeType`** casually | Auditing events and invariants apply |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `isinstance(gencoro, CoroutineType)` false | Generator-based coroutines differ | `inspect.isawaitable` |
| Mutating **`MappingProxyType`** backing dict | View reflects changes | Copy if snapshot needed |
| **`new_class` without exec_body** | Empty class | Pass lambda ns or class statement equivalent |
| Confusing **`ModuleType`** with namespace objects | Different semantics | Use `SimpleNamespace` for data bags |

---

## See also

- [`copy`](../copy-shallow-and-deep-copy-operations/index.md) — `SimpleNamespace` supports `copy.replace`
- [`enum`](../enum-support-for-enumerations/index.md) — uses `DynamicClassAttribute`
- [`abc`](https://docs.python.org/3/library/abc.html) — metaclass ABC machinery
