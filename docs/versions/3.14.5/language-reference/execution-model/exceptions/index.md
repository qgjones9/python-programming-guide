# [4.3. Exceptions](https://docs.python.org/3/reference/executionmodel.html#exceptions)

**Exceptions** break out of the normal control flow when errors or other exceptional conditions occur. They may be raised by the interpreter (runtime errors) or explicitly with `raise`. Handlers use `try` / `except` / `finally`; cleanup in `finally` runs whether or not an exception was handled. Python uses a **termination** model: handlers cannot repair the original failure and resume mid-operation—they continue at an outer level or re-enter from the top. Canonical text: [Exceptions](https://docs.python.org/3/reference/executionmodel.html#exceptions).

Parent: [4. Execution model](../index.md) · Statement syntax: [The try statement](../../compound-statements/the-try-statement/index.md), [The raise statement](../../simple-statements/the-raise-statement/index.md)

---

## Control flow model

| Concept | Behavior |
|---------|----------|
| **Raise point** | Exception originates where the error is detected |
| **Propagation** | Unwinds through callers until a matching handler or top level |
| **Handler match** | `except` type must be the exception’s class or a **non-virtual** base |
| **Instance payload** | Handler can bind `as name` to receive the exception object |
| **Unhandled** | Interpreter exits (script) or prints traceback (interactive); `SystemExit` is special |
| **Messages** | `str(exc)` is **not** a stable API across versions |

```python
# Goal: except catches by type; as binds the instance
class MyError(Exception):
    pass

caught = None
try:
    raise MyError("detail")
except MyError as exc:
    caught = (type(exc).__name__, str(exc))

assert caught == ("MyError", "detail")
```

```python
# Goal: base class in except matches subclass instance
try:
    raise ValueError("bad value")
except Exception as exc:
    label = type(exc).__name__

assert label == "ValueError"
```

---

## try / except / finally

| Clause | Role |
|--------|------|
| `try` suite | Normal body where exceptions may originate |
| `except` | Handles matching exceptions; execution continues after the `try` block |
| `else` | Runs if no exception (not covered in execution-model chapter, but common) |
| `finally` | Always runs; does not swallow exceptions unless combined with `return` / bare `except` pitfalls |

```python
# Goal: finally runs even when except handles the error
events = []
try:
    events.append("try")
    raise RuntimeError
except RuntimeError:
    events.append("except")
finally:
    events.append("finally")

assert events == ["try", "except", "finally"]
```

```python
# Goal: explicit raise with exception chaining context
def low():
    raise ValueError("low")

def high():
    try:
        low()
    except ValueError as err:
        raise TypeError("high") from err

chain = None
try:
    high()
except TypeError as exc:
    chain = (exc.__cause__.__class__.__name__, str(exc))

assert chain == ("ValueError", "high")
```

---

## Termination model (not resumption)

Handlers may log, convert, or abort, but they **cannot** jump back into the failing line and retry as if the error never happened (contrast with some “resumption” systems). Recovery means continuing **after** the `try` block or re-invoking code from the beginning.

```python
# Goal: handler continues after try; failing line is not retried automatically
attempts = []

def fragile():
    attempts.append("run")
    if len(attempts) == 1:
        raise OSError("transient")
    return "ok"

result = None
try:
    result = fragile()
except OSError:
    result = fragile()  # explicit re-call from caller, not automatic retry

assert attempts == ["run", "run"] and result == "ok"
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Bare `except:` or `except Exception:` | Catches `KeyboardInterrupt`, `SystemExit` unintentionally | Catch specific types |
| Relying on `str(exc)` in tests | Breaks across Python versions | Assert `type(exc)` and public attributes |
| `finally` + `return` | Suppresses exception or return value surprises | Keep `finally` for cleanup only |
| Re-raising without `from` | Loses explicit exception chain | Use `raise New() from old` when wrapping |
| Assuming handler “fixes” internal state | Partial mutations may remain | Use context managers or redo idempotent steps |
