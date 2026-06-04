# [abc — Abstract Base Classes](https://docs.python.org/3/library/abc.html)

The [`abc`](https://docs.python.org/3/library/abc.html) module defines **Abstract Base Classes (ABCs)**: classes that declare interface methods with `@abstractmethod`, refuse instantiation until concrete subclasses implement them, and support **virtual subclass** registration. Reference: [docs.python.org](https://docs.python.org/3/library/abc.html).

---

## Defining ABCs

| Symbol | Role |
|--------|------|
| `ABC` / `ABCMeta` | Metaclass marking abstract classes |
| `@abstractmethod` | Must be overridden in concrete subclass |
| `@classmethod` + `@abstractmethod` | Abstract class methods |
| `register(cls)` | Declare virtual subclass without inheritance |

```python
# Goal: ABC enforces interface before instantiation
from abc import ABC, abstractmethod

class Serializer(ABC):
    @abstractmethod
    def dumps(self, obj) -> bytes:
        raise NotImplementedError

class JsonSerializer(Serializer):
    def dumps(self, obj) -> bytes:
        return repr(obj).encode()

s = JsonSerializer()
assert s.dumps({"a": 1}) == b"{'a': 1}"

try:
    Serializer()
except TypeError as e:
    assert "abstract" in str(e).lower()
```

---

## Virtual subclasses

`MyABC.register(concrete)` returns `concrete` and makes `issubclass(concrete, MyABC)` true without changing MRO — useful for retro-fitting protocols onto existing types.

---

## Best practices

| Practice | Why |
|----------|-----|
| Combine with **`typing.Protocol`** for structural typing | ABCs are nominal; Protocols check shape |
| Keep ABC APIs **minimal** | Easier third-party implementations |
| Document which methods are **optional** via mixins | Avoid over-abstracting |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Instantiate ABC with unimplemented methods | `TypeError` at construction | Implement all abstract members |
| Forgetting `@abstractmethod` on placeholder bodies | Concrete class silently inherits pass | Decorator required for enforcement |

---

## See also

- [`collections.abc`](https://docs.python.org/3/library/collections.abc.html) — standard container ABCs
- [`inspect`](../inspect-inspect-live-objects/index.md) — detect abstract methods via `inspect.isabstract`
