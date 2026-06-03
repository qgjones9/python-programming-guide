# [Thread safety for set objects](https://docs.python.org/3/library/threadsafety.html#thread-safety-for-set-objects)

Built-in **`set`** objects have documented thread-safety guarantees in Python’s **free-threaded** build (GIL disabled). With the **GIL enabled**, set operations are mostly serialized, but logical races still matter in concurrent code. Full specification remains on [docs.python.org](https://docs.python.org/3/library/threadsafety.html#thread-safety-for-set-objects); this page covers lock-free reads, locked mutations, set-algebra locking, and iteration.

See [Thread safety levels](../thread-safety-levels/index.md). Related: [Thread safety for list objects](../thread-safety-for-list-objects/index.md), [Thread safety for dict objects](../thread-safety-for-dict-objects/index.md), and [`Set Types — set, frozenset`](../../built-in-types/set-types-set-frozenset/index.md).

---

## Scope: free-threaded vs GIL-enabled builds

| Build | What you can assume |
|-------|---------------------|
| **GIL enabled** | Memory corruption from concurrent set use is unlikely; membership check-then-remove and iteration races remain. |
| **Free-threaded** | `len` and `in` are lock-free; mutations and set algebra use per-object locks as documented below. |

---

## Lock-free reads

| Operation | Locking | Consistency notes |
|-----------|---------|-------------------|
| `len(s)` | Lock-free, atomic | Size read is atomic |
| `elem in s` | Lock-free | Does not block writers; may reflect concurrent changes |
| `elem not in s` | Lock-free | Same as `in` |

Lock-free **`in`** traverses the set with atomic reads. Operations that hold the per-object lock **do not block** these reads, so membership tests during in-place mutations may observe **intermediate states**.

### `__eq__()` during membership and mutations

`in`, `add`, `remove`, and `discard` may compare elements with **`==`**. Built-in types compare in C without releasing the set lock. Custom types with Python **`__eq__`** may cause the lock to be **released** during comparison, allowing concurrent modification.

---

## Per-object lock: single-element mutations (corruption-safe)

| Operation | Behavior |
|-----------|----------|
| `s.add(elem)` | Insert if not present |
| `s.remove(elem)` | Delete; raises `KeyError` if missing |
| `s.discard(elem)` | Delete if present |
| `s.pop()` | Remove and return arbitrary element |

These will **not corrupt** the set object. The same **`__eq__`** caveats apply when comparing custom element types.

```python
s = {1, 2, 3}
s.add(4)
assert 4 in s
s.discard(2)
assert 2 not in s
removed = s.pop()
assert removed in {1, 3, 4}
```

---

## Copy and clear

| Operation | Locking | Notes |
|-----------|---------|-------|
| `s.copy()` | Lock held for full operation | New set; appears atomic |
| `s.clear()` | Lock held for full operation | Other threads cannot see gradual removal |

---

## Set algebra: locking one or both operands

### Operators and in-place operators (`other` must be `set` or `frozenset`)

These **always lock both** operands:

| Operation |
|-----------|
| `s \| other`, `s &= other`, `s -= other`, `s ^= other` |
| `s & other`, `s - other`, `s ^ other` |

### Methods — when both objects are locked

| Method | Both locked when |
|--------|------------------|
| `s.update()`, `s.union()` | Other operand is **`set`**, **`frozenset`**, or **`dict`** (keys) |
| `s.intersection()`, `s.difference()` | Always tries to lock **all** involved sets |
| `s.symmetric_difference()` | Tries to lock both |
| `s.difference_update()`, `s.intersection_update()` | Tries to lock all objects one-by-one |
| `s.symmetric_difference_update()` | Locks args only if **`set`**, **`frozenset`**, or **`dict`** |
| `s.isdisjoint()`, `s.issubset()`, `s.issuperset()` | Always tries to lock both |

When methods accept **general iterables** (not exactly `set` / `frozenset` / `dict`), only the **target set** is locked—the iterable may be modified concurrently by another thread (same pattern as [dict `update`](../thread-safety-for-dict-objects/index.md)).

```python
a = {1, 2, 3}
b = {3, 4, 5}
assert a | b == {1, 2, 3, 4, 5}
a &= b
assert a == {3}
```

---

## NOT atomic (check-then-act, iteration)

| Anti-pattern | Problem |
|--------------|---------|
| `if elem in s: s.remove(elem)` | Element may be removed by another thread after `in` |
| `for elem in s: process(elem)` with concurrent writers | Skipped elements, `RuntimeError`, or duplicate processing |
| `if elem in s: s.discard(elem)` | Still two steps at Python level if written separately |

---

## Best practices

| Situation | Approach |
|-----------|----------|
| Shared set | External `threading.Lock` around compound logic |
| Remove if present | `s.discard(elem)` — single locked operation |
| Must raise if missing | `s.remove(elem)` alone — not preceded by `in` |
| Iterate under mutation | `for elem in s.copy():` or `for elem in set(s):` |
| Union from unknown iterable | `s.update(list(other))` under a lock, or use frozenset snapshot |
| Custom element `__eq__` | Hold external lock around `remove` / membership-heavy loops |

---

## Examples: safe vs unsafe patterns

### Atomic `len` and lock-free `in`

```python
import threading

def demo_len_and_membership():
    s = {10, 20, 30}
    sizes = []
    hits = []

    def observe():
        sizes.append(len(s))
        hits.append(20 in s)

    threads = [threading.Thread(target=observe) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sizes == [3, 3, 3]
    assert hits == [True, True, True]

demo_len_and_membership()
```

### Safe `discard` vs unsafe check-then-remove

```python
def demo_discard_vs_check_remove():
    s = {1, 2, 3}

    # UNSAFE under concurrency:
    # if 2 in s:
    #     s.remove(2)

    # SAFE: one operation
    s.discard(2)
    assert 2 not in s
    s.discard(99)  # no KeyError
    assert s == {1, 3}

demo_discard_vs_check_remove()
```

### Copy before iterate

```python
def demo_copy_before_iterate():
    s = {"a", "b", "c"}
    snapshot = set(s)  # or s.copy()
    upper = {x.upper() for x in snapshot}
    assert upper == {"A", "B", "C"}

demo_copy_before_iterate()
```

### Concurrent adds with external lock

```python
import threading

def demo_concurrent_add():
    s = set()
    lock = threading.Lock()

    def add_many(start, count):
        for i in range(start, start + count):
            with lock:
                s.add(i)

    threads = [
        threading.Thread(target=add_many, args=(0, 50)),
        threading.Thread(target=add_many, args=(50, 50)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(s) == 100
    assert s == set(range(100))

demo_concurrent_add()
```

### Set operators lock both operands

```python
def demo_operator_merge():
    workers = {1, 2, 3}
    extras = {3, 4}
    combined = workers | extras
    assert combined == {1, 2, 3, 4}
    workers |= extras
    assert workers == {1, 2, 3, 4}

demo_operator_merge()
```

---

## Related topics in this guide

| Subject | Link |
|---------|------|
| Set type reference | [`Set Types — set, frozenset`](../../built-in-types/set-types-set-frozenset/index.md) |
| Dict lock-free reads and TOCTOU | [thread-safety-for-dict-objects](../thread-safety-for-dict-objects/index.md) |
| List iteration and extend locking | [thread-safety-for-list-objects](../thread-safety-for-list-objects/index.md) |

**See also:** [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html).
