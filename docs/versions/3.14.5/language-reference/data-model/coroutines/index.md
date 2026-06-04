# [3.4. Coroutines](https://docs.python.org/3/reference/datamodel.html#coroutines)

§3.4 defines the object protocols behind **`async`/`await`**: awaitable objects, native coroutines, asynchronous iterators, and asynchronous context managers. These types integrate with an event loop (for example [asyncio](https://docs.python.org/3/library/asyncio.html)); the language specifies the methods—scheduling policy belongs to the framework. See the [official section](https://docs.python.org/3/reference/datamodel.html#coroutines) and [PEP 492](https://peps.python.org/pep-0492/).

## Awaitable objects

An **awaitable** generally implements `__await__()`, which must return an **iterator**. Driving that iterator (via `await` or manual iteration) runs the coroutine body until it suspends or completes.

| Object kind | Awaitable? | Notes |
|-------------|------------|-------|
| Coroutine from `async def` | Yes | Primary native coroutine type |
| Objects with `__await__()` | Yes | e.g. some `asyncio.Future` implementations |
| Plain `object` | No | No `__await__` |
| Generator decorated with `@types.coroutine` | Yes (legacy) | Does not implement `__await__` directly |

```python
import asyncio


async def fetch():
    return 42


coro = fetch()
assert asyncio.iscoroutine(coro)
result = asyncio.run(coro)
assert result == 42
```

## Coroutine objects

Coroutine objects support **`send`**, **`throw`**, and **`close`**, analogous to generators. When execution finishes, the await-iterator raises **`StopIteration`** and the return value is in `StopIteration.value`. **Awaiting the same coroutine twice** raises `RuntimeError` (since 3.5.2).

```python
import asyncio


async def add_one(n):
    return n + 1


async def main():
    return await add_one(41)


assert asyncio.run(main()) == 42
```

Coroutines are **automatically closed** when garbage-collected if still suspended.

## Asynchronous iterators

Objects used in **`async for`** implement:

| Method | Contract |
|--------|----------|
| `__aiter__()` | Returns `self` or another async iterator (must not return a plain awaitable since 3.7) |
| `__anext__()` | Returns an awaitable yielding the next item; raises `StopAsyncIteration` when done |

```python
class Counter:
    def __init__(self, stop):
        self.stop = stop
        self.n = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.n >= self.stop:
            raise StopAsyncIteration
        self.n += 1
        return self.n


async def consume():
    total = 0
    async for value in Counter(3):
        total += value
    return total


import asyncio

assert asyncio.run(consume()) == 6
```

## Asynchronous context managers

Used with **`async with`**. Both hooks return **awaitables**:

| Method | Role |
|--------|------|
| `__aenter__(self)` | Setup; result bound to `as` target |
| `__aexit__(self, exc_type, exc, tb)` | Teardown; return value can suppress exceptions (like `__exit__`) |

```python
class AsyncResource:
    async def __aenter__(self):
        return "resource"

    async def __aexit__(self, exc_type, exc, tb):
        return False


async def use_resource():
    async with AsyncResource() as r:
        return r


import asyncio

assert asyncio.run(use_resource()) == "resource"
```

## Relationship to generators

| Feature | Generator (`yield`) | Coroutine (`async def`) |
|---------|---------------------|-------------------------|
| Iteration | `for` / `next()` | `await` / async frameworks |
| Return value | `StopIteration.value` | Same via await protocol |
| Methods | `send`, `throw`, `close` | Same family on coroutine objects |

Decorated legacy generator-coroutines exist for pre-3.5 code paths; new code should use **`async def`**.

## Best practices

| Practice | Why |
|----------|-----|
| Always `await` coroutines (or schedule them on a loop) | Bare coroutine objects warn (`RuntimeWarning`) and never run |
| Do not await the same coroutine twice | `RuntimeError` |
| Implement `__aiter__` returning `self` when appropriate | Required shape since 3.7 |
| Use `async with` for async setup/teardown | Mirrors sync `with` and guarantees `__aexit__` |
| Let the event loop close suspended coroutines | Or call `.close()` explicitly when abandoning work |

Parent: [3. Data model](../index.md)
