# [Thread safety for dict objects](https://docs.python.org/3/library/threadsafety.html#thread-safety-for-dict-objects)

Built-in **`dict`** objects have documented thread-safety guarantees in Python’s **free-threaded** build (GIL disabled). With the **GIL enabled**, dict access is largely serialized by the interpreter, but logical races remain possible at the Python level. Full specification remains on [docs.python.org](https://docs.python.org/3/library/threadsafety.html#thread-safety-for-dict-objects); this page maps operations to locking behavior and TOCTOU fixes.

See [Thread safety levels](../thread-safety-levels/index.md) for terminology. Related: [Thread safety for list objects](../thread-safety-for-list-objects/index.md), [Thread safety for set objects](../thread-safety-for-set-objects/index.md), and [`Mapping Types — dict`](../../built-in-types/mapping-types-dict/index.md).

---

## Scope: free-threaded vs GIL-enabled builds

| Build | What you can assume |
|-------|---------------------|
| **GIL enabled** | Structural corruption from concurrent dict use is uncommon, but check-then-act bugs and stale reads still occur in multi-threaded programs. |
| **Free-threaded** | Lock-free reads and per-object-lock writes documented here are the authoritative guarantees. |

Atomic **construction** (no concurrent visibility of half-built dicts):

| Constructor | Atomic when argument is |
|-------------|-------------------------|
| `dict(...)` | Another **`dict`** or a **`tuple`** of pairs |
| `dict.fromkeys(iterable)` | Iterable is exactly **`dict`**, **`set`**, or **`frozenset`** (not subclasses) |

---

## Lock-free and atomic reads

These operations **do not** acquire the per-object lock. They cannot corrupt the dict; concurrent writers may still change results between your operations.

| Operation | Behavior |
|-----------|----------|
| `d[key]` (read) | Atomic read of one value slot |
| `d.get(key)` | Atomic read; no `KeyError` |
| `key in d` / `key not in d` | Atomic membership test |
| `len(d)` | Atomic size read |

Lock-free reads **do not block** operations that hold the per-object lock. Writers using the lock will not be stalled by readers, and readers may observe values that change immediately afterward.

---

## Per-object lock: single-item writes (corruption-safe)

These operations hold the dict’s lock for the mutation. They **will not corrupt** the dictionary structure.

| Operation | Notes |
|-----------|-------|
| `d[key] = value` | Single insert or update |
| `del d[key]` | Single delete |
| `d.pop(key)` / `d.pop(key, default)` | Remove and return |
| `d.popitem()` | Remove LIFO pair |
| `d.setdefault(key, default)` | Insert-if-missing |

### `__eq__()` during key comparison

Writes that compare keys (`pop`, `setdefault`, etc.) may call **`__eq__`** on custom key types. For built-in keys (`str`, `int`, `float`, …) comparison runs in C **without releasing** the dict lock. For arbitrary Python classes, the lock **may be released** during `__eq__`, allowing concurrent modification.

---

## Copy, views, merge, and clear

| Operation | Locking | Atomic appearance |
|-----------|---------|-------------------|
| `d.copy()` | Holds lock for full shallow copy | Yes — snapshot consistent |
| `d.keys()` / `d.values()` / `d.items()` | Lock held while view object is created | View reflects dict at creation time; view updates live afterward |
| `d \| other` | Both operands locked (`dict` only for `\|`) | New dict; atomic |
| `d.clear()` | Lock held entire operation | Other threads cannot see gradual emptying |

### `update()`, `|=`, and `==` — locking both operands

When the **other** operand is a standard **`dict`** (using the built-in iterator, not a subclass override), **both** dicts are locked:

| Operation | Both dicts locked when |
|-----------|------------------------|
| `d.update(other_dict)` | `other_dict` is a **`dict`** |
| `d \|= other_dict` | `other_dict` is a **`dict`** |
| `d == other_dict` | Either side is **`dict`** or subclass |

For **`d.update(iterable)`**, **`d |= iterable`**, or **`dict.fromkeys(iterable)`** where the iterable is **not** exactly `dict` / `set` / `frozenset`, only the **target** (or result) dict is locked—the iterable may be mutated concurrently by another thread.

Equality comparisons also compare **values** with **`__eq__`**, so locks may be released for non-built-in value types during `d == other`.

```python
left = {"a": 1, "b": 2}
right = {"b": 99, "c": 3}
merged = left | right
assert merged == {"a": 1, "b": 99, "c": 3}

target = {"x": 1}
target |= {"x": 2, "y": 3}
assert target == {"x": 2, "y": 3}
```

---

## NOT atomic (read-modify-write, TOCTOU, iteration)

| Anti-pattern | Problem |
|--------------|---------|
| `d[key] = d[key] + 1` | Separate read and write |
| `if key in d: del d[key]` | Key may disappear between test and delete (TOCTOU) |
| `if key in d: val = d[key]` | Value may change or key vanish before read |
| `for k, v in d.items(): ...` with concurrent writers | Skipped keys, `RuntimeError`, or inconsistent pairs |

---

## TOCTOU fixes

| Instead of | Use |
|------------|-----|
| `if key in d: del d[key]` | `d.pop(key, None)` |
| `if key in d: del d[key]` | `try: del d[key]` / `except KeyError: pass` |
| `for k, v in d.items():` on shared dict | `for k, v in d.copy().items():` |
| Counter increment | `with lock: d[k] = d.get(k, 0) + 1` or `collections.Counter` with external sync |

```python
def demo_pop_instead_of_check_delete():
    d = {"task": "pending", "done": True}
    removed = d.pop("task", None)
    assert removed == "pending"
    assert "task" not in d
    assert d.pop("missing", None) is None

demo_pop_instead_of_check_delete()
```

```python
def demo_delete_with_exception():
    d = {"a": 1}
    try:
        del d["a"]
    except KeyError:
        pass
    assert d == {}
    try:
        del d["gone"]
    except KeyError:
        pass

demo_delete_with_exception()
```

```python
def demo_copy_before_iterate():
    d = {"x": 1, "y": 2, "z": 3}
    for key, value in d.copy().items():
        assert key in "xyz"
        assert isinstance(value, int)

demo_copy_before_iterate()
```

---

## Lock-free reads vs locked writes (consistency)

```python
import threading

def demo_lockfree_read():
    d = {"count": 0}
    reads = []

    def reader():
        reads.append(d.get("count", -1))

    d["count"] = 42
    threads = [threading.Thread(target=reader) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert all(r in (0, 42) for r in reads)

demo_lockfree_read()
```

```python
import threading

def demo_increment_with_lock():
    d = {"n": 0}
    lock = threading.Lock()

    def bump(times):
        for _ in range(times):
            with lock:
                d["n"] = d["n"] + 1

    threads = [threading.Thread(target=bump, args=(250,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert d["n"] == 1000

demo_increment_with_lock()
```

---

## Best practices

| Situation | Approach |
|-----------|----------|
| Shared mutable dict | Per-dict `threading.Lock` or queue-based handoff |
| Cache with get-or-create | `setdefault` under a lock, or `dict.setdefault` knowing custom key `__eq__` risks |
| Bulk merge from untrusted iterable | Copy iterable to `list(pairs)` under lock first, then `update` |
| Compare dicts concurrently | `d == other` locks both for `dict` operands; still not a snapshot of future state |
| Read-heavy workload | Lock-free `get`/`in`/`len` avoid blocking writers—but plan for stale reads |

---

## Related topics in this guide

| Subject | Link |
|---------|------|
| Dict reference (views, merge operators) | [`Mapping Types — dict`](../../built-in-types/mapping-types-dict/index.md) |
| List extend / iteration pitfalls | [thread-safety-for-list-objects](../thread-safety-for-list-objects/index.md) |
| Set algebra locking | [thread-safety-for-set-objects](../thread-safety-for-set-objects/index.md) |

**See also:** [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html).
