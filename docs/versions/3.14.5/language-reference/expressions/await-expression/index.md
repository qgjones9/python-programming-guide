# [6.4. Await expression](https://docs.python.org/3/reference/expressions.html#await-expression)

An **await expression** suspends a coroutine until an awaitable completes. Syntax:

```ebnf
await_expr: "await" primary
```

`await` may appear only inside a **coroutine function** (`async def`). It evaluates the primary (which must be awaitable), schedules it on the event loop, and resumes with the result.

```python
import asyncio


async def fetch_value():
    await asyncio.sleep(0)  # yield control; resume immediately
    return 42


async def main():
    result = await fetch_value()
    assert result == 42


asyncio.run(main())
```

Parent: [6. Expressions](../index.md)
