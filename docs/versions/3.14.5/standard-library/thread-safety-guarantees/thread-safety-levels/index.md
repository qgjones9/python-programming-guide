# [Thread safety levels](https://docs.python.org/3/library/threadsafety.html#thread-safety-levels)

The C API and CPython internals classify operations by how much concurrency they tolerate. Those labels also help you reason about **built-in type** behavior in the [free-threaded build](../../../glossary/free-threaded-build/index.md): when the [GIL](../../../glossary/global-interpreter-lock/index.md) is disabled, guarantees on this page apply; with the GIL enabled, bytecode execution is largely serialized anyway. Full definitions live on [docs.python.org](https://docs.python.org/3/library/threadsafety.html#thread-safety-levels); this page maps each level to everyday Python and to when you must add your own [`threading.Lock`](https://docs.python.org/3/library/threading.html#threading.Lock).

For application-level patterns, see [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html).

---

## Levels at a glance (least → most safe)

Upstream lists five levels from **weakest** to **strongest** guarantees:

| Level | Caller synchronization | Same object, concurrent calls | Python-flavored mental model |
|-------|------------------------|------------------------------|------------------------------|
| [Incompatible](#incompatible) | Cannot be made safe | Unsafe even with a lock | Process-wide or interpreter-global state |
| [Compatible](#compatible) | **Required** — caller holds a lock | Races without external locking | Unsynchronized reads/writes on shared mutable state |
| [Safe on distinct objects](#safe-on-distinct-objects) | None if each thread uses its **own** instance | Unsafe on the **same** instance | Per-thread `list()` / `dict()` instances |
| [Safe on shared objects](#safe-on-shared-objects) | None — implementation locks internally | Safe on one object | Many `list.append` / `dict[key] =` operations |
| [Atomic](#atomic) | None | Appears instantaneous to other threads | Single indexed read `lst[i]` or `d[key]` |

---

## Incompatible

An operation cannot be made thread-safe for concurrent use, even if the caller wraps every call in a lock. Typical causes: unsynchronized **global** or **process-wide** state, or APIs whose contract assumes a single thread for the lifetime of the process.

| Situation | Why locking fails |
|-----------|-------------------|
| Installing signal handlers while other threads run | POSIX signal semantics and interpreter bookkeeping interact unpredictably |
| Mutating `os.environ` while other code reads the environment | The C runtime and other libraries may read env vars without your lock |
| Calling non-thread-safe C extensions from multiple threads | Extension may touch static globals the Python lock cannot cover |

**Python takeaway:** treat these as **single-threaded setup** phases (import time, `main` before workers start), not as hot paths inside worker threads.

---

## Compatible

Safe **only** when the caller supplies external synchronization for the whole critical section. Without it, concurrent calls may race or corrupt in-memory structures.

| Pattern | Risk without a lock |
|---------|---------------------|
| Read-modify-write on a shared `list` | `lst[i] = lst[i] + 1` is two operations |
| Check-then-act on a shared `dict` | `if key in d: del d[key]` (TOCTOU) |
| User-defined class mutating `self.items` | No per-object lock unless you add one |

```python
# Goal: external lock makes a compatible pattern safe
import threading

counter = {"n": 0}
lock = threading.Lock()

def increment():
    with lock:
        counter["n"] += 1

threads = [threading.Thread(target=increment) for _ in range(8)]
for t in threads:
    t.start()
for t in threads:
    t.join()
assert counter["n"] == 8
```

**When you need a lock:** any **multi-step** mutation or **check-then-act** on data shared across threads, including composed built-in operations upstream marks as non-atomic.

---

## Safe on distinct objects

Multiple threads may call the operation **at the same time** without your lock, as long as each call targets a **different** object (no shared underlying buffer or identity).

```python
# Goal: two threads, two lists — no shared object
import threading

left, right = [], []

def append_one(target, value):
    target.append(value)

t1 = threading.Thread(target=append_one, args=(left, "a"))
t2 = threading.Thread(target=append_one, args=(right, "b"))
t1.start()
t2.start()
t1.join()
t2.join()
assert left == ["a"] and right == ["b"]
```

**When you need a lock:** two threads pass the **same** `list`, `dict`, `set`, or `bytearray` instance, or aliases/views that share storage (for example multiple `memoryview` objects over one `bytearray`).

---

## Safe on shared objects

The implementation protects mutable state with [per-object locks](../../../glossary/per-object-lock/index.md) (or equivalent), so concurrent calls on the **same** instance do not corrupt the container. Other threads may still observe **logical** races (stale reads, partially applied logical updates) unless the operation is also **atomic** in the sense below.

| Example (free-threaded guarantees) | Notes |
|-----------------------------------|-------|
| `lst.append(x)`, `lst.pop()` at end | End mutations avoid element shifting |
| `d[key] = value`, `del d[key]`, `d.pop(key)` | Single-key writes hold the dict lock |
| `s.add(elem)`, `s.discard(elem)` | Set holds lock; `__eq__` on custom types can still run user code |

```python
# Goal: many threads appending to one list — no corruption (length grows)
import threading

shared = []

def append_range(start, count):
    for i in range(count):
        shared.append(start + i)

threads = [
    threading.Thread(target=append_range, args=(0, 50)),
    threading.Thread(target=append_range, args=(100, 50)),
]
for t in threads:
    t.start()
for t in threads:
    t.join()
assert len(shared) == 100
```

**When you need a lock:** you need a **consistent snapshot** or a **compound invariant** across multiple operations (iterate while another thread mutates, sort while another thread reads “logical” contents, etc.).

---

## Atomic

From the perspective of other threads, the operation completes **as one step**: no observable intermediate state on that object for that operation. Weaker operations may still run concurrently without blocking atomic reads ([lock-free](../../../glossary/lock-free/index.md) paths).

| Atomic-style reads (examples) | Non-atomic composed use |
|------------------------------|-------------------------|
| `lst[i]` | `lst[i] = lst[i] + 1` |
| `d[key]`, `d.get(key)`, `key in d`, `len(d)` | `if key in d: del d[key]` |
| `len(s)` (set) | `if elem in s: s.remove(elem)` when `in` and `remove` are separate steps |

```python
# Goal: prefer one atomic API over check-then-act
d = {"token": 1, "other": 2}

# Check-then-delete is NOT atomic across threads
removed = d.pop("token", None)
assert removed == 1
assert "token" not in d
```

**When you need a lock:** iteration over a live container, multi-key updates, or any workflow that must see a **frozen** view of the structure.

---

## Choosing a lock strategy

| Your goal | Prefer |
|-----------|--------|
| Protect a few shared built-ins | One `threading.Lock` (or `RLock`) around the critical section |
| Many independent objects | No lock across objects; lock per **shared** instance |
| Publish a consistent snapshot | `copy()`, `list(d)`, or iterate over `d.copy().items()` |
| Avoid TOCTOU on dicts | `d.pop(key, default)` or `try` / `except KeyError` instead of `if key in d` |
| Extension or C module | Read that module’s thread-safety docs — may be **Compatible** or **Incompatible** |

---

## Common pitfalls

| Pitfall | Safer approach |
|---------|----------------|
| Assuming “thread-safe type” means “thread-safe program” | Compose only **atomic** ops, or use explicit locks for multi-step logic |
| Iterating `for x in shared_list` while another thread mutates | Iterate `for x in shared_list.copy():` or hold a lock |
| Passing a generic **iterator** into `list.extend` from another thread | Lock the iterable or use built-in `list` / `tuple` / `dict` / `set` / `frozenset` operands documented as locked |
| Custom `__eq__` on keys or set elements | Comparison may run with locks released — see per-type pages |
| `memoryview` over mutable buffers | Thread safety follows the **exporter**; views do not make writes safe |

---

## Related pages in this repo

| Page | Focus |
|------|-------|
| [Thread Safety Guarantees](../index.md) | Hub: built-in container guarantees and navigation |
| [Thread safety for list objects](../thread-safety-for-list-objects/index.md) | Indexing, `append`, `sort`, iteration |
| [Thread safety for dict objects](../thread-safety-for-dict-objects/index.md) | Lock-free reads, `pop`, `update` locking rules |
| [Thread safety for set objects](../thread-safety-for-set-objects/index.md) | `in`, set algebra, `update` iterables |
| [Thread safety for bytearray objects](../thread-safety-for-bytearray-objects/index.md) | Buffer protocol vs per-object lock |
| [Thread safety for memoryview objects](../thread-safety-for-memoryview-objects/index.md) | Exporter ownership and races |
