# [Coroutines](https://docs.python.org/3/reference/compound_stmts.html#coroutines)

**Coroutine functions** (`async def`) return coroutine objects when called; their bodies may use **`await`**, **`async for`**, and **`async with`** (only inside a coroutine function). **`async for`** drives asynchronous iterators (`__aiter__` / `__anext__`); **`async with`** uses `__aenter__` / `__aexit__`. Syntax and desugaring: [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#coroutines) (PEP 492).

Parent: [Compound statements](../index.md)

---

## Forms

| Statement | Requires |
|-----------|----------|
| `async def` | Always a coroutine function, even without `await` |
| `async for` | `__aiter__` returning object with `__anext__` → awaitable |
| `async with` | Async context manager (`__aenter__` / `__aexit__` awaitables) |

`yield from` inside `async def` is a **SyntaxError**. `await` and `async` are keywords since 3.7.

---

## Best practices

| Practice | Why |
|----------|-----|
| Run coroutines with `asyncio.run` (scripts) or a running loop | Calling coroutine without await warns / does nothing useful |
| Use `async with` for async locks and clients | Matches sync `with` cleanup guarantees |
| Prefer `asyncio.TaskGroup` / structured concurrency for fan-out | Clear cancellation boundaries (3.11+) |
| Do not call blocking I/O in coroutines | Starves the event loop |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Forgetting `await` | Coroutine never runs; RuntimeWarning | Always await or schedule tasks |
| `async for` / `async with` in plain `def` | SyntaxError | Only in `async def` |
| Mixing sync `with` around async resources | Blocks or protocol mismatch | Use `async with` |
| Reusing exhausted async iterator | Second loop sees nothing | Recreate or `aclosing` pattern |

```python
# Goal: async def and await drive coroutine to completion
import asyncio

async def double(x):
    await asyncio.sleep(0)
    return x * 2


async def main():
    return await double(21)


assert asyncio.run(main()) == 42
```

```python
# Goal: async for desugars to __aiter__ / __anext__
import asyncio

class CountDown:
    def __init__(self, start):
        self.n = start

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.n <= 0:
            raise StopAsyncIteration
        self.n -= 1
        await asyncio.sleep(0)
        return self.n + 1


async def collect():
    out = []
    async for v in CountDown(3):
        out.append(v)
    return out


assert asyncio.run(collect()) == [3, 2, 1]
```

```python
# Goal: async with calls __aenter__ / __aexit__
import asyncio

class AsyncTrace:
    def __init__(self, log):
        self.log = log

    async def __aenter__(self):
        self.log.append("enter")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.log.append("exit")
        return False


async def run():
    log = []
    async with AsyncTrace(log):
        log.append("body")
    return log


assert asyncio.run(run()) == ["enter", "body", "exit"]
```
