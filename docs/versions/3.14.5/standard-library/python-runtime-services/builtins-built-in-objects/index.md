# [builtins — Built-in objects](https://docs.python.org/3/library/builtins.html)

The [`builtins`](https://docs.python.org/3/library/builtins.html) module is the namespace of **built-in names** — `len`, `range`, `open`, exception classes, and singletons like `None`, `True`, `False`. Normal Python code sees these without importing; the module exists for introspection and for environments that restrict `__builtins__`. Reference: [docs.python.org](https://docs.python.org/3/library/builtins.html).

---

## Relationship to `__builtins__`

| Context | Binding |
|---------|---------|
| Module globals | `__builtins__` is usually the `builtins` module (or its dict) |
| Restricted execution | Custom dict can shadow built-ins deliberately |
| `import builtins` | Explicit access to the same objects |

Built-in functions are instances of `builtin_function_or_method`; built-in types subclass `type`.

---

## Common introspection patterns

```python
# Goal: resolve a built-in by name and call it
import builtins

fn = getattr(builtins, "abs")
assert fn is abs
assert fn(-3) == 3
assert getattr(builtins, "ValueError") is ValueError
assert getattr(builtins, "None") is None
```

```python
# Goal: check whether a name is a built-in type
import builtins

assert isinstance(builtins.dict, type)
assert issubclass(builtins.str, builtins.object)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Avoid **`from builtins import *`** in libraries | Pollutes namespace; surprises readers |
| Use **`getattr(builtins, name, default)`** in sandboxes | Graceful missing built-in handling |
| Prefer direct **`open`/`len`** in application code | Clearer than indirection through module |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Shadowing built-ins (`list = 1`) | Breaks downstream code in same scope | Never reuse built-in names |
| Mutating `builtins` module | Global interpreter corruption | Treat as read-only |

---

## See also

- [Built-in Types](../built-in-types/index.md) — stdlib chapter on `int`, `str`, containers, …
- [Built-in Exceptions](../built-in-exceptions/index.md) — exception hierarchy
- [`sys`](../sys-system-specific-parameters-and-functions/index.md) — interpreter services (separate from built-in objects)
