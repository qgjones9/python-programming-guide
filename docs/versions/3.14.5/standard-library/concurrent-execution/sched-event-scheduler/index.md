# [sched — Event scheduler](https://docs.python.org/3/library/sched.html)

The [`sched`](https://docs.python.org/3/library/sched.html) module implements a **general-purpose event scheduler**: register callbacks at absolute or relative times, then `run()` dispatches them in **priority order** when their time arrives. It is **single-threaded** by default but safe to use from multiple threads (3.3+); `delayfunc(0)` yields after each event. Full API: [docs.python.org](https://docs.python.org/3/library/sched.html).

---

## `scheduler` constructor

| Parameter | Default | Role |
|-----------|---------|------|
| `timefunc` | `time.monotonic` (3.3+) | Current time (any numeric units) |
| `delayfunc` | `time.sleep` | Wait until next event |

Use **`time.monotonic`** for relative scheduling to avoid clock skew; use **`time.time`** when you need wall-clock `enterabs` times.

---

## Scheduling events

| Method | When it runs |
|--------|----------------|
| `enter(delay, priority, action, argument=(), kwargs={})` | `timefunc() + delay` |
| `enterabs(time, priority, action, ...)` | At absolute `time` |
| `cancel(event)` | Remove pending event |
| `run(blocking=True)` | Execute due events; wait between them if blocking |

**Lower priority number = runs first** among events at the same time.

```python
# Goal: run events in priority order at the same deadline
import sched
import time

events = []
s = sched.scheduler(time.monotonic, lambda _: None)  # no real sleep

def record(label):
    events.append(label)

now = time.monotonic()
s.enterabs(now, 2, record, argument=("low",))
s.enterabs(now, 1, record, argument=("high",))
s.run(blocking=False)
assert events == ["high", "low"]
```

```python
# Goal: relative enter — later delay runs after earlier
import sched
import time

log = []
s = sched.scheduler(time.monotonic, lambda _: None)

def mark(x):
    log.append(x)

t0 = time.monotonic()
s.enter(0, 1, mark, argument=("a",))
s.enter(0, 1, mark, argument=("b",))
s.run(blocking=False)
assert log == ["a", "b"]
```

---

## Attributes and non-blocking run

- **`scheduler.queue`**: read-only list of upcoming `namedtuple` events (`time`, `priority`, `action`, `argument`, `kwargs`).
- **`run(blocking=False)`**: runs all events with `time <= timefunc()` immediately; returns delay until next event or `None` if empty.

If handlers run longer than the gap to the next event, the scheduler **falls behind** — no events are dropped.

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`asyncio`** for many timed I/O tasks | Built-in loop integration |
| Use **`sched`** for simple scripted timers in sync code | Minimal dependencies |
| Call **`cancel`** on obsolete events | Avoid stale callbacks |
| Keep actions **short** | Long handlers delay subsequent events |

---

## See also

- [threading](../threading-thread-based-parallelism/index.md) — `delayfunc(0)` cooperates with other threads
- [asyncio](https://docs.python.org/3/library/asyncio.html) — event-loop scheduling
- [time](../../numeric-and-mathematical-modules/time/index.md) — `monotonic`, `sleep`
