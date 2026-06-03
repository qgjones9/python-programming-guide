# [MemoryError](https://docs.python.org/3/library/exceptions.html#MemoryError)

Raised when an operation runs out of memory but the situation **may still be rescued** by freeing objects. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#MemoryError). The interpreter may not fully recover, but it raises so a traceback can be printed.

---

## When it is raised

| Situation | Notes |
|-----------|-------|
| Huge allocation request | May fail before allocation completes |
| Container growth | Lists, dicts, etc. when RAM exhausted |
| Not ordinary big integers | Huge `int` math raises `MemoryError`, not `OverflowError` |

---

## Demonstrating raise and catch

```python
# Goal: MemoryError is catchable; message describes failure
caught = None
try:
    raise MemoryError('unable to allocate array')
except MemoryError as exc:
    caught = str(exc)
assert caught == 'unable to allocate array'
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| Free caches / large buffers | Recovery attempt at process boundary |
| `except MemoryError` | Degrade feature and notify user |
| Avoid catching in inner loops | Recovery is expensive and often fails again |

Related: [`OverflowError`](overflowerror/index.md) (fixed-width bounds, not heap exhaustion).

---

## Best practices

- Catch only at process boundaries; free caches or degrade functionality, then retry if safe.
- Do not catch in tight loops—recovery is expensive and may fail again.
- Related: [`OverflowError`](overflowerror/index.md) (fixed-width numeric bounds, not heap exhaustion).
