# [anext()](https://docs.python.org/3/library/functions.html#anext)

## Description

`anext()` is the async variant of `next()`. When awaited, it returns the next item from an asynchronous iterator, or a provided default when the iterator is exhausted (Python 3.10+).

## What problem it solves

Sometimes you cannot use `async for`—custom scheduling, peek-ahead, merging streams, or wrapping async iterators in library code. `anext()` lets you pull items one at a time while staying in async/await style.

## Implementation options

### Stepping through with a default

```python
import asyncio

async def count_to_two():
    yield 1
    yield 2

async def main():
    it = aiter(count_to_two())
    assert await anext(it) == 1
    assert await anext(it) == 2
    assert await anext(it, "done") == "done"

asyncio.run(main())
```

### Handling exhaustion with `StopAsyncIteration`

```python
import asyncio

async def once():
    yield "only"

async def main():
    it = aiter(once())
    assert await anext(it) == "only"
    try:
        await anext(it)
        raise AssertionError("expected StopAsyncIteration")
    except StopAsyncIteration:
        pass

asyncio.run(main())
```

## Best practices

- Pass a default to avoid catching `StopAsyncIteration` when exhaustion is expected.
- Always obtain the iterator with `aiter()` (or `__aiter__()`) before calling `anext()`.
- Do not mix sync `next()` with async iterators—it will not await underlying coroutines.
