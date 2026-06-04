# [binascii — Convert between binary and ASCII](https://docs.python.org/3/library/binascii.html)

The [`binascii`](https://docs.python.org/3/library/binascii.html) module provides **C-accelerated** conversions between binary data and ASCII representations: hex, Base64, quoted-printable, uuencode, and CRC helpers. Higher-level modules such as [`base64`](../base64-base16-base32-base64-base85-data-encodings/index.md) and [`quopri`](../quopri-encode-and-decode-mime-quoted-printable-data/index.md) wrap these primitives. Reference: [docs.python.org](https://docs.python.org/3/library/binascii.html).

---

## Purpose

| Function family | Role |
|-----------------|------|
| `hexlify` / `unhexlify` | Hex encode/decode with optional separators |
| `b2a_base64` / `a2b_base64` | Base64 lines (optional trailing newline) |
| `b2a_qp` / `a2b_qp` | Quoted-printable blocks |
| `b2a_uu` / `a2b_uu` | Unix uuencode lines (≤45 bytes) |
| `crc32` / `crc_hqx` | Checksums (ZIP-style CRC-32, 16-bit CRC-CCITT) |

`a2b_*` functions accept ASCII-only `str`; other functions require **bytes-like** objects.

---

## Hex encoding

```python
# Goal: hexlify matches manual nybble expansion
import binascii

data = b"\xb9\x01\xef"
assert binascii.hexlify(data) == b"b901ef"
assert binascii.unhexlify(b"b901ef") == data
```

```python
# Goal: separators for readable dumps (3.8+)
import binascii

assert binascii.hexlify(b"\xb9\x01\xef", b"-") == b"b9-01-ef"
assert binascii.b2a_hex(b"\xb9\x01\xef", b" ", -2) == b"b901 ef"
```

For everyday code, `bytes.hex()` and `bytes.fromhex()` are often clearer; use `binascii` when you need **separator placement** or share code with older CPython targets.

---

## Base64 (low level)

```python
# Goal: b2a_base64 adds newline by default (MIME-friendly)
import binascii

line = binascii.b2a_base64(b"hello", newline=True)
assert line.endswith(b"\n")
assert binascii.a2b_base64(line) == b"hello"
```

```python
# Goal: strict_mode rejects padding and garbage (3.11+)
import binascii

valid = binascii.b2a_base64(b"x", newline=False)
assert binascii.a2b_base64(valid, strict_mode=True) == b"x"
```

Prefer [`base64.b64encode`](../base64-base16-base32-base64-base85-data-encodings/index.md) when you want RFC 4648 helpers without managing newlines.

---

## Quoted-printable and uuencode

```python
# Goal: quoted-printable round-trip for mostly ASCII
import binascii

raw = b"Lines with = signs and tabs\t"
qp = binascii.b2a_qp(raw, quotetabs=True)
assert binascii.a2b_qp(qp) == raw
```

```python
# Goal: uuencode single line (max 45 bytes of data)
import binascii

chunk = b"A" * 45
line = binascii.b2a_uu(chunk)
assert binascii.a2b_uu(line) == chunk
```

---

## CRC helpers

```python
# Goal: incremental CRC-32 matches one-shot (ZIP algorithm)
import binascii

full = binascii.crc32(b"hello world")
part = binascii.crc32(b"hello")
part = binascii.crc32(b" world", part)
assert full == part
assert full & 0xFFFFFFFF == full  # unsigned since 3.0
```

```python
# Goal: 16-bit CRC-CCITT for binhex-style pipelines
import binascii

crc = binascii.crc_hqx(b"data", 0)
assert 0 <= crc < 0x10000
```

---

## Exceptions

| Exception | Meaning |
|-----------|---------|
| `binascii.Error` | Invalid input (bad hex length, illegal base64, etc.) |
| `binascii.Incomplete` | Truncated input — read more data and retry |

---

## See also

- [`base64`](../base64-base16-base32-base64-base85-data-encodings/index.md) — RFC 4648 / Base85 high-level API
- [`quopri`](../quopri-encode-and-decode-mime-quoted-printable-data/index.md) — file-oriented quoted-printable
