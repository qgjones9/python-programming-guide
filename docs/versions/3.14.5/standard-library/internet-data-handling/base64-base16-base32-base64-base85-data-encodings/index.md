# [base64 — Base16, Base32, Base64, Base85 Data Encodings](https://docs.python.org/3/library/base64.html)

The [`base64`](https://docs.python.org/3/library/base64.html) module encodes binary data into printable ASCII and decodes it back. It implements **RFC 4648** (Base16/32/64, including URL-safe variants), **Ascii85** (PDF/PostScript), **RFC 1924-style base85** (Git), and **Z85** (ZeroMQ). Full API and security notes are on [docs.python.org](https://docs.python.org/3/library/base64.html).

---

## Purpose

| Interface | Role |
|-----------|------|
| Modern (`b64encode`, `b32decode`, …) | Bytes in → bytes out; accepts ASCII `str` on decode |
| Legacy (`encodebytes`, file `encode`/`decode`) | MIME-style Base64 with newlines every 76 characters |
| URL-safe | `-` and `_` instead of `+` and `/` for paths and tokens |

For **MIME email bodies**, prefer the [`email`](../email-an-email-and-mime-handling-package/index.md) package; for **registry-style** transforms with a trailing newline, see [`codecs` binary transforms](../../binary-data-services/codecs-codec-registry-and-base-classes/python-specific-encodings/binary-transforms/index.md).

---

## RFC 4648 — Base64 and friends

```python
# Goal: standard Base64 round-trip
import base64

raw = b"data to be encoded"
encoded = base64.b64encode(raw)
assert encoded == b"ZGF0YSB0byBiZSBlbmNvZGVk"
assert base64.b64decode(encoded) == raw
```

```python
# Goal: URL- and filesystem-safe alphabet (no + /)
import base64

token = base64.urlsafe_b64encode(b"user:session")
assert b"+" not in token and b"/" not in token
assert base64.urlsafe_b64decode(token) == b"user:session"
```

```python
# Goal: custom altchars for non-standard alphabets
import base64

alt = b"-_"
encoded = base64.b64encode(b"test", altchars=alt)
assert base64.b64decode(encoded, altchars=alt) == b"test"
```

```python
# Goal: Base32 for case-insensitive transport
import base64

wire = base64.b32encode(b"hi")
assert base64.b32decode(wire) == b"hi"
```

---

## Base85 family

| Function | Typical consumer |
|----------|------------------|
| `a85encode` / `a85decode` | PDF, PostScript (`<~` … `~>` optional) |
| `b85encode` / `b85decode` | Git binary patches |
| `z85encode` / `z85decode` | ZeroMQ frames (length multiple of 4 bytes in) |

```python
# Goal: Ascii85 without Adobe framing
import base64

data = b"four!!"
encoded = base64.a85encode(data, adobe=False)
assert base64.a85decode(encoded, adobe=False) == data
```

---

## Legacy MIME interface

`encodebytes` / `decodebytes` insert a newline after every 76 characters and ensure a trailing newline per RFC 2045. Use when reproducing classic MIME tools, not for compact API tokens.

```python
# Goal: MIME-style output includes periodic newlines
import base64

mime_style = base64.encodebytes(b"xy" * 40)
assert mime_style.endswith(b"\n")
assert b"\n" in mime_style[:-1]
```

---

## Security and validation

| Topic | Guidance |
|-------|----------|
| RFC 4648 §12 | Review non-alphabet handling and padding when accepting untrusted input |
| `validate=True` on `b64decode` | Rejects garbage characters instead of stripping them |
| Strict base64 at C layer | See [`binascii.a2b_base64`](../binascii-convert-between-binary-and-ascii/index.md) `strict_mode` |

```python
# Goal: strict decode rejects invalid alphabet bytes
import base64
import binascii

bad = b"!!!"
try:
    base64.b64decode(bad, validate=True)
except binascii.Error:
    ok = True
else:
    ok = False
assert ok
```

---

## vs other modules

| Need | Module |
|------|--------|
| No MIME newlines, URL-safe | `base64` (this module) |
| Hex with separators | `binascii.hexlify` or `bytes.hex()` |
| Quoted-printable | [`quopri`](../quopri-encode-and-decode-mime-quoted-printable-data/index.md) |
| Codec registry uniform API | `codecs.encode(..., "base64")` |

---

## See also

- [`binascii`](../binascii-convert-between-binary-and-ascii/index.md) — low-level C accelerators used internally
- [RFC 4648 security considerations](https://www.rfc-editor.org/rfc/rfc4648#section-12)
