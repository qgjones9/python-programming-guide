# [StopAsyncIteration](https://docs.python.org/3/library/exceptions.html#StopAsyncIteration)

Must be raised by an asynchronous iterator's `__anext__()` to **stop async iteration**. Added in Python 3.5 ([docs.python.org](https://docs.python.org/3/library/exceptions.html#StopAsyncIteration)).

---

## When it is raised

| Context | Notes |
|---------|-------|
| `async for` over exhausted async iterator | Normal control flow |
| Manual `await anext()` | Propagates to caller |

Analogous to [`StopIteration`](stopiteration/index.md) for synchronous iterators.

---

## Demonstrating raise and catch

```python
import asyncio

# Goal: async for stops via StopAsyncIteration
class OneShot:
    def __aiter__(self):
        return self

    async def __anext__(self):
        if getattr(self, 'sent', False):
            raise StopAsyncIteration
        self.sent = True
        return 'only'

async def consume():
    results = []
    async for item in OneShot():
        results.append(item)
    return results

assert asyncio.run(consume()) == ['only']
assert issubclass(StopAsyncIteration, Exception)
```

---

## Best practices

- Never use `StopIteration` inside async iterators—always `StopAsyncIteration`.
- Related: [`StopIteration`](stopiteration/index.md).
