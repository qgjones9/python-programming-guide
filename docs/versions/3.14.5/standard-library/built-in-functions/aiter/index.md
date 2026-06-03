# [aiter()](https://docs.python.org/3/library/functions.html#aiter)

## Description

`aiter()` returns an asynchronous iterator for an async iterable. It is equivalent to calling `async_iterable.__aiter__()` and was added in Python 3.10 as the async counterpart to `iter()`.

## What problem it solves

Async code consumes data from coroutine-based generators and other async iterables. `aiter()` gives you the iterator object explicitly—useful when you want symmetry with `iter()`, need to pass the iterator around, or pair it with `anext()` in manual async loops.

## Implementation options

### Manual async iteration with `anext()`

```python
import asyncio

async def ticker():
    for n in range(3):
        yield n

async def main():
    it = aiter(ticker())
    assert await anext(it) == 0
    assert await anext(it) == 1
    assert await anext(it) == 2

asyncio.run(main())
```

### Equivalent to `async for` (explicit iterator)

```python
import asyncio

async def collect(async_iterable):
    it = aiter(async_iterable)
    items = []
    while True:
        try:
            items.append(await anext(it))
        except StopAsyncIteration:
            break
    return items

async def gen():
    yield "a"
    yield "b"

assert asyncio.run(collect(gen())) == ["a", "b"]
```

## Best practices

- Unlike `iter()`, `aiter()` has no two-argument form—there is no async sentinel default.

  ```python
  # This will error! There is no sentinel variant:
  # it = aiter(async_iterable, sentinel)
  ```

- Prefer `async for` in application code; use `aiter()` when you need low-level control or to build your own async iteration tools.

  ```python
  async def use_async_for(async_iterable):
      # idiomatic way, handles StopAsyncIteration for you
      async for item in async_iterable:
          print(item)
  ```

  ```python
  async def manual_iteration(async_iterable):
      # explicit iterator, rare in application code:
      it = aiter(async_iterable)
      while True:
          try:
              item = await anext(it)
              print(item)
          except StopAsyncIteration:
              break
  ```

- Always `await` results from `anext()`; plain `next()` does not work on async iterators.

  ```python
  import asyncio

  async def gen():
      yield 1

  async def main():
      it = aiter(gen())
      item = await anext(it)  # correct
      assert item == 1
      # Incorrect: next(it)  # TypeError

  asyncio.run(main())
  ```