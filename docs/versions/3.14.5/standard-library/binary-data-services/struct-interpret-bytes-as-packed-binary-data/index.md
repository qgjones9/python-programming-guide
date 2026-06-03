# [struct — Interpret bytes as packed binary data](https://docs.python.org/3/library/struct.html)

The [`struct`](https://docs.python.org/3/library/struct.html) module converts between Python values and C-style packed bytes. A **format string** describes field types, byte order, and (in native mode) alignment padding. Use it for network headers, file formats, and Python↔C data exchange. Full format tables and edge cases remain on [docs.python.org](https://docs.python.org/3/library/struct.html).

Related modules: [`array`](../../data-types/array-efficient-arrays-of-numeric-values/index.md) for homogeneous numeric buffers, [`ctypes`](../../generic-operating-system-services/ctypes-a-foreign-function-library-for-python/index.md) for C struct layouts, and built-in [`bytes`](../../built-in-types/binary-sequence-types-bytes-bytearray-memoryview/index.md) / [`memoryview`](../../built-in-types/binary-sequence-types-bytes-bytearray-memoryview/index.md) for zero-copy views.

---

## Core functions — [Functions and Exceptions](https://docs.python.org/3/library/struct.html#functions-and-exceptions)

| Function | Role |
|----------|------|
| `struct.pack(format, *values)` | Build a `bytes` object from values |
| `struct.unpack(format, buffer)` | Parse one record from `bytes` (returns a tuple) |
| `struct.unpack_from(format, buffer, offset=0)` | Parse at a slice offset |
| `struct.pack_into(format, buffer, offset, *values)` | Write into a writable buffer (`bytearray`, `memoryview`) |
| `struct.iter_unpack(format, buffer)` | Yield one tuple per fixed-size record |
| `struct.calcsize(format)` | Byte length of one packed record |
| `struct.error` | Raised on bad formats, wrong buffer sizes, out-of-range values |

```python
# Goal: pack and unpack a big-endian record
import struct

fmt = ">hhl"  # signed short, signed short, signed long (standard sizes)
data = struct.pack(fmt, 1, 2, 3)
assert struct.unpack(fmt, data) == (1, 2, 3)
assert struct.calcsize(fmt) == 8
```

```python
# Goal: iterate fixed-width records from a buffer
import struct

blob = struct.pack("<ii", 10, 20) + struct.pack("<ii", 30, 40)
records = list(struct.iter_unpack("<ii", blob))
assert records == [(10, 20), (30, 40)]
```

```python
# Goal: write into a preallocated bytearray (no intermediate bytes)
import struct

buf = bytearray(8)
struct.pack_into("<II", buf, 0, 0xDEADBEEF, 42)
assert struct.unpack_from("<II", buf, 0) == (0xDEADBEEF, 42)
```

---

## Format strings — [Format Strings](https://docs.python.org/3/library/struct.html#format-strings)

A format string is an optional **byte-order prefix** followed by one or more **format characters** (and optional repeat counts). Whitespace between characters is ignored. Repeat counts apply to the preceding code (`'4h'` ≡ `'hhhh'`).

| Concept | Detail |
|---------|--------|
| Prefix | Controls endianness and whether C-style padding is inserted |
| Characters | Map C types to Python `int`, `float`, `bool`, `bytes`, or `complex` |
| Buffer args | `bytes`, `bytearray`, and any object supporting the [buffer protocol](https://docs.python.org/3/c-api/buffer.html) |

When no prefix is given, **native mode** (`@`) is assumed: layout matches the C compiler that built your interpreter, including implicit pad bytes between members.

---

## Byte order and alignment — [Byte Order, Size, and Alignment](https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment)

The first character of a format string (when present) selects endianness and sizing rules:

| Prefix | Byte order | Size / alignment |
|--------|------------|------------------|
| `@` | Native | Native (default when no prefix) |
| `=` | Native | Standard sizes, no alignment padding |
| `<` | Little-endian | Standard sizes, no padding |
| `>` | Big-endian | Standard sizes, no padding |
| `!` | Network (big-endian) | Standard sizes, no padding |

For **data interchange** (files, sockets, other languages), prefer `<`, `>`, or `!` and insert explicit `'x'` pad bytes. Native `@` matches the C compiler that built your interpreter but not necessarily remote peers.

```python
# Goal: same integer, different endianness
import struct

n = 1023
assert struct.pack(">h", n) == b"\x03\xff"
assert struct.pack("<h", n) == b"\xff\x03"
```

---

## Common format characters — [Format Characters](https://docs.python.org/3/library/struct.html#format-characters)

| Char | C type (typical) | Python type | Std size (bytes) |
|------|------------------|-------------|------------------|
| `x` | pad byte | — | 1 |
| `c` | char | bytes length 1 | 1 |
| `b` / `B` | signed / unsigned char | int | 1 |
| `h` / `H` | short / unsigned short | int | 2 |
| `i` / `I` | int / unsigned int | int | 4 |
| `q` / `Q` | long long | int | 8 |
| `e` | _Float16 | float | 2 |
| `f` / `d` | float / double | float | 4 / 8 |
| `F` / `D` | float / double complex | complex | 8 / 16 |
| `n` / `N` | `ssize_t` / `size_t` | int | native only |
| `s` | char[] | bytes (fixed width) | count |
| `p` | Pascal string | bytes (≤255 chars) | count |
| `P` | void* | int | native only |
| `?` | _Bool | bool | 1 |

`'s'` counts **bytes in one blob** (`'10s'`); `'c'` repeats **single-byte values** (`'10c'` → ten 1-byte fields). `'P'`, `'n'`, and `'N'` are available only in native (`@`) mode. Out-of-range integers raise `struct.error` (since 3.1).

```python
# Goal: detect out-of-range values early
import struct

try:
    struct.pack(">h", 99999)
except struct.error:
    ok = True
else:
    ok = False
assert ok
```

---

## Examples — [Examples](https://docs.python.org/3/library/struct.html#examples)

```python
# Goal: 's' packs one fixed-width blob; 'c' packs separate 1-byte values
import struct

assert struct.pack("@3s", b"123") == b"123"
assert struct.pack("@ccc", b"1", b"2", b"3") == b"123"
assert struct.unpack("@3s", b"123") == (b"123",)
assert struct.unpack("@ccc", b"123") == (b"1", b"2", b"3")
```

```python
# Goal: unpack into a named tuple for readable record access
import struct
from collections import namedtuple

Record = namedtuple("Record", "name serialnum school gradelevel")
raw = b"raymond   \x32\x12\x08\x01\x08"
record = Record._make(struct.unpack("<10sHHb", raw))
assert record.name.startswith(b"raymond")
assert record.gradelevel == 8
```

---

## Native vs standard layouts — [Applications](https://docs.python.org/3/library/struct.html#applications)

| Mode | When to use | Padding |
|------|-------------|---------|
| **Native** (`@` or no prefix) | Same-process C extension / same compiler | Automatic between members |
| **Standard** (`<`, `>`, `!`) | Cross-platform protocols | You supply `'x'` bytes explicitly |

Native trailing alignment may need a zero-repeat suffix (e.g. `'llh0l'`) so struct size matches C. Standard mode requires manual padding—compare sizes with `calcsize()`.

```python
# Goal: standard layout with explicit padding (portable)
import struct

# Two 64-bit ints + 16-bit field + 6 pad bytes → 24 bytes total
fmt = "<qqh6x"
assert struct.calcsize(fmt) == 24
packed = struct.pack(fmt, 1, 2, 3)
assert struct.unpack(fmt, packed) == (1, 2, 3)
```

---

## Struct objects — [Classes](https://docs.python.org/3/library/struct.html#classes)

`struct.Struct(format)` compiles the format once. Methods mirror module-level functions; `.size` and `.format` are attributes.

| Method | Same as |
|--------|---------|
| `s.pack(*values)` | `struct.pack(s.format, *values)` |
| `s.unpack(buffer)` | `struct.unpack(s.format, buffer)` |
| `s.unpack_from(buffer, offset=0)` | `struct.unpack_from(...)` |
| `s.pack_into(buf, offset, *values)` | `struct.pack_into(...)` |
| `s.iter_unpack(buffer)` | `struct.iter_unpack(...)` |

```python
# Goal: reuse a compiled format in a loop
import struct

header = struct.Struct("<IHH")  # magic, version, flags
records = [header.pack(0xDEADBEEF, 1, 0), header.pack(0xCAFEBABE, 2, 4)]
for blob in records:
    magic, ver, flags = header.unpack(blob)
    assert ver in (1, 2)
```

---

## Best practices and pitfalls

| Practice | Why |
|----------|-----|
| Document format strings next to protocol specs | One-character typos change every offset |
| Use `unpack_from` on larger buffers | Avoid slicing copies in parsers |
| Prefer buffer protocol objects | `bytes`, `bytearray`, `memoryview` work without extra copies |
| Test on both 32- and 64-bit if using `@` | `l`/`q` sizes and padding differ |

| Pitfall | Mitigation |
|---------|------------|
| `'s'` vs `'c'` confusion | `'10s'` = one 10-byte blob; `'10c'` = ten 1-byte values |
| `'P'` (void*) only in native mode | Use fixed-width integers for portable pointers-as-IDs |
| Assuming float endian matches int | Specify prefix on the whole format string |

```python
# Goal: parse a field inside a larger packet without copying
import struct

packet = b"\x00" * 4 + struct.pack("<I", 42) + b"\xff"
offset = 4
value = struct.unpack_from("<I", packet, offset)[0]
assert value == 42
```
