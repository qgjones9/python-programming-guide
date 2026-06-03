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

### Manual async loop mirroring `async for`

```python
import asyncio

async def stream():
    for ch in "ab":
        yield ch

async def collect():
    it = aiter(stream())
    out = []
    while True:
        item = await anext(it, None)
        if item is None:
            break
        out.append(item)
    return out

assert asyncio.run(collect()) == ["a", "b"]
```

## Best practices

- Pass a default to avoid catching `StopAsyncIteration` when exhaustion is expected.

  ```python
  import asyncio

  async def once():
      yield "only"

  async def main():
      it = aiter(once())
      assert await anext(it) == "only"
      assert await anext(it, None) is None  # clean sentinel

  asyncio.run(main())
  ```

- Always obtain the iterator with `aiter()` before calling `anext()`; calling `anext()` on the async iterable itself is wrong.

  ```python
  import asyncio

  async def gen():
      yield 1

  async def main():
      it = aiter(gen())  # correct: iterator object
      assert await anext(it) == 1

  asyncio.run(main())
  # Incorrect: await anext(gen())  # TypeError
  ```

- Do not mix sync `next()` with async iterators—it will not await underlying coroutines.

  ```python
  import asyncio

  async def gen():
      yield 1

  async def main():
      it = aiter(gen())
      # Correct:
      assert await anext(it) == 1
      # Incorrect: next(it)  # TypeError

  asyncio.run(main())
  ```
