# [gc — Garbage Collector interface](https://docs.python.org/3/library/gc.html)

The [`gc`](https://docs.python.org/3/library/gc.html) module controls CPython's **cycle-detecting garbage collector** for containers that participate in reference cycles (`dict`, `list`, custom classes, …). It complements reference counting, which handles acyclic objects immediately. Reference: [docs.python.org](https://docs.python.org/3/library/gc.html).

---

## Key functions

| API | Role |
|-----|------|
| `collect(generation=2)` | Run collection; returns number of unreachable objects collected |
| `get_count()` | Per-generation collection counts since start |
| `get_threshold()` / `set_threshold()` | Tune when automatic collections trigger |
| `get_objects()` | Snapshot of tracked objects (debug only) |
| `get_referrers(*objs)` | Objects referring to given objects (debug) |
| `isenabled()` / `enable()` / `disable()` | Toggle automatic collector |
| `set_debug(flags)` | Verbose leak diagnostics |

Generations 0, 1, 2 — young objects promoted when they survive collections.

---

## Example — manual collection

```python
# Goal: observe collector counters increase after collect
import gc

before = gc.get_count()
collected = gc.collect()
after = gc.get_count()
assert collected >= 0
assert isinstance(before, tuple) and len(before) == 3
assert isinstance(after, tuple)
```

---

## `gc.disable()` use cases

Disable during tight latency-sensitive sections where you know no cycles form, then re-enable. Long-running servers sometimes batch `collect()` during idle windows.

---

## Best practices

| Practice | Why |
|----------|-----|
| Fix cycles with **`weakref`** or explicit teardown | Collector is backup, not primary strategy |
| Avoid **`get_referrers` in production** | Expensive and confusing with implementation details |
| Use **`gc.set_debug(gc.DEBUG_LEAK)`** only in dev | Extremely verbose |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Relying on `__del__` in cyclic graphs | Order undefined; may never run before leak | Break cycles in `close()` |
| Assuming `collect()` frees everything immediately | Only cyclic unreachable graphs | Drop references explicitly |

---

## See also

- [`weakref`](https://docs.python.org/3/library/weakref.html) — callbacks without keeping objects alive
- [`sys`](../sys-system-specific-parameters-and-functions/index.md) — `getrefcount` for debugging refcount
