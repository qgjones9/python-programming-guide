# [Thread Safety Guarantees](https://docs.python.org/3/library/threadsafety.html)

Built-in containers (`list`, `dict`, `set`, `bytearray`, and `memoryview` over exporters) gained explicit **per-operation** concurrency rules for CPython’s [free-threaded build](../../glossary/free-threaded-build/index.md). Those rules apply when the [GIL](../../glossary/global-interpreter-lock/index.md) is **disabled**; with the GIL on, bytecode execution still serializes most Python-level races. Canonical tables and edge cases remain on [docs.python.org](https://docs.python.org/3/library/threadsafety.html). This hub orients you to the vocabulary, child notes, and practical locking patterns.

For writing thread-safe applications (locks, immutability, extension modules), start with [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html).

---

## What “thread-safe” means here

Upstream does **not** claim that sharing a `list` or `dict` across threads is always safe without thought. It documents **which single operations** avoid corruption, which are **atomic**, which use [lock-free](../../glossary/lock-free/index.md) reads, and when you must supply [external synchronization](../../glossary/synchronization-primitive/index.md).

| Concept | Meaning in these docs |
|---------|----------------------|
| **No corruption** | Concurrent calls will not smash internal C structures of the built-in object |
| **Atomic** | Other threads do not observe a half-finished **single** operation on that object |
| **Logical race** | Structure stays valid, but results may surprise you (stale length, partial membership scan) |
| **Per-object lock** | Many mutating methods serialize on the same instance; see [per-object lock](../../glossary/per-object-lock/index.md) |

Operations that touch **two** objects (for example `d.update(other_dict)`) may lock **both** when the other operand is a plain built-in of the documented type—not a subclass with custom iteration.

---

## C API safety levels (summary)

The same five-level scale used in the C API applies to how you should think about Python call sites. Full prose and examples: [Thread safety levels](thread-safety-levels/index.md).

| Level | You provide a lock? | Typical built-in example |
|-------|---------------------|--------------------------|
| Incompatible | Cannot fix with Python locks | Process-wide setup (signals, env) |
| Compatible | **Yes**, for multi-step use | `lst[i] = lst[i] + 1`, `if key in d: del d[key]` |
| Safe on distinct objects | No, if instances differ | Thread A mutates `list_a`, thread B mutates `list_b` |
| Safe on shared objects | No, for that single op | `lst.append(x)`, `d[key] = v` |
| Atomic | No; appears one step | `lst[i]`, `d.get(key)`, `len(d)` |

---

## Sharing built-in containers — best practices

| Practice | Why |
|----------|-----|
| Treat **single operations** as the unit of safety | Composing two “safe” calls is often **Compatible**, not atomic |
| Use **`pop(key, default)`** instead of check-then-delete on dicts | Avoids time-of-check/time-of-use races between threads |
| Iterate **`for item in container.copy():`** (or snapshot keys) | Iteration is never atomic while another thread mutates |
| Prefer **immutable** messages between threads | `tuple`, `frozenset`, or new `list`/`dict` snapshots reduce shared mutation |
| Lock **iterables** passed to `extend` / `update` unless they are documented built-in types | Generic iterators can be consumed or mutated concurrently |
| Guard **custom `__eq__`** keys and set elements | Comparisons may run Python code while locks are released |
| Separate **`memoryview`** writers with a lock when the exporter is mutable | View safety follows the underlying `bytearray` (or buffer), not the view alone |

```python
# Goal: snapshot before iteration — safe logical view
import threading

data = {"a": 1, "b": 2, "c": 3}

def sum_values_snapshot():
    return sum(data.copy().values())

assert sum_values_snapshot() == 6
```

```python
# Goal: one lock around a multi-step invariant on shared state
import threading

inventory = {"apples": 10}
lock = threading.Lock()

def sell(item, qty):
    with lock:
        if inventory[item] < qty:
            return False
        inventory[item] -= qty
        return True

assert sell("apples", 3) is True
assert inventory["apples"] == 7
```

```python
# Goal: atomic read vs non-atomic read-modify-write
values = [1, 2, 3]
index = 1
assert values[index] == 2  # single __getitem__ — atomic read

# NOT atomic as a whole — needs a lock if threads share values
values[index] = values[index] + 10
assert values == [1, 12, 3]
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| “`append` is safe, so my counter logic is safe” | `if lst: lst.pop()` is two steps | Hold a lock or use atomic single-op patterns |
| Concurrent **`sort()`** while reading | List may appear **empty** for the sort duration | Do not assume stable length during `sort()` |
| **`remove`** / **`__eq__`** on lists or sets | User code runs during search | Narrow element types or external lock |
| **`lst += iterable`** with a custom iterator | Iterator not locked | Pass `list`, `tuple`, `dict`, `set`, or `frozenset` per upstream rules |
| Assuming **`memoryview`** makes bytes safe | Writable exporter still races | Lock the `bytearray` (or avoid shared mutation) |

---

## When external synchronization is required

Use your own lock (or a higher-level queue) when any of the following apply:

- **Multiple operations** must appear as one transaction on the same object.
- Threads **iterate** while others **mutate** the same container.
- You implement **check-then-act** (`if`, then `del` / `pop` / `remove`).
- You pass **non-built-in iterables** into bulk mutators (`extend`, `update`, slice assignment).
- You share **mutable buffer memory** through `memoryview` or the buffer protocol.
- You call **C extensions** or library code with unknown [thread safety levels](thread-safety-levels/index.md).

With the **GIL enabled**, many bugs hide because bytecode is serialized; test free-threaded builds (`python3.14t` or `--disable-gil` builds) when targeting true parallelism.

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [Thread safety levels](thread-safety-levels/index.md) | Five C API levels (Incompatible → Atomic); comparison table; when callers must lock; Python-oriented examples. |
| [Thread safety for list objects](thread-safety-for-list-objects/index.md) | Atomic `lst[i]` reads; lock-free `in` / `index` / `count`; `append` / `pop` at end; non-atomic insert, slice, iteration. |
| [Thread safety for dict objects](thread-safety-for-dict-objects/index.md) | Lock-free `d[key]`, `get`, `in`, `len`; single-key writes; paired locking for `update` and `==`; TOCTOU avoidance. |
| [Thread safety for set objects](thread-safety-for-set-objects/index.md) | Lock-free `len`; `in` without blocking locked mutators; `add` / `remove`; set/set algebra locking rules. |
| [Thread safety for bytearray objects](thread-safety-for-bytearray-objects/index.md) | Buffer-protocol concat/compare vs locked byte ops; slice assignment locking pairs. |
| [Thread safety for memoryview objects](thread-safety-for-memoryview-objects/index.md) | View lifetime vs exporter mutability; races on shared buffers; `BufferError` on resize while exported. |

---

## Subsection highlights

### [Thread safety levels](thread-safety-levels/index.md)

Vocabulary for reading both C API docs and the per-type sections below. Use it to decide whether your **call site** is one atomic operation or a **Compatible** pattern that needs `threading.Lock`.

### [Thread safety for list objects](thread-safety-for-list-objects/index.md)

Single-element reads are atomic; traversal helpers use atomic per-element reads but may see concurrent edits. Most other mutators take the per-object lock; `sort()` temporarily presents an empty list to other threads.

### [Thread safety for dict objects](thread-safety-for-dict-objects/index.md)

Several read paths are lock-free. Single-key insert/delete/pop paths avoid corruption; equality and some updates lock one or two dicts when operands are exact built-in types.

### [Thread safety for set objects](thread-safety-for-set-objects/index.md)

Membership tests can interleave with locked mutations. Bulk operations lock documented `set` / `frozenset` / `dict` partners; arbitrary iterables in `update` may need caller-side locking.

### [Thread safety for bytearray objects](thread-safety-for-bytearray-objects/index.md)

Concatenation and ordering comparisons use the buffer protocol without the per-object lock; byte and slice writes generally hold it.

### [Thread safety for memoryview objects](thread-safety-for-memoryview-objects/index.md)

Creating and releasing views is synchronized; **data** safety depends on the exporter—immutable `bytes` vs mutable `bytearray` differ sharply.
