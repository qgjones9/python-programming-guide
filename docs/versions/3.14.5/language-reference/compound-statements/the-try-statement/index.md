# [The try statement](https://docs.python.org/3/reference/compound_stmts.html#the-try-statement)

The **`try` statement** groups statements under **exception handlers** (`except` or `except*`), an optional **`else`** (runs if no exception in `try`), and optional **`finally`** (always runs on the way out). Matching rules, `sys.exception()`, and exception-group splitting are specified on [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#the-try-statement). See also [Exceptions](../../execution-model/exceptions/index.md) and [The raise statement](../../simple-statements/the-raise-statement/index.md).

Parent: [Compound statements](../index.md)

---

## Clause roles

| Clause | When it runs |
|--------|----------------|
| `try` suite | First; exceptions propagate unless handled |
| `except [type] [as name]` | On matching exception in `try` (bare `except:` last, matches any) |
| `except* type [as name]` | On `BaseExceptionGroup`; splits subgroups (not mixable with `except` in same `try`) |
| `else` | After successful `try` (no exception, no `return`/`break`/`continue` from `try`) |
| `finally` | Always; may suppress or replace pending exceptions |

**Changed in 3.14:** multiple exception types in one `except` may omit grouping parentheses when `as` is absent (PEP 758).

---

## Handler matching (summary)

| Rule | Detail |
|------|--------|
| Expression `except` types | Class or tuple of classes; match via `isinstance` |
| Exception in handler header | Cancels search; new exception propagates |
| `as target` binding | Cleared at end of `except` block (avoids reference cycles) |
| `except*` | Mandatory type; `except*:` is a syntax error |

---

## Best practices

| Practice | Why |
|----------|-----|
| Catch specific exceptions | Bare `except:` hides bugs and KeyboardInterrupt |
| Use `else` for code that should not run if `try` failed | Keeps happy path out of handlers |
| Put cleanup in `finally` | Runs even when returning or re-raising |
| Use `except*` only for intentional `ExceptionGroup` handling | Ordinary exceptions are wrapped in a one-item group |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `return` in `finally` | Overrides value from `try`/`except` | Avoid (SyntaxWarning in 3.14+) |
| Relying on `e` after `except E as e` | Name deleted at block end | Bind to another name inside the block |
| `else` with exceptions | Not handled by preceding `except` | Put guarded code in `try` or separate handler |
| Empty `except*` subgroup | Propagates merged group | Handle or re-raise explicitly |

```python
# Goal: else runs only when try completes without exception
def parse_positive(text):
    try:
        n = int(text)
    except ValueError:
        return "bad"
    else:
        return "ok" if n > 0 else "nonpositive"


assert parse_positive("42") == "ok"
assert parse_positive("x") == "bad"
```

```python
# Goal: finally runs before exception propagates
log = []

def probe():
    try:
        log.append("try")
        raise RuntimeError("boom")
    finally:
        log.append("finally")


try:
    probe()
except RuntimeError:
    pass
assert log == ["try", "finally"]
```

```python
# Goal: except* splits ExceptionGroup (3.11+)
def handle_group():
    outcome = None
    try:
        raise ExceptionGroup("eg", [TypeError(2)])
    except* TypeError as eg:
        assert len(eg.exceptions) == 1
        outcome = "caught-type"
    return outcome


assert handle_group() == "caught-type"
```
