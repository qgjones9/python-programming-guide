# [copy — Shallow and deep copy operations](https://docs.python.org/3/library/copy.html)

The [`copy`](https://docs.python.org/3/library/copy.html) module implements **generic shallow and deep copying** for compound objects. Assignment binds names; `copy.copy` duplicates the outer container but shares nested mutables; `copy.deepcopy` recursively clones. Since 3.13, **`copy.replace`** creates updated copies of dataclasses, named tuples, and types with `__replace__`. Pickle registration hooks integrate via `copyreg`. Details on `__copy__` / `__deepcopy__` are on [docs.python.org](https://docs.python.org/3/library/copy.html).

---

## Core functions

| Function | Behavior |
|----------|----------|
| `copy.copy(obj)` | Shallow copy — one new outer object, shared innards |
| `copy.deepcopy(obj[, memo])` | Deep copy — recursive clone with cycle memo |
| `copy.replace(obj, /, **changes)` | Same type, selected fields replaced (3.13+) |

| Exception | When |
|-----------|------|
| `copy.Error` | Module-specific copy failures |

Immutable scalars (`int`, `str`, `tuple` of immutables) copy as identity.

```python
# Goal: shallow vs deep for nested list
import copy

original = [["a"], ["b"]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)
shallow[0].append("x")
assert original[0] == ["a", "x"]
assert deep[0] == ["a"]
```

---

## Built-in shortcuts

| Approach | Copies |
|----------|--------|
| `list.copy()`, `dict.copy()`, `set.copy()` | Shallow |
| `sequence[:]` | Shallow sequence slice |
| `copy.copy` on subclass | Usually same type as `copy.copy` |

Slice/copy on subclasses may yield base type — `copy.copy` preserves registered types.

```python
# Goal: functional update without mutating original (dataclasses.replace; see also copy.replace 3.13+)
from dataclasses import dataclass, replace

@dataclass
class Point:
    x: int
    y: int

p = Point(1, 2)
updated = replace(p, y=99)
assert p.y == 2 and updated.y == 99
assert isinstance(updated, Point)
```

---

## Custom copy hooks

| Method | Called by |
|--------|-----------|
| `__copy__(self)` | `copy.copy` |
| `__deepcopy__(self, memo)` | `copy.deepcopy` — call `deepcopy(child, memo)` for components |
| `__replace__(self, /, **changes)` | `copy.replace` |

Functions, modules, frames, and sockets are not truly copied — originals returned.

---

## Best practices

| Practice | Why |
|----------|-----|
| Default to **shallow** when nested data is immutable | Faster and shares read-only substructures |
| **Deepcopy** before mutating shared config trees | Prevents accidental alias bugs |
| Implement **`__deepcopy__`** only for custom graph types | Default handles cycles via memo |
| Use **`copy.replace`** for frozen/dataclass updates | Clearer than manual reconstruct |
| Avoid deepcopying **open resources** | Unsupported — reopen instead |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Shallow copy of nested dict | Inner dict shared | Deepcopy or `{k: v.copy() ...}` |
| Deepcopy infinite graphs without memo | Recursion error | Default memo handles cycles |
| Expecting deep copy of **module** | Same module object returned | Copy data, not module |
| `list.copy()` on subclass instance | May lose subclass type | `copy.copy` or override |
| Mutating during `__deepcopy__` | Inconsistent tree | Copy children before attaching |

---

## See also

- [`pickle`](https://docs.python.org/3/library/pickle.html) — shares copyreg hooks
- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) — `replace()` helper (dataclass-specific)
- [`types`](../types-dynamic-type-creation-and-names-for-built-in-types/index.md) — `SimpleNamespace` + `copy.replace`
