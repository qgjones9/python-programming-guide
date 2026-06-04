# [tracemalloc — Trace memory allocations](https://docs.python.org/3/library/tracemalloc.html)

`tracemalloc` tracks **Python memory allocations** with lightweight stack traces. Compare snapshots to find leaks, identify top allocators, and correlate usage with source lines. Canonical reference: [tracemalloc.html](https://docs.python.org/3/library/tracemalloc.html).

---

## Purpose

When memory grows unexpectedly, `tracemalloc` shows **where objects were allocated** (filename and line). It traces Python's object allocator—not every low-level `malloc` from C extensions unless they allocate Python objects.

---

## Key API

| Function | Role |
|----------|------|
| `start(nframes)` | Begin tracing (optional stack depth) |
| `stop()` | End tracing |
| `take_snapshot()` | Capture current allocation state |
| `Snapshot.compare_to(old, key_type)` | Diff two snapshots |
| `get_traced_memory()` | Current and peak traced bytes |
| `Statistical` display | `snapshot.statistics("lineno")` |

---

## Example — top allocation sites

```python
import tracemalloc

tracemalloc.start()
data = [bytearray(1024) for _ in range(100)]
snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics("lineno")[:3]
assert len(top) >= 1
assert top[0].size > 0
tracemalloc.stop()
```

---

## Example — compare snapshots for growth

```python
import tracemalloc

tracemalloc.start()
snapshot1 = tracemalloc.take_snapshot()
more = [object() for _ in range(1000)]
snapshot2 = tracemalloc.take_snapshot()
diff = snapshot2.compare_to(snapshot1, "lineno")
assert len(diff) > 0
tracemalloc.stop()
```

---

## Example — current and peak memory

```python
import tracemalloc

tracemalloc.start()
chunk = "x" * 10000
current, peak = tracemalloc.get_traced_memory()
assert current > 0
tracemalloc.stop()
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Start tracing **before** the suspect code | Misses allocations if started late |
| Limit stack depth (`start(5)`) | Reduces overhead |
| Compare snapshots at steady state | Filters one-time startup noise |
| Pair with [`gc`](https://docs.python.org/3/library/gc.html) for unreachable cycles | tracemalloc shows allocations, not GC reachability |

---

## See also

- [`faulthandler`](faulthandler-dump-the-python-traceback/index.md)
- [`resource`](https://docs.python.org/3/library/resource.html) — OS-level usage (Unix)
