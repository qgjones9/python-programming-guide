# [The with statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)

The **`with` statement** wraps a suite with a **context manager**: evaluate the context expression, call **`__enter__()`**, run the suite, then call **`__exit__(type, value, tb)`** — passing exception info if the suite failed, or three `None`s otherwise. If `__exit__` returns a true value, the exception is **suppressed**. Semantics match the desugaring in [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement); see [context manager types](https://docs.python.org/3/library/stdtypes.html#context-manager-types).

Parent: [Compound statements](../index.md)

---

## Forms and evaluation

| Form | Behavior |
|------|----------|
| `with expr as target:` | `target` receives `__enter__()` result (may be omitted) |
| Multiple items | Equivalent to nested `with` (left to right) |
| Parenthesized items (3.10+) | Multi-line `with (A(), B()):` |

`__enter__` / `__exit__` use **implicit special method lookup** (not plain attribute access on arbitrary proxies).

---

## Best practices

| Practice | Why |
|----------|-----|
| Use `with` for files, locks, and temporary state | Documents guaranteed cleanup |
| Prefer `contextlib.contextmanager` for simple setup/teardown | Less boilerplate than a full class |
| Order managers from outermost dependency to innermost | Matches nested resource ownership |
| Do not rely on `__exit__` seeing exceptions you swallow in the suite | `__exit__` still runs |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Returning `True` from `__exit__` unintentionally | Swallows exceptions | Return `None` or `False` unless suppressing is intended |
| Assuming `as` binds the manager | Binds **enter** result, not the manager object | Use `with mgr as x` vs separate variable |
| Exception during `__enter__` | `__exit__` is not called (3.x guarantee applies after successful enter) | Handle enter failures outside `with` |
| Mixing sync `with` in async code | Blocks event loop | Use `async with` ([Coroutines](../coroutines/index.md)) |

```python
# Goal: __exit__ runs even when suite raises
class Trace:
    def __init__(self, log):
        self.log = log

    def __enter__(self):
        self.log.append("enter")
        return self

    def __exit__(self, exc_type, exc, tb):
        self.log.append("exit")
        return False  # do not suppress


log = []
try:
    with Trace(log):
        log.append("body")
        raise ValueError("fail")
except ValueError:
    pass
assert log == ["enter", "body", "exit"]
```

```python
# Goal: suppress exception when __exit__ returns True
class Swallow:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return True


out = "ok"
with Swallow():
    raise RuntimeError("hidden")
    out = "skipped"
assert out == "ok"
```

```python
# Goal: multiple context managers nest like two with statements
closed = []

class Res:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        return self

    def __exit__(self, *args):
        closed.append(self.name)


with Res("a") as _, Res("b") as _:
    pass
assert closed == ["b", "a"]
```
