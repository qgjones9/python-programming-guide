# [enum — Support for enumerations](https://docs.python.org/3/library/enum.html)

The [`enum`](https://docs.python.org/3/library/enum.html) module (3.4+) defines **enumerations**: sets of named constants with unique values, iterable in definition order. Enums are **not normal classes** — metaclass `EnumType` controls creation, aliases, and repr/str. Variants include `IntEnum`, `StrEnum`, and bitwise `Flag` / `IntFlag`. Full dunder/sunder rules and `verify()` constraints are on [docs.python.org](https://docs.python.org/3/library/enum.html).

---

## Defining enums — [Module Contents](https://docs.python.org/3/library/enum.html#module-contents)

| Style | Example |
|-------|---------|
| Class syntax | `class Color(Enum): RED = 1` |
| Functional API | `Color = Enum('Color', ['RED', 'GREEN'])` |
| `@unique` decorator | Ensures no duplicate values |
| `@verify` decorator | Enforce `EnumCheck` constraints |

Members are accessed as `Color.RED`; call syntax `Color(1)` looks up by value; index syntax `Color['RED']` looks up by name.

```python
# Goal: define enum and lookup by name/value
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    DONE = "done"

assert Status["PENDING"] is Status.PENDING
assert Status("done") is Status.DONE
assert list(Status)[0] is Status.PENDING
```

---

## Enum variants

| Base | Use |
|------|-----|
| `Enum` | Generic symbolic constants |
| `IntEnum` | Also subclasses `int` — compares equal to int |
| `StrEnum` | Also subclasses `str` — `auto()` lowercases name (3.11+) |
| `Flag` / `IntFlag` | Bitwise combine without losing flag type |
| `auto()` | Auto-generate values |

```python
# Goal: IntFlag for permission bits
from enum import IntFlag, auto

class Perm(IntFlag):
    READ = auto()
    WRITE = auto()
    EXEC = auto()

combo = Perm.READ | Perm.WRITE
assert combo & Perm.READ
assert Perm.READ in combo
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`StrEnum`** for string constants in 3.11+ | JSON/API friendly while staying typed |
| Use plain **`Enum`** when you need inequality vs ints | `IntEnum` compares equal to raw ints |
| Apply **`@unique`** on API surface enums | Catches accidental alias collisions |
| Never rely on **`Enum` member order** across refactors | Iteration order follows definition |
| Use **`FlagBoundary`** for strict invalid bit handling | Control overflow on bad inputs |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `Color.RED == 1` with plain `Enum` | False | Use `IntEnum` or compare `.value` |
| Subclassing enums with new members | `TypeError` unless `_ignore_` set | Extend via composition |
| Pickling by value across versions | Member set may change | Version your enum contract |
| **`auto()` start values** differ by base | Surprising offsets | Assign explicit values for stable APIs |
| Mixing `Flag` and int freely | Loses type safety | Stay in `IntFlag` operations |

---

## See also

- [`types`](../types-dynamic-type-creation-and-names-for-built-in-types/index.md) — `DynamicClassAttribute` for Enum
- [PEP 435](https://peps.python.org/pep-0435/) — original enum specification
- [`typing.Literal`](https://docs.python.org/3/library/typing.html#typing.Literal) — static-only alternative
