# [contextvars — Context Variables](https://docs.python.org/3/library/contextvars.html)

The [`contextvars`](https://docs.python.org/3/library/contextvars.html) module manages **context-local state** — values visible along the current logical call chain without explicit parameter threading. It replaces many uses of [`threading.local()`](../threading-thread-based-parallelism/index.md) in **asyncio** and other concurrent frameworks because context propagates per **Task**, not per OS thread. Added in 3.7 ([PEP 567](https://peps.python.org/pep-0567/)). Full API: [docs.python.org](https://docs.python.org/3/library/contextvars.html).

---

## Core types

| Name | Role |
|------|------|
| `ContextVar(name, *, default=...)` | Declare a named variable; create at **module level**, not in closures |
| `Token` | Returned by `set()`; pass to `reset()` or use as context manager (3.14+) |
| `Context` | Mapping of vars → values; enter with `run()` |
| `copy_context()` | Snapshot current context (O(1) in number of vars) |

```python
# Goal: set, read, and reset a ContextVar
import contextvars

request_id = contextvars.ContextVar("request_id", default="none")

assert request_id.get() == "none"
token = request_id.set("abc-123")
assert request_id.get() == "abc-123"
request_id.reset(token)
assert request_id.get() == "none"
```

```python
# Goal: scoped set via token (context manager on 3.14+)
import contextvars
import sys

user = contextvars.ContextVar("user", default="guest")

if sys.version_info >= (3, 14):
    with user.set("alice"):
        assert user.get() == "alice"
else:
    token = user.set("alice")
    try:
        assert user.get() == "alice"
    finally:
        user.reset(token)
assert user.get() == "guest"
```

---

## Manual context management — [Manual Context Management](https://docs.python.org/3/library/contextvars.html#manual-context-management)

`ctx.run(callable, *args, **kwargs)` **enters** `ctx` on the current thread’s context stack, runs the callable, then **exits** — reverting `ContextVar` changes made inside.

```python
# Goal: isolated changes inside copy_context().run()
import contextvars

var = contextvars.ContextVar("var", default=0)

def inner():
    var.set(99)
    return var.get()

ctx = contextvars.copy_context()
assert ctx.run(inner) == 99
assert var.get() == 0  # outer context unchanged
```

Each thread maintains its own **stack** of `Context` objects; entering the same `Context` twice (even from another thread) raises `RuntimeError`.

---

## asyncio — [asyncio support](https://docs.python.org/3/library/contextvars.html#asyncio-support)

Context variables **copy into new Tasks** automatically. Set a var at the start of a request handler; downstream coroutines call `get()` without threading the value through every `await`.

```python
# Goal: ContextVar visible in nested async function
import asyncio
import contextvars

client = contextvars.ContextVar("client")

async def render():
    return f"hello {client.get()}"

async def handler():
    client.set("127.0.0.1:8080")
    return await render()

async def main():
    return await handler()

assert asyncio.run(main()) == "hello 127.0.0.1:8080"
```

---

## vs `threading.local()`

| Aspect | `contextvars` | `threading.local()` |
|--------|---------------|---------------------|
| asyncio Tasks on one thread | Separate contexts per task | One value per thread |
| Libraries with hidden state | Preferred (PEP 567) | Can leak across tasks |
| Thread pool worker | New thread = new local | Context copy not automatic |

---

## Best practices

| Practice | Why |
|----------|-----|
| Define `ContextVar` at **module scope** | `Context` holds strong refs; closure vars confuse GC |
| **`reset(token)`** after `set()` in `finally` | Avoid leaking values on exceptions |
| Use **`copy_context()`** to run callbacks in a clean context | Framework integration pattern |

---

## See also

- [threading](../threading-thread-based-parallelism/index.md) — `local()` for thread-only state
- [asyncio](https://docs.python.org/3/library/asyncio.html) — task-local propagation
