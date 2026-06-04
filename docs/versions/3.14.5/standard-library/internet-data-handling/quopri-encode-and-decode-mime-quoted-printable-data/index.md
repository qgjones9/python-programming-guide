# [quopri — Encode and decode MIME quoted-printable data](https://docs.python.org/3/library/quopri.html)

The [`quopri`](https://docs.python.org/3/library/quopri.html) module implements **quoted-printable** encoding and decoding per RFC 1521 (bodies) and RFC 1522 (**Q**-encoded headers when `header=True`). It suits mostly-ASCII text; dense binary data should use [`base64`](../base64-base16-base32-base64-base85-data-encodings/index.md). API reference: [docs.python.org](https://docs.python.org/3/library/quopri.html).

---

## Purpose

| Function | Role |
|----------|------|
| `encodestring(s, quotetabs=False, header=False)` | Bytes → quoted-printable bytes |
| `decodestring(s, header=False)` | Reverse |
| `encode(input, output, quotetabs, header=False)` | Stream to stream (binary file objects) |
| `decode(input, output, header=False)` | Stream decode |

For full MIME messages, prefer [`email`](../email-an-email-and-mime-handling-package/index.md) content managers; use `quopri` for **raw body chunks** or custom pipelines.

---

## Body encoding

Non-printable octets become `=XX` escapes. Trailing spaces and tabs on lines are always encoded. Set `quotetabs=True` to encode embedded spaces and tabs as well.

```python
# Goal: encode non-ASCII bytes and decode back
import quopri

raw = b"Caf\xe9 and a tab:\tend"
encoded = quopri.encodestring(raw, quotetabs=True)
assert b"=E9" in encoded or b"=e9" in encoded.lower()
assert quopri.decodestring(encoded) == raw
```

```python
# Goal: mostly printable text stays readable
import quopri

plain = b"Mostly printable: hello!"
wire = quopri.encodestring(plain)
assert b"hello" in wire
assert quopri.decodestring(wire) == plain
```

---

## Header (Q) encoding

With `header=True`, spaces become underscores on encode and underscores become spaces on decode (RFC 1522 “Q” encoding for header fragments).

```python
# Goal: Q-encoding for header-safe bytes
import quopri

text = b"Caf\xe9 today"
q = quopri.encodestring(text, header=True)
decoded = quopri.decodestring(q, header=True)
assert decoded == text
```

---

## Stream API

```python
# Goal: encode via binary file objects
import io
import quopri

src = io.BytesIO(b"line one\nline two\n")
dst = io.BytesIO()
quopri.encode(src, dst, quotetabs=False)
assert quopri.decodestring(dst.getvalue()) == b"line one\nline two\n"
```

---

## vs binascii and email

| Layer | Module |
|-------|--------|
| Message-level MIME | `email` — picks CTE and boundaries |
| Block quoted-printable | `quopri` or `binascii.b2a_qp` |
| Base64 binary | `base64` |

[`binascii.b2a_qp`](../binascii-convert-between-binary-and-ascii/index.md) offers `istext` and `header` flags at a lower level; `quopri` matches RFC 1521 file semantics.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **base64** for images and compressed data | Quoted-printable expands binary-heavy content |
| Pass **bytes** to `encodestring` / `decodestring` | Avoid implicit encoding guesses |
| Set `header=True` only for **RFC 1522 header** segments | Body decoding uses different underscore rules |

---

## See also

- [`base64`](../base64-base16-base32-base64-base85-data-encodings/index.md) — binary attachments
- [`email`](../email-an-email-and-mime-handling-package/index.md) — end-to-end message assembly
