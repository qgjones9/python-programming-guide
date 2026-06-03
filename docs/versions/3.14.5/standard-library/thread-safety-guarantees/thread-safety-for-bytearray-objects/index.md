# [Thread safety for bytearray objects](https://docs.python.org/3/library/threadsafety.html#thread-safety-for-bytearray-objects)

Built-in **`bytearray`** objects have documented thread-safety guarantees in Python’s **free-threaded** build (GIL disabled). When the **GIL is enabled**, most operations are implicitly serialized, but logical races (check-then-act, iteration during mutation) still matter for correct programs. Full specification remains on [docs.python.org](https://docs.python.org/3/library/threadsafety.html#thread-safety-for-bytearray-objects); this page categorizes operations and shows safe patterns.

For safety-level terminology, see [Thread safety levels](../thread-safety-levels/index.md). Buffer views over mutable bytes are covered in [Thread safety for memoryview objects](../thread-safety-for-memoryview-objects/index.md).

---

## Scope: free-threaded vs GIL-enabled builds

| Build | What you can assume |
|-------|---------------------|
| **GIL enabled** (default CPython) | One thread runs Python bytecode at a time; structure corruption is rare, but TOCTOU and stale reads still occur across threads. |
| **Free-threaded** (`Py_GIL_DISABLED`) | Guarantees below apply explicitly: `len` is lock-free; buffer-protocol compares may see intermediate states; mutations use a per-object lock. |

Neither mode makes **iteration while another thread mutates** safe without a snapshot or external lock.

---

## Lock-free operations

| Operation | Behavior |
|-----------|----------|
| `len(ba)` | Lock-free and **atomic** — returns a consistent length without acquiring the per-object lock. |

### Buffer-protocol reads (no per-object lock)

Concatenation and comparisons use the **buffer protocol**. They prevent **resizing** the buffer but do **not** hold the bytearray’s per-object lock. Lock-free reads and other threads’ in-place writes may interleave, so results can reflect **intermediate states**:

| Operation | Notes |
|-----------|-------|
| `ba + other` | Builds a new object; may observe concurrent in-place writes to `ba` or `other`. |
| `ba == other`, `ba < other`, … | Compares via buffer protocol; not a single atomic snapshot of both buffers. |

**Corruption:** These operations will not corrupt the bytearray object. **Consistency:** Comparison and concatenation results may be inconsistent with any single point-in-time view of the data.

---

## Per-object lock: safe from corruption

All operations below acquire the bytearray’s internal lock (unless noted). They **will not corrupt** the buffer structure.

### Single-element and slice access

| Operation | Notes |
|-----------|-------|
| `ba[i]` (read) | Safe from multiple threads. |
| `ba[i:j]` (read slice) | Safe from multiple threads. |
| `ba[i] = x` | Single-byte write; safe, will not corrupt. |
| `ba[i:j] = values` | Slice write; safe. When `values` is a **`bytearray`**, **both** objects are locked for the assignment. |

### In-place mutators (one object locked)

| Operation | Notes |
|-----------|-------|
| `ba.append(x)` | Append one byte at end. |
| `ba.extend(iterable)` | Extend with iterable bytes. |
| `ba.insert(i, x)` | Insert one byte. |
| `ba.pop()` | Remove and return last byte. |
| `ba.pop(i)` | Remove and return byte at index. |
| `ba.remove(x)` | Remove first occurrence of byte value `x`. |
| `ba.reverse()` | Reverse in place. |
| `ba.clear()` | Remove all bytes; other threads cannot observe element-by-element removal. |

### Operations that return new objects (lock held for duration)

| Operation | Notes |
|-----------|-------|
| `ba.copy()` | Shallow copy; appears atomic to other threads. |
| `ba * n` | Repeat into a **new** `bytearray`; lock held for the operation. |

### Membership (lock held for duration)

| Operation | Notes |
|-----------|-------|
| `x in ba` | Holds lock for the search; will not corrupt, but still separate from a following `remove` in user code. |

### Other methods

All remaining `bytearray` methods (`find`, `replace`, `split`, `decode`, `hex`, …) hold the per-object lock for their full duration.

---

## Slice assignment: locking both bytearrays

When the right-hand side of slice assignment is exactly a **`bytearray`** (not a subclass), CPython locks **both** the target and the source for the assignment:

```python
# ba[i:j] = other_bytearray  # both locked when other_bytearray is bytearray
target = bytearray(b"00000")
source = bytearray(b"AB")
target[1:3] = source
assert target == b"0AB00"
```

Assigning from `bytes`, `memoryview`, or arbitrary iterables follows the usual rules for that RHS type; only **bytearray → bytearray** slice assign locks both sides.

---

## NOT atomic (read-modify-write, check-then-act, iteration)

Compound Python expressions compile to **multiple** steps. They are never atomic even when each step is corruption-safe.

| Anti-pattern | Why it fails |
|--------------|--------------|
| `if x in ba: ba.remove(x)` | Membership and `remove` are separate calls (TOCTOU). |
| `for byte in ba: ...` while another thread mutates | Iterator may skip, repeat, or raise during concurrent structural change. |
| `ba[i] = ba[i] + 1` | Read and write are separate (not meaningful for bytes without a lock, but illustrates the pattern). |

---

## Safe iteration

Iterate over a **copy** when another thread may modify the same `bytearray` (see also `demo_copy_before_iterate` below):

```python
def demo_iterate_copy_snapshot():
    ba = bytearray(b"abc")

    def process(byte_val):
        return byte_val + 1

    results = [process(b) for b in ba.copy()]
    assert results == [98, 99, 100]

demo_iterate_copy_snapshot()
```

`list(ba)` or `bytes(ba)` also materialize a snapshot (immutable `bytes` for read-only consumers).

---

## Best practices

| Situation | Recommended approach |
|-----------|---------------------|
| Shared `bytearray` across threads | One `threading.Lock` per buffer, or single-writer design |
| Compare or concatenate under writers | Treat result as approximate; use a lock for strict snapshots |
| Remove if present | `with lock:` around check + `remove`, or design without check-then-act |
| Iterate while others write | `for b in ba.copy():` |
| Expose buffer to `memoryview` | Coordinate with [memoryview thread safety](../thread-safety-for-memoryview-objects/index.md); lock underlying data |
| Resize or `extend` while views exist | Avoid — raises `BufferError` while exported |

---

## Examples

### Lock-free `len` vs locked `append`

```python
import threading

def demo_len_and_append():
    ba = bytearray(b"hi")
    assert len(ba) == 2

    def grow():
        for _ in range(50):
            ba.append(ord("a"))

    t = threading.Thread(target=grow)
    t.start()
    t.join()
    assert len(ba) == 52
    assert ba[-1] == ord("a")

demo_len_and_append()
```

### Unsafe check-then-act vs locked remove

```python
import threading

def demo_check_then_act_vs_lock():
    ba = bytearray([10, 20, 30])
    lock = threading.Lock()

    # UNSAFE under concurrency (two steps):
    # if 20 in ba:
    #     ba.remove(20)

    with lock:
        if 20 in ba:
            ba.remove(20)
    assert ba == bytearray([10, 30])

demo_check_then_act_vs_lock()
```

### Copy before iterate

```python
def demo_copy_before_iterate():
    ba = bytearray(b"abc")
    snapshot = ba.copy()
    upper = [bytes([b]).upper() for b in snapshot]
    assert upper == [b"A", b"B", b"C"]

demo_copy_before_iterate()
```

### Concurrent access with `threading.Lock`

```python
import threading

def demo_lock_for_shared_bytearray():
    ba = bytearray(4)
    lock = threading.Lock()

    def writer(start, fill):
        for i in range(4):
            with lock:
                ba[start + i] = fill

    t1 = threading.Thread(target=writer, args=(0, ord("x")))
    t2 = threading.Thread(target=writer, args=(0, ord("y")))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert len(ba) == 4
    assert all(b in (ord("x"), ord("y")) for b in ba)

demo_lock_for_shared_bytearray()
```

### Slice assignment locks both bytearrays

```python
def demo_slice_assign_two_locked():
    target = bytearray(b"----")
    source = bytearray(b"AB")
    target[1:3] = source
    assert bytes(target) == b"-AB-"

demo_slice_assign_two_locked()
```

---

## Related topics in this guide

| Subject | Link |
|---------|------|
| Thread safety levels | [thread-safety-levels](../thread-safety-levels/index.md) |
| memoryview and underlying buffers | [thread-safety-for-memoryview-objects](../thread-safety-for-memoryview-objects/index.md) |
| Binary sequence types | [bytes, bytearray, memoryview](../../built-in-types/binary-sequence-types-bytes-bytearray-memoryview/index.md) |

**See also:** [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html).
