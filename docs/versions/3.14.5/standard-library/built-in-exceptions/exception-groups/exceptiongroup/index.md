# [ExceptionGroup](https://docs.python.org/3/library/exceptions.html#ExceptionGroup)

`ExceptionGroup` bundles multiple **application-level** failures—each member must be an [`Exception`](../../base-classes/exception/index.md) subclass—while still behaving like a normal exception in the hierarchy. Added in Python 3.11 (PEP 654), it is the type raised by [`asyncio.TaskGroup`](https://docs.python.org/3/library/asyncio-task.html#task-groups) and the target of most `except*` handlers. Canonical reference: [docs.python.org](https://docs.python.org/3/library/exceptions.html#ExceptionGroup).

---

## Role in the hierarchy

`ExceptionGroup` inherits from both `Exception` and [`BaseExceptionGroup`](../baseexceptiongroup/index.md). That dual inheritance is why:

- `except Exception` catches an `ExceptionGroup`.
- `except*` can split it by contained types.
- `isinstance(eg, BaseExceptionGroup)` is true for introspection and APIs that accept either group type.

```python
# Goal: ExceptionGroup is both Exception and BaseExceptionGroup
eg = ExceptionGroup("demo", [ValueError(1)])
assert isinstance(eg, Exception)
assert isinstance(eg, BaseExceptionGroup)
assert issubclass(ExceptionGroup, Exception)
assert issubclass(ExceptionGroup, BaseExceptionGroup)
```

---

## Constructor validation

`ExceptionGroup(msg, excs)` requires a string message and a sequence of exceptions. Unlike [`BaseExceptionGroup`](../baseexceptiongroup/index.md), it **raises `TypeError`** if any member is not an `Exception` subclass—there is no silent upgrade or downgrade.

```python
# Goal: non-Exception members are rejected at construction
rejected = False
try:
    ExceptionGroup("bad", [ValueError(1), KeyboardInterrupt()])
except TypeError:
    rejected = True
assert rejected
```

```python
# Goal: valid group stores members in exceptions tuple
eg = ExceptionGroup("validation", (TypeError("t"), ValueError("v")))
assert eg.message == "validation"
assert len(eg.exceptions) == 2
```

---

## Caught by `except Exception`

Broad handlers that should **not** catch `KeyboardInterrupt` or `SystemExit` will still catch `ExceptionGroup`, because it derives from `Exception`. Use `except*` when you need to react to **specific** member types instead of treating the whole bundle as one opaque error.

```python
# Goal: except Exception catches the whole group
def broad_handler():
    label = None
    try:
        raise ExceptionGroup("eg", [ValueError(1), TypeError(2)])
    except Exception as exc:
        label = type(exc).__name__
    return label

assert broad_handler() == "ExceptionGroup"
```

---

## Handling with `except*`

Each `except*` clause receives a **subgroup** containing only the matching exceptions. Handlers run in order; unhandled members propagate after the chain completes.

```python
# Goal: sequential except* clauses drain matching subgroups
def handle_batch():
    seen = []
    try:
        raise ExceptionGroup(
            "batch",
            [ValueError(1), TypeError(2), ValueError(3)],
        )
    except* ValueError as eg:
        seen.append(("ValueError", len(eg.exceptions)))
    except* TypeError as eg:
        seen.append(("TypeError", len(eg.exceptions)))
    return seen

assert handle_batch() == [("ValueError", 2), ("TypeError", 1)]
```

A single non-group exception that matches an `except*` type is wrapped in an `ExceptionGroup` with an empty message so the handler always receives a group-shaped target.

```python
# Goal: lone matching exception is wrapped for except*
def wrap_singleton():
    target = None
    try:
        raise ValueError("solo")
    except* ValueError as eg:
        target = eg
    assert target.message == ""
    assert len(target.exceptions) == 1
    assert isinstance(target.exceptions[0], ValueError)

wrap_singleton()
```

---

## `subgroup()`, `split()`, and `derive()`

These methods mirror [`BaseExceptionGroup`](../baseexceptiongroup/index.md) behavior. Override `derive()` on subclasses so splitting preserves your type (see [subclassing example](../index.md#deriveexcs--derive)).

```python
# Goal: split partitions members for manual handling
eg = ExceptionGroup("jobs", [OSError(1), OSError(2), RuntimeError(3)])
match, rest = eg.split(OSError)
assert len(match.exceptions) == 2
assert len(rest.exceptions) == 1
assert isinstance(rest.exceptions[0], RuntimeError)
```

---

## Asyncio `TaskGroup` integration

When any task started inside `asyncio.TaskGroup` fails, the context manager raises `ExceptionGroup` containing every task failure. Pair it with `except*` to log or recover per error type.

```python
# Goal: mirror TaskGroup-style fan-out without losing secondary errors
import asyncio

async def work(name, exc=None):
    if exc:
        raise exc
    return name

async def fan_out():
    results = {"handled": []}
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(work("ok"))
            tg.create_task(work("bad", ValueError("v")))
            tg.create_task(work("also bad", KeyError("k")))
    except* ValueError as eg:
        results["handled"].append(type(eg.exceptions[0]).__name__)
    except* KeyError as eg:
        results["handled"].append(type(eg.exceptions[0]).__name__)
    return results

out = asyncio.run(fan_out())
assert set(out["handled"]) == {"ValueError", "KeyError"}
```

---

## Nested exception groups

Groups may contain other groups. `subgroup()` preserves nesting and omits empty nested groups from the result.

```python
# Goal: nested groups stay nested when filtering
leaf = ExceptionGroup("leaf", [ValueError(1)])
nested = ExceptionGroup("nested", [leaf, TypeError(2)])
picked = nested.subgroup(ValueError)
assert len(picked.exceptions) == 1
assert isinstance(picked.exceptions[0], ExceptionGroup)
assert picked.exceptions[0].message == "leaf"
```

---

## Practical guidance

| Practice | Reason |
|----------|--------|
| Prefer `ExceptionGroup` for application errors | Safe with `except Exception`; clear intent |
| Use `except*` over manual `exceptions` iteration | Correct split/merge semantics and traceback handling |
| Override `derive()` on custom group subclasses | Keeps `subgroup()` / `split()` on your type |
| Pass `excs` as a tuple | Faster construction in CPython |

For `BaseExceptionGroup` (non-`Exception` members and auto-upgrade rules), see [BaseExceptionGroup](../baseexceptiongroup/index.md). For the full `except*` specification, see the [Exception groups overview](../index.md).
