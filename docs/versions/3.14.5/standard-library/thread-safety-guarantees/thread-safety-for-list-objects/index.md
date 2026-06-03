# [Thread safety for list objects](https://docs.python.org/3/library/threadsafety.html#thread-safety-for-list-objects)

Built-in **`list`** objects have documented thread-safety guarantees in Python’s **free-threaded** build (GIL disabled). When the **GIL is enabled**, most list operations are already serialized by the interpreter, so races are far less visible—but the guarantees below still describe what the implementation promises in free-threaded mode. Full specification remains on [docs.python.org](https://docs.python.org/3/library/threadsafety.html#thread-safety-for-list-objects); this page categorizes operations and shows safe patterns.

For background on safety levels (atomic, per-object lock, compatible), see [Thread safety levels](../thread-safety-levels/index.md). Related containers: [Thread safety for dict objects](../thread-safety-for-dict-objects/index.md), [Thread safety for set objects](../thread-safety-for-set-objects/index.md).

---

## Scope: free-threaded vs GIL-enabled builds

| Build | What you can assume |
|-------|---------------------|
| **GIL enabled** (default CPython) | One thread runs Python bytecode at a time; concurrent list access rarely corrupts memory, but logical races (TOCTOU, stale reads) still exist if you release the GIL in C extensions or use `threading`. |
| **Free-threaded** (`Py_GIL_DISABLED`) | Guarantees in this page apply explicitly: some reads are lock-free, mutations use a per-object lock, and compound Python-level expressions are **not** atomic. |

Neither mode makes **iteration while another thread mutates** safe without external synchronization or a snapshot copy.

---

## Operation categories

### Lock-free reads (no per-object lock)

These operations use **atomic reads** of each element. They **do not block** concurrent writers and may return results reflecting **intermediate states** during in-place mutations (for example during `insert` or slice assignment).

| Operation | Notes |
|-----------|-------|
| `lst[i]` (read) | Single-element read is atomic; you always get one complete object reference. |
| `item in lst` | Traverses with atomic reads; membership may reflect concurrent changes. |
| `lst.index(item)` | Same traversal model as `in`. |
| `lst.count(item)` | Same traversal model as `in`. |

**Corruption:** These reads will not corrupt the list object itself. **Consistency:** Results may be stale or reflect a partially updated list during multi-element in-place operations.

### Per-object lock held (safe from corruption)

All operations below acquire the list’s internal lock (unless noted). They **will not corrupt** the list structure. Some still allow lock-free reads to observe intermediate element states during multi-step in-place updates.

| Operation | Corruption-safe | Other threads may observe |
|-----------|-----------------|---------------------------|
| `lst[i] = x` (write one slot) | Yes | N/A for structure |
| `lst1 + lst2`, `x * lst`, `lst.copy()` | Yes | New object; appears atomic |
| `lst.append(x)`, `lst.pop()` (no index) | Yes | Atomic end operations |
| `lst.clear()` | Yes | Cannot see elements removed one-by-one |
| `lst.sort()` | Yes | List appears **empty** for sort duration |
| `lst.insert(idx, item)`, `lst.pop(idx)`, `lst *= n` | Yes | Lock-free reads may see **intermediate** layouts |
| `lst.extend(iterable)`, `lst += iterable` | Yes | Iterable locking depends on type (see below) |
| `lst[i:j] = iterable` | Yes | Iterable locked only when it is exactly a **`list`** (not subclasses) |

### `__eq__()` and `remove()`

`lst.remove(item)` compares elements with **`==`**, which may run arbitrary Python code for custom types. During comparison the per-object lock **may be released**, so another thread can modify the list. Built-in types (`str`, `int`, `float`, …) compare in C without releasing the lock.

| Type of element | Lock during `remove()` comparison |
|-----------------|-----------------------------------|
| Built-in immutable types | Lock retained |
| Custom types with Python `__eq__` | Lock may be released |

---

## NOT atomic (read-modify-write, check-then-act, iteration)

Compound Python expressions compile to **multiple** C API calls. They are never atomic even when each individual step is “safe.”

| Anti-pattern | Why it fails |
|--------------|--------------|
| `lst[i] = lst[i] + 1` | Read and write are separate operations. |
| `if lst: item = lst.pop()` | Check and pop are separate (TOCTOU). |
| `for item in lst: ...` while another thread mutates | Iterator invalidation / skipped or duplicate items. |
| `lst.remove(x)` with custom `__eq__` | Comparison may interleave with other mutations. |

---

## `extend`, `+=`, and slice assignment

| Iterable passed to `extend` / `+=` / slice assign | Thread-safe against concurrent modification of **iterable** |
|---------------------------------------------------|---------------------------------------------------------------|
| `list`, `tuple`, `set`, `frozenset`, `dict`, dict views (exact types, not subclasses) | Yes — iterable is read under appropriate locking |
| Arbitrary iterator or subclass | No — another thread may mutate the source during iteration |

```python
# extend from a built-in tuple is safe against concurrent tuple replacement
# (each thread should use its own list or external lock for the list itself)
base = [1, 2]
base.extend((3, 4))
assert base == [1, 2, 3, 4]

# slice assignment locks the RHS only when it is exactly list, not a list subclass
class MyList(list):
    pass

target = [0, 0, 0]
target[0:2] = [10, 20]  # RHS is list — locked
assert target == [10, 20, 0]
sub = MyList([1, 2])
assert isinstance(sub, list) and type(sub) is MyList  # subclass: different locking rules
```

---

## Best practices

| Situation | Recommended approach |
|-----------|---------------------|
| Shared list across threads | One `threading.Lock` (or `RLock`) per shared list, or confine ownership to one thread |
| Iterate while others may write | `for item in lst.copy():` or `for item in list(lst):` |
| Pop if non-empty | `try: item = lst.pop()` / `except IndexError: pass` — not `if lst: lst.pop()` |
| Increment in place | `with lock: lst[i] = lst[i] + 1` or use a dedicated counter |
| Bulk consume | Prefer `pop()` from the end (atomic) over `pop(0)` when order allows |
| Custom element types in `remove` | External lock around `remove`, or avoid `remove` in concurrent code |

---

## Examples: safe vs unsafe patterns

### Atomic single-element read

```python
import threading

def demo_atomic_index_read():
    lst = [10, 20, 30]
    seen = []

    def reader():
        seen.append(lst[1])

    threads = [threading.Thread(target=reader) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert seen == [20, 20, 20, 20, 20]

demo_atomic_index_read()
```

### Safe end mutations (`append` / `pop`)

```python
import threading

def demo_append_pop_end():
    lst = []
    lock = threading.Lock()

    def producer(n):
        for i in range(n):
            with lock:
                lst.append(i)

    def consumer(n):
        got = []
        for _ in range(n):
            with lock:
                if lst:
                    got.append(lst.pop())
        return got

    t1 = threading.Thread(target=producer, args=(100,))
    t1.start()
    t1.join()
    assert len(lst) == 100
    assert lst[-1] == 99

demo_append_pop_end()
```

### Unsafe check-then-act vs safe `pop`

```python
def demo_check_then_act_vs_pop():
    lst = [1, 2, 3]

    # UNSAFE under concurrency (two steps):
    # if lst:
    #     item = lst.pop()

    # SAFE: single call; use try/except for empty list
    item = lst.pop()
    assert item == 3
    assert lst == [1, 2]

    lst.clear()
    try:
        lst.pop()
    except IndexError:
        pass
    assert lst == []

demo_check_then_act_vs_pop()
```

### Copy before iterate

```python
def demo_copy_before_iterate():
    lst = ["a", "b", "c"]
    snapshot = list(lst)  # or lst.copy()
    processed = [x.upper() for x in snapshot]
    assert processed == ["A", "B", "C"]

demo_copy_before_iterate()
```

### Read-modify-write requires a lock

```python
import threading

def demo_read_modify_write():
    lst = [0]
    lock = threading.Lock()

    def increment_many(times):
        for _ in range(times):
            with lock:
                lst[0] = lst[0] + 1

    threads = [threading.Thread(target=increment_many, args=(100,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert lst[0] == 400

demo_read_modify_write()
```

---

## Related topics in this guide

| Subject | Link |
|---------|------|
| Thread safety levels | [thread-safety-levels](../thread-safety-levels/index.md) |
| Dict TOCTOU and lock-free reads | [thread-safety-for-dict-objects](../thread-safety-for-dict-objects/index.md) |
| Set membership and set algebra locking | [thread-safety-for-set-objects](../thread-safety-for-set-objects/index.md) |
| Sequence types reference | [`list`](../../built-in-types/sequence-types-list-tuple-range/index.md) |

**See also:** [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html) for general guidance on writing concurrent Python code without the GIL.
