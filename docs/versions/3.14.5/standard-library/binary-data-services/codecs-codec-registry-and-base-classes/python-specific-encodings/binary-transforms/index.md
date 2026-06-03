# [Binary Transforms](https://docs.python.org/3/library/codecs.html#python-specific-encodings-binary-transforms)

**Binary transforms** map **bytes-like → bytes** (encode and decode are symmetric in role). They are **not** available through `bytes.decode()`—use `codecs.encode()` / `codecs.decode()` with the codec name. Restored in 3.2+ after Python 2 `string_escape` removal. Table on [docs.python.org](https://docs.python.org/3/library/codecs.html#python-specific-encodings-binary-transforms).

---

## Built-in transforms

| Codec | Aliases | Effect |
|-------|---------|--------|
| `base64_codec` | `base64`, `base_64` | MIME base64; output includes trailing `\n` |
| `hex_codec` | `hex` | Two hex digits per byte |
| `quopri_codec` | `quopri`, `quoted_printable` | MIME quoted-printable |
| `uu_codec` | `uu` | uuencode format |
| `bz2_codec` | `bz2` | bz2 compression |
| `zlib_codec` | `zip`, `zlib` | zlib compression |

Since 3.4, encoders accept any **bytes-like** object.

```python
# Goal: hex round-trip
import codecs

data = b"\xde\xad\xbe\xef"
hex_bytes = codecs.encode(data, "hex")
assert hex_bytes == b"deadbeef"
assert codecs.decode(hex_bytes, "hex") == data
```

```python
# Goal: base64 through codecs (note trailing newline)
import codecs

raw = b"hello"
b64 = codecs.encode(raw, "base64")
assert b64.endswith(b"\n")
assert codecs.decode(b64.strip() + b"\n", "base64") == raw
```

```python
# Goal: zlib compress/decompress via codec
import codecs

plain = b"repeat " * 20
compressed = codecs.encode(plain, "zlib")
assert len(compressed) < len(plain)
assert codecs.decode(compressed, "zlib") == plain
```

---

## vs dedicated modules

| Task | Prefer |
|------|--------|
| RFC 4648 base64 without MIME newlines | [`base64`](https://docs.python.org/3/library/base64.html) module |
| Hex for crypto/display | `bytes.hex()` / `bytes.fromhex()` (3.5+) |
| gzip file format | [`gzip`](https://docs.python.org/3/library/gzip.html) module |
| Codec registry uniformity | `codecs.encode(..., "hex")` |

---

## Best practices

| Practice | Why |
|----------|-----|
| Strip **`base64_codec`** newline if size-sensitive | Codec always appends `\n` |
| Do not **`iterdecode`** binary transforms from str iterators | Requires bytes chunks |
| Validate decompressed **size limits** | zlib/bz2 bombs |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Expecting **`str.decode('base64')`** | Use `codecs.decode` |
| **`uu_codec`** for modern pipelines | Legacy Unix email format |
| Confusing **`zip`** alias with ZIP files | zlib compression only |
