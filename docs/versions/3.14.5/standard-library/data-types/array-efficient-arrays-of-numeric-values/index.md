# [array — Efficient arrays of numeric values](https://docs.python.org/3/library/array.html)

The [`array`](https://docs.python.org/3/library/array.html) module defines **`array.array`**, a mutable sequence that stores **homogeneous numeric values** compactly using C-level type codes (`'i'`, `'f'`, `'d'`, …). Arrays behave like lists for indexing and slicing but constrain element types and expose the **buffer protocol** for binary I/O. Type code sizes may depend on platform; see `array.itemsize`. Full type-code table and file interchange methods are on [docs.python.org](https://docs.python.org/3/library/array.html).

---

## Type codes — [Type Codes](https://docs.python.org/3/library/array.html)

| Code | C type (typical) | Python type | Notes |
|------|------------------|-------------|-------|
| `'b'` / `'B'` | signed/unsigned char | int | 1 byte |
| `'h'` / `'H'` | short | int | 2 bytes |
| `'i'` / `'I'` | int | int | platform width |
| `'l'` / `'L'` | long | int | 4 bytes typical |
| `'q'` / `'Q'` | long long | int | 8 bytes |
| `'f'` | float | float | 4 bytes |
| `'d'` | double | float | 8 bytes |
| `'w'` | Py_UCS4 | str char | Unicode (3.13+) |

`'u'` is deprecated — migrate to `'w'`. Discover all codes: `array.typecodes`.

```python
# Goal: compact int buffer and export bytes
import array

nums = array.array("i", [1, 2, 3, 4])
raw = nums.tobytes()
clone = array.array("i")
clone.frombytes(raw)
assert list(clone) == [1, 2, 3, 4]
assert nums.itemsize * len(nums) == len(raw)
```

---

## Sequence and I/O methods

| Method | Role |
|--------|------|
| `append` / `extend` / `insert` | Mutate like list (typed) |
| `tobytes()` / `frombytes()` | Machine-value byte blob |
| `tofile(f)` / `fromfile(f, n)` | Binary file read/write |
| `tolist()` | Convert to Python list |
| `byteswap()` | Endian swap for multi-byte codes |
| `buffer_info()` | `(address, length)` — prefer buffer protocol |

Slice assignment requires another `array` with the **same typecode**.

```python
# Goal: stack arrays of same typecode
import array

a = array.array("f", [1.0, 2.0])
b = array.array("f", [3.0])
a.extend(b)
assert a.typecode == b.typecode == "f"
assert list(a) == [1.0, 2.0, 3.0]
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Match **typecode to wire format** | Avoid silent widening/narrowing |
| Call **`byteswap()`** when reading foreign-endian files | Native order is platform-dependent |
| Use **`struct`** for mixed-type records | `array` is homogeneous only |
| Prefer **NumPy** for heavy numerics | Richer ops and broadcasting |
| Keep **`itemsize`** in protocol docs | Peers must agree on layout |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Mixing typecodes in `extend` | `TypeError` | Normalize or convert first |
| Assuming `'i'` is always 4 bytes | Platform-dependent | Check `itemsize` |
| Unicode via wrong typecode | `ValueError` on `fromunicode` | Use `'w'` or encode/decode bytes |
| Relying on `eval(repr(a))` | Needs imports and `nan`/`inf` defined | Use `tobytes`/`frombytes` for persistence |
| Using deprecated `'u'` | Removal planned | Migrate to `'w'` |

---

## See also

- [`struct`](../binary-data-services/struct-interpret-bytes-as-packed-binary-data/index.md) — heterogeneous packing
- [`memoryview`](https://docs.python.org/3/library/stdtypes.html#memoryview) — zero-copy buffer views
