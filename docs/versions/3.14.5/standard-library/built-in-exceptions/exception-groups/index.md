# [Exception groups](https://docs.python.org/3/library/exceptions.html#exception-groups)

When several unrelated failures happen at once—parallel tasks, nested cleanup, or fan-out I/O—you often need to raise **more than one exception** as a single propagated error. Python 3.11 added [`BaseExceptionGroup`](baseexceptiongroup/index.md) and [`ExceptionGroup`](exceptiongroup/index.md) (PEP 654) for that purpose, plus the [`except*`](https://docs.python.org/3/reference/compound_stmts.html#except-star) clause to match subgroups by contained exception type. Full specification remains on [docs.python.org](https://docs.python.org/3/library/exceptions.html#exception-groups); this page explains construction, splitting, handling, and subclassing patterns.

---

## Why exception groups exist

Classic `try` / `except` handles **one** active exception at a time. Before 3.11, concurrent failures were awkward: you could chain with `raise ... from`, collect errors in a list, or lose secondary failures entirely. Exception groups preserve **every** failure while still participating in the normal hierarchy—so `except Exception` catches an `ExceptionGroup`, and `except*` can peel off matching members without dropping the rest.

| Mechanism | Handles | Typical use |
|-----------|---------|-------------|
| `except SomeError` | One exception (or subclass) | Single failure path |
| `except*` | Matching **subgroup** inside an exception group | Parallel tasks, multi-resource cleanup |
| `subgroup()` / `split()` | Programmatic filtering without `try` | Libraries building custom handlers |

---

## BaseExceptionGroup vs ExceptionGroup

Both wrap a **sequence** of exceptions (`excs`) under a string `message`. The split is deliberate:

| Type | Base class | Can wrap | Caught by `except Exception` |
|------|------------|----------|--------------------------------|
| [`BaseExceptionGroup`](baseexceptiongroup/index.md) | `BaseException` | Any `BaseException` subclass | **No** |
| [`ExceptionGroup`](exceptiongroup/index.md) | `Exception` (also `BaseExceptionGroup`) | Only `Exception` subclasses | **Yes** |

`BaseExceptionGroup(...)` **automatically returns** an `ExceptionGroup` when every contained exception is an `Exception` instance—handy when you do not know the mix ahead of time. `ExceptionGroup(...)` raises `TypeError` if any member is not an `Exception` subclass.

```python
# Goal: BaseExceptionGroup upgrades to ExceptionGroup when all members are Exception
mixed = BaseExceptionGroup("mixed", (ValueError(1), TypeError(2)))
assert type(mixed) is ExceptionGroup
assert mixed.message == "mixed"
assert len(mixed.exceptions) == 2

pure = ExceptionGroup("errors", (ValueError(1), KeyError(2)))
assert isinstance(pure, BaseExceptionGroup)
assert isinstance(pure, Exception)
```

---

## Attributes — [Exception groups](https://docs.python.org/3/library/exceptions.html#exception-groups)

| Attribute | Meaning |
|-----------|---------|
| `message` | The `msg` string passed to the constructor (read-only). |
| `exceptions` | Tuple of wrapped exceptions (read-only). Nested groups stay nested. |

For performance, pass a **tuple** as `excs` when you can; lists work but tuples are processed more efficiently in CPython.

```python
# Goal: message and exceptions reflect constructor arguments
eg = ExceptionGroup("two failures", (ValueError("a"), KeyError("b")))
assert eg.message == "two failures"
assert len(eg.exceptions) == 2
assert isinstance(eg.exceptions[0], ValueError)
assert isinstance(eg.exceptions[1], KeyError)
```

---

## Handling with `except*` — [except* clause](https://docs.python.org/3/reference/compound_stmts.html#except-star)

An `except*` clause matches **subgroups** of a raised exception group—the same type rules as `except`, applied to each contained exception. Key rules:

- A `try` may use **`except` or `except*`, not both** in the same statement.
- The exception type is **mandatory** (`except*:` is a syntax error).
- Matching types must **not** be subclasses of `BaseExceptionGroup` (that would be ambiguous).
- Each clause calls `split()` internally: the matching subgroup becomes `sys.exception()` for that handler; non-matching members flow to the next `except*` or propagate as a merged group.
- A lone non-group exception that matches is wrapped in an `ExceptionGroup` with an empty message so the handler target is always group-shaped.

```python
# Goal: except* routes each matching subgroup when all types are handled
def handle_mixed_group():
    log = []
    try:
        raise ExceptionGroup(
            "batch",
            [TypeError(2), OSError(3)],
        )
    except* TypeError as eg:
        log.append(("TypeError", len(eg.exceptions)))
    except* OSError as eg:
        log.append(("OSError", len(eg.exceptions)))
    return log

assert handle_mixed_group() == [("TypeError", 1), ("OSError", 1)]
```

When every member is handled across the `except*` chain, execution continues after the `try`. Any unhandled subgroup is re-raised (merged with exceptions raised inside handlers).

```python
# Goal: unhandled subgroup re-raises after except* chain
def leftover_propagates():
    try:
        raise ExceptionGroup("eg", [ValueError(1), TypeError(2)])
    except* ValueError:
        pass  # TypeError not handled here
    return "unreachable"

try:
    leftover_propagates()
except ExceptionGroup as remaining:
    assert len(remaining.exceptions) == 1
    assert isinstance(remaining.exceptions[0], TypeError)
```

---

## `subgroup(condition)` — [subgroup()](https://docs.python.org/3/library/exceptions.html#BaseExceptionGroup.subgroup)

Returns a new group containing only exceptions that match `condition`, or `None` if nothing matches. Preserves nesting, `message`, traceback, cause, context, and notes. Since 3.13, `condition` may be any **callable** (not a type) taking one exception and returning a bool.

```python
# Goal: subgroup filters by exception type
root = ExceptionGroup("root", [ValueError(1), TypeError(2), ValueError(3)])
val_subgroup = root.subgroup(ValueError)
assert val_subgroup is not None
assert len(val_subgroup.exceptions) == 2
assert root.subgroup(KeyboardInterrupt) is None
```

```python
# Goal: callable condition (3.13+) filters by custom predicate
eg = ExceptionGroup("nums", [ValueError(1), ValueError(10), TypeError(2)])
evens = eg.subgroup(lambda exc: isinstance(exc, ValueError) and exc.args[0] % 2 == 0)
assert len(evens.exceptions) == 1
assert evens.exceptions[0].args[0] == 10
```

---

## `split(condition)` — [split()](https://docs.python.org/3/library/exceptions.html#BaseExceptionGroup.split)

Returns `(match, rest)` where `match` is `subgroup(condition)` and `rest` holds everything else. Metadata (`__traceback__`, `__cause__`, `__context__`, `__notes__`) is copied to both halves.

```python
# Goal: split partitions a group into matching and non-matching parts
eg = ExceptionGroup("pair", [ValueError(1), TypeError(2)])
match, rest = eg.split(ValueError)
assert len(match.exceptions) == 1
assert isinstance(match.exceptions[0], ValueError)
assert len(rest.exceptions) == 1
assert isinstance(rest.exceptions[0], TypeError)
assert eg.__traceback__ is match.__traceback__ is rest.__traceback__
```

---

## `derive(excs)` — [derive()](https://docs.python.org/3/library/exceptions.html#BaseExceptionGroup.derive) {#deriveexcs--derive}

Builds a new group with the same `message` but a different `excs` sequence. `subgroup()` and `split()` call `derive()` internally. Override `derive()` on **subclasses** so those methods return your type instead of plain `ExceptionGroup`.

```python
# Goal: custom derive keeps subgroup/split on the subclass
class MyGroup(ExceptionGroup):
    def derive(self, excs):
        return MyGroup(self.message, excs)

original = MyGroup("eg", [ValueError(1), TypeError(2)])
match, rest = original.split(ValueError)
assert type(match) is MyGroup
assert type(rest) is MyGroup
assert match.exceptions[0].args[0] == 1
```

---

## Subclassing patterns — [Exception groups](https://docs.python.org/3/library/exceptions.html#exception-groups)

`BaseExceptionGroup` defines `__new__()`, not a rich `__init__()`. Custom constructor signatures should override `__new__` and return the instance from there. Always override `derive()` when `subgroup()` / `split()` must preserve your class.

```python
# Goal: custom __new__ + derive preserve extra fields through split
class Errors(ExceptionGroup):
    def __new__(cls, errors, exit_code):
        self = super().__new__(cls, f"exit code: {exit_code}", errors)
        self.exit_code = exit_code
        return self

    def derive(self, excs):
        return Errors(excs, self.exit_code)

err = Errors([ValueError(1), TypeError(2)], 42)
half, _ = err.split(ValueError)
assert half.exit_code == 42
assert "42" in half.message
```

Any subclass of `BaseExceptionGroup` that is **also** a subclass of `Exception` (including `ExceptionGroup` itself) may only wrap `Exception` instances—same rule as the built-in `ExceptionGroup` constructor.

---

## Asyncio and `TaskGroup` (3.11+)

[`asyncio.TaskGroup`](https://docs.python.org/3/library/asyncio-task.html#task-groups) collects failures from concurrent tasks and raises a single `ExceptionGroup` when the block exits. Use `except*` to handle each failure type without losing the others.

```python
# Goal: TaskGroup failures surface as ExceptionGroup; except* handles each type
import asyncio

async def fail_with(exc):
    raise exc

async def run_task_group():
    handled = []
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fail_with(ValueError(1)))
            tg.create_task(fail_with(KeyError(2)))
    except* ValueError as eg:
        handled.append(("ValueError", len(eg.exceptions)))
    except* KeyError as eg:
        handled.append(("KeyError", len(eg.exceptions)))
    return handled

result = asyncio.run(run_task_group())
assert result == [("ValueError", 1), ("KeyError", 1)]
```

---

## Related reading

- [`except*`](https://docs.python.org/3/reference/compound_stmts.html#except-star) — language reference for star handlers
- [Exception context](../exception-context/index.md) — chaining with `__cause__` / `__context__` on group members
- [Base classes](../base-classes/index.md) — `BaseException` vs `Exception` catch semantics

---

## Sections in this repo

| Exception | Notes |
|-----------|-------|
| [ExceptionGroup](exceptiongroup/index.md) | Wraps only `Exception` subclasses; caught by `except Exception`; used by `asyncio.TaskGroup`. |
| [BaseExceptionGroup](baseexceptiongroup/index.md) | Wraps any `BaseException`; auto-upgrades to `ExceptionGroup` when all members are `Exception` instances. |
