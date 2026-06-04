# [queue — A synchronized queue class](https://docs.python.org/3/library/queue.html)

The [`queue`](https://docs.python.org/3/library/queue.html) module provides **thread-safe FIFO, LIFO, and priority queues** for exchanging work between producer and consumer threads. Locks block competing threads; queues are **not re-entrant** within one thread. For multiprocessing IPC, use [`multiprocessing.Queue`](../multiprocessing-process-based-parallelism/index.md). Full method semantics: [docs.python.org](https://docs.python.org/3/library/queue.html).

---

## Queue types

| Class | Order | Notes |
|-------|-------|-------|
| `Queue` | FIFO | `maxsize=0` means unbounded |
| `LifoQueue` | Stack (LIFO) | Most recent item out first |
| `PriorityQueue` | Lowest priority first | Entries should be comparable (often `(priority, item)` tuples) |
| `SimpleQueue` | FIFO, unbounded | C-backed; re-entrant `put`/`get` in same thread (3.7+) |

Exceptions: `Empty`, `Full`, `ShutDown` (3.13+).

```python
# Goal: FIFO producer/consumer with task_done/join
import queue

q = queue.Queue()
results = []

def work(item):
    results.append(item * 2)
    q.task_done()

for i in range(3):
    q.put(i)

while not q.empty():
    item = q.get()
    work(item)

q.join()
assert sorted(results) == [0, 2, 4]
```

```python
# Goal: priority queue — lowest number dequeued first
import queue

pq = queue.PriorityQueue()
pq.put((2, "second"))
pq.put((1, "first"))
order = [pq.get()[1] for _ in range(2)]
assert order == ["first", "second"]
```

---

## Producer/consumer pattern — [Waiting for task completion](https://docs.python.org/3/library/queue.html#waiting-for-task-completion)

| Step | API |
|------|-----|
| Enqueue work | `put(item)` |
| Worker fetches | `item = get()` |
| Worker finishes | `task_done()` |
| Coordinator waits | `join()` blocks until unfinished count is zero |

Prefer **blocking** `get()` over `empty()` + `get()` — `empty()` is approximate under contention.

```python
# Goal: bounded queue blocks producers when full
import queue

bounded = queue.Queue(maxsize=2)
bounded.put(1)
bounded.put(2)
assert bounded.full()
bounded.get()
assert not bounded.full()
```

---

## Shutdown — [Terminating queues](https://docs.python.org/3/library/queue.html#terminating-queues)

`shutdown(immediate=False)` (3.13+): stops growth; `put` raises `ShutDown`; drain with `get` or use `immediate=True` to drop pending work (breaks `join()` invariants if misused).

---

## `SimpleQueue` vs `Queue`

| Feature | `Queue` | `SimpleQueue` |
|---------|---------|---------------|
| `task_done` / `join` | Yes | No |
| Bounded size | Yes | No (unbounded) |
| Re-entrant in one thread | No | Yes (CPython) |

Use `SimpleQueue` in destructors or weakref callbacks where re-entrancy matters.

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Non-comparable priority items | Wrap in `dataclasses.dataclass(order=True)` with `compare=False` on payload field |
| Daemon thread dies before `task_done` | Keep worker alive until queue drained or use non-daemon |
| `get_nowait` on empty queue | Catch `queue.Empty` |

---

## See also

- [threading](../threading-thread-based-parallelism/index.md) — worker threads
- [multiprocessing](../multiprocessing-process-based-parallelism/index.md) — `multiprocessing.Queue`
- [collections.deque](../../data-types/collections-container-datatypes/index.md) — fast unbounded deque without blocking semantics
