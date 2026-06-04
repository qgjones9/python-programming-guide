# [dataclasses — Data Classes](https://docs.python.org/3/library/dataclasses.html)

[`dataclasses`](https://docs.python.org/3/library/dataclasses.html) generates **boilerplate methods** (`__init__`, `__repr__`, comparisons, …) for classes mainly holding attributes. Added in 3.7; options include `frozen`, `slots`, `kw_only`, and field factories via `field()`. Reference: [docs.python.org](https://docs.python.org/3/library/dataclasses.html).

---

## Decorator and fields

| Parameter | Effect |
|-----------|--------|
| `@dataclass` | Synthesize dunder methods |
| `frozen=True` | Immutable instances (`__setattr__` raises) |
| `slots=True` | `__slots__` memory layout (3.10+) |
| `order=True` | Ordering comparisons from fields |
| `field(default=…, default_factory=…, repr=…, compare=…)` | Per-field metadata |

```python
# Goal: minimal dataclass with repr and equality
from dataclasses import dataclass, field

@dataclass
class InventoryItem:
    name: str
    quantity: int = 0
    tags: list[str] = field(default_factory=list)

item = InventoryItem("widget", 3, ["sale"])
assert item.name == "widget" and item.quantity == 3
copy = InventoryItem("widget", 3, ["sale"])
assert item == copy
assert "InventoryItem" in repr(item)
```

---

## Post-init and inheritance

Use `__post_init__(self)` for validation after generated `__init__`. Subclassing merges fields; defaults in subclasses follow dataclass ordering rules — put non-default fields before defaulted ones.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`default_factory=list`** for mutable defaults | Avoid shared state across instances |
| Pick **`frozen=True`** for hashable value objects | Enables dict/set keys when combined with `eq` |
| Prefer **`slots=True`** for large collections of instances | Lower memory footprint |
| Keep **`typing` annotations** accurate | Enables static checkers and [`annotationlib`](../annotationlib-functionality-for-introspecting-annotations/index.md) |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `field(default=[])` | Shared list across instances | Always `default_factory` |
| Mutating **frozen** instance | `FrozenInstanceError` | Use `replace()` to derive new object |
| Expecting dataclass to validate types | No runtime enforcement by default | Add `__post_init__` checks or use pydantic |

---

## See also

- [`typing`](https://docs.python.org/3/library/typing.html) — generics used in field annotations
- [`inspect`](../inspect-inspect-live-objects/index.md) — signature introspection on generated `__init__`
