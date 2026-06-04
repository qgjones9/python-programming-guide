# [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)

[`asyncio`](https://docs.python.org/3/library/asyncio.html) runs **coroutines** on an **event loop** so I/O-bound work can overlap without threads. It underpins many async web stacks and client libraries. Full task, stream, subprocess, and synchronization APIs remain on [docs.python.org](https://docs.python.org/3/library/asyncio.html). **Not available on WASI.**

Related: [`socket`](socket-low-level-networking-interface/index.md) (loopback transports), [`selectors`](selectors-high-level-io-multiplexing/index.md) (blocking multiplexing alternative), [`signal`](signal-set-handlers-for-asynchronous-events/index.md) (loop signal handlers).

---

## High-level APIs — [High-level API Index](https://docs.python.org/3/library/asyncio.html#high-level-api-index)

| Area | Key entry points |
|------|------------------|
| Run coroutines | `asyncio.run(coro)`, `asyncio.create_task(coro)` |
| Sleep / timeouts | `asyncio.sleep()`, `asyncio.wait_for()` |
| TCP streams | `asyncio.open_connection()`, `asyncio.start_server()` |
| Synchronization | `asyncio.Lock`, `Queue`, `Event` |
| Subprocesses | `asyncio.create_subprocess_exec()` |

```python
# Goal: run a coroutine to completion with asyncio.run
import asyncio

async def main():
    await asyncio.sleep(0)
    return 42

assert asyncio.run(main()) == 42
```

```python
# Goal: schedule concurrent tasks on one loop
import asyncio

async def work(n):
    await asyncio.sleep(0)
    return n * 2

async def main():
    tasks = [asyncio.create_task(work(i)) for i in range(3)]
    return await asyncio.gather(*tasks)

assert asyncio.run(main()) == [0, 2, 4]
```

```python
# Goal: timeout a slow coroutine
import asyncio

async def slow():
    await asyncio.sleep(10)

async def main():
    try:
        await asyncio.wait_for(slow(), timeout=0.01)
    except asyncio.TimeoutError:
        return "timed out"
    return "ok"

assert asyncio.run(main()) == "timed out"
```

---

## Event loop — [Event Loop](https://docs.python.org/3/library/asyncio-eventloop.html)

| Concept | Detail |
|---------|--------|
| Default loop | `asyncio.run()` creates, runs, and closes a loop |
| `get_running_loop()` | Only valid inside a running coroutine/callback |
| `call_soon()` | Schedule a callback on the next iteration |
| Debug mode | `asyncio.run(..., debug=True)` helps trace slow callbacks |

```python
# Goal: schedule a callback from inside a coroutine
import asyncio

seen = []

async def main():
    loop = asyncio.get_running_loop()
    loop.call_soon(seen.append, "done")
    await asyncio.sleep(0)
    return seen

assert asyncio.run(main()) == ["done"]
```

---

## Streams — [Streams](https://docs.python.org/3/library/asyncio-stream.html)

`StreamReader` / `StreamWriter` pair with `open_connection` and `start_server` for buffered protocol I/O.

```python
# Goal: loopback StreamReader/Writer round-trip
import asyncio

async def echo_handler(reader, writer):
    data = await reader.read(100)
    writer.write(data)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo_handler, "127.0.0.1", 0)
    host, port = server.sockets[0].getsockname()[:2]
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(b"async")
    await writer.drain()
    reply = await reader.read(10)
    writer.close()
    await writer.wait_closed()
    server.close()
    await server.wait_closed()
    return reply

assert asyncio.run(main()) == b"async"
```

---

## Synchronization — [Synchronization Primitives](https://docs.python.org/3/library/asyncio-sync.html)

| Primitive | Use |
|-----------|-----|
| `Lock` | Mutual exclusion between coroutines |
| `Event` | One coroutine signals others |
| `Queue` | Producer/consumer with backpressure |
| `Semaphore` | Limit concurrent access |

```python
# Goal: asyncio.Lock serializes coroutine access
import asyncio

lock = asyncio.Lock()
counter = 0

async def inc():
    global counter
    async with lock:
        counter += 1

async def main():
    await asyncio.gather(*(inc() for _ in range(5)))
    return counter

assert asyncio.run(main()) == 5
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`asyncio.run()`** as the main entry | Replaces manual loop create/close for scripts |
| Never call **blocking** socket/file APIs in coroutines | Blocks the entire loop |
| Prefer **`asyncio.to_thread()`** for unavoidable blocking work | Offloads to a thread pool (3.9+) |
| Cancel tasks explicitly on shutdown | Avoids dangling callbacks |
| Read **Security considerations** for TLS in asyncio | Wrapper defaults differ from `ssl` module notes |

```python
# Goal: offload blocking work with to_thread (3.9+)
import asyncio

def blocking_add(a, b):
    return a + b

async def main():
    return await asyncio.to_thread(blocking_add, 3, 4)

assert asyncio.run(main()) == 7
```

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| `time.sleep()` inside coroutine | Use `await asyncio.sleep()` |
| Creating tasks without awaiting or retaining reference | Task may be garbage-collected mid-flight |
| Mixing threads and loop without `loop.call_soon_threadsafe` | Race on loop state |
| `asyncio.run()` inside `asyncio.run()` | Nested runs raise `RuntimeError` |

---

## REPL and debugging

Experiment interactively: `python -m asyncio` allows top-level `await`. Audit events are emitted on supported versions when running the REPL stdin path.

---

## See also

- [Conceptual overview of asyncio](https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html)
- Source tree: `Lib/asyncio/` on [github.com/python/cpython](https://github.com/python/cpython/tree/main/Lib/asyncio)
