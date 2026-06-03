# [BaseExceptionGroup](https://docs.python.org/3/library/exceptions.html#BaseExceptionGroup)

`BaseExceptionGroup` is the root type for **bundled exceptions** in Python 3.11+. It inherits directly from [`BaseException`](../../base-classes/baseexception/index.md), so it sits beside `SystemExit` and `KeyboardInterrupt` rather than under [`Exception`](../../base-classes/exception/index.md). Full API wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#BaseExceptionGroup); the notes below focus on construction rules, wrapping non-`Exception` types, and programmatic splitting.

---

## Role in the hierarchy

- Direct subclass of `BaseException` — **not** caught by `except Exception`.
- Parent class of [`ExceptionGroup`](../exceptiongroup/index.md), which adds the restriction that members must be `Exception` subclasses.
- Supports the same instance methods as `ExceptionGroup`: `subgroup()`, `split()`, and `derive()` (see the [parent page](../index.md)).

```python
# Goal: confirm hierarchy placement
assert issubclass(BaseExceptionGroup, BaseException)
assert not issubclass(BaseExceptionGroup, Exception)
assert issubclass(ExceptionGroup, BaseExceptionGroup)
assert issubclass(ExceptionGroup, Exception)
```

---

## Constructor and automatic upgrade

`BaseExceptionGroup(msg, excs)` requires a string `msg` and a sequence `excs`. If **every** element of `excs` is an `Exception` instance, the constructor returns an [`ExceptionGroup`](../exceptiongroup/index.md) instead of a `BaseExceptionGroup`—you do not need to pick the concrete type yourself.

```python
# Goal: all-Exception input yields ExceptionGroup from BaseExceptionGroup(...)
auto = BaseExceptionGroup("batch", (ValueError(1), RuntimeError(2)))
assert type(auto) is ExceptionGroup
assert isinstance(auto, BaseExceptionGroup)  # ExceptionGroup is a subclass
```

When at least one member is **not** an `Exception` subclass, you get a true `BaseExceptionGroup`:

```python
# Goal: mixing in BaseException keeps BaseExceptionGroup type
class Cancelled(BaseException):
    pass

group = BaseExceptionGroup("shutdown", (ValueError("save failed"), Cancelled()))
assert type(group) is BaseExceptionGroup
assert len(group.exceptions) == 2
```

Use a **tuple** for `excs` when possible; CPython processes tuples more efficiently than other sequences.

---

## Wrapping system-exiting exceptions

Because `BaseExceptionGroup` extends `BaseException`, it can bundle `KeyboardInterrupt`, `GeneratorExit`, or custom `BaseException` types that must not be swallowed by broad `except Exception` handlers.

```python
# Goal: BaseExceptionGroup is not caught by except Exception
def catches_exception_only():
    label = None
    try:
        raise BaseExceptionGroup(
            "fatal mix",
            (RuntimeError("logic bug"), KeyboardInterrupt()),
        )
    except Exception:
        label = "caught"
    except BaseExceptionGroup:
        label = "not caught"
    return label

assert catches_exception_only() == "not caught"
```

Handle such groups with `except BaseExceptionGroup`, targeted `except*`, or inspect `group.exceptions` and re-raise critical members.

---

## Attributes

| Attribute | Meaning |
|-----------|---------|
| `message` | Read-only copy of the constructor `msg` string. |
| `exceptions` | Read-only tuple of wrapped exceptions (may include nested groups). |

```python
# Goal: attributes mirror constructor inputs
msg = "parallel IO failures"
members = (OSError("disk"), OSError("network"))
group = BaseExceptionGroup(msg, members)
assert group.message == msg
assert group.exceptions == members
```

---

## Splitting and filtering

`subgroup()` and `split()` use the same matching rules as `except` / `except*`. Callable conditions (Python 3.13+) accept any predicate on individual exceptions.

```python
# Goal: subgroup extracts nested structure preserving message
inner = BaseExceptionGroup("inner", (ValueError(1),))
outer = BaseExceptionGroup("outer", (inner, TypeError(2)))
match = outer.subgroup(ValueError)
assert match is not None
assert match.message == "outer"
assert len(match.exceptions) == 1
assert isinstance(match.exceptions[0], BaseExceptionGroup)
```

```python
# Goal: split returns (match, rest) with shared traceback metadata
eg = BaseExceptionGroup("work", (ValueError(1), TypeError(2)))
try:
    raise eg
except BaseExceptionGroup as caught:
    match, rest = caught.split(TypeError)
    assert len(match.exceptions) == 1
    assert len(rest.exceptions) == 1
    assert caught.__traceback__ is match.__traceback__
```

---

## Subclassing `BaseExceptionGroup`

Override `__new__()` (not `__init__`) when the constructor signature differs from `(msg, excs)`. Override `derive()` so `subgroup()` / `split()` return your subclass. If your subclass also inherits from `Exception`, it may only wrap `Exception` instances—same constraint as [`ExceptionGroup`](../exceptiongroup/index.md).

```python
# Goal: derive preserves custom class through split
class TaggedGroup(BaseExceptionGroup):
    def __new__(cls, tag, excs):
        self = super().__new__(cls, f"[{tag}]", excs)
        self.tag = tag
        return self

    def derive(self, excs):
        return TaggedGroup(self.tag, excs)

# All Exception members → constructor returns ExceptionGroup subclass path;
# use Exception-only members for a clean TaggedGroup via BaseExceptionGroup:
class TaggedErrors(ExceptionGroup):
    def __new__(cls, tag, excs):
        self = super().__new__(cls, f"[{tag}]", excs)
        self.tag = tag
        return self

    def derive(self, excs):
        return TaggedErrors(self.tag, excs)

tg = TaggedErrors("api", [ValueError(1), TypeError(2)])
part, _ = tg.split(ValueError)
assert part.tag == "api"
assert part.message == "[api]"
```

---

## When to use `BaseExceptionGroup` vs `ExceptionGroup`

| Situation | Prefer |
|-----------|--------|
| All failures are `Exception` subclasses | `ExceptionGroup` or `BaseExceptionGroup` (auto-upgrades) |
| Mix includes `KeyboardInterrupt`, `GeneratorExit`, etc. | `BaseExceptionGroup` |
| Handler uses `except Exception` | `ExceptionGroup` only |
| Library models ordinary application errors | [`ExceptionGroup`](../exceptiongroup/index.md) |

See the [Exception groups overview](../index.md) for `except*`, asyncio `TaskGroup`, and end-to-end handling patterns.
