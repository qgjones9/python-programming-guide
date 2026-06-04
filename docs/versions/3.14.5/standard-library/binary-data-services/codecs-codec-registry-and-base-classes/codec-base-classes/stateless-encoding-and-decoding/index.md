# [Stateless Encoding and Decoding](https://docs.python.org/3/library/codecs.html#stateless-encoding-and-decoding)

The **`codecs.Codec`** base class defines the **stateless** contract: each `encode()` or `decode()` call must be independent, handle **zero-length** input, and return `(output, length_consumed)`. Registry-level `codecs.encode()` / `decode()` and `CodecInfo.encode` / `decode` callables follow this shape. Details remain on [docs.python.org](https://docs.python.org/3/library/codecs.html#stateless-encoding-and-decoding).

---

## Method contract

| Method | Input | Output tuple |
|--------|-------|--------------|
| `Codec.encode(input, errors='strict')` | `str` (text codec) or bytes-like | `(encoded_object, chars_consumed)` |
| `Codec.decode(input, errors='strict')` | bytes-like (text codec) | `(decoded_object, bytes_consumed)` |

State must **not** persist on the `Codec` instance—use [incremental](../incremental-encoding-and-decoding/index.md) or [stream](../stream-encoding-and-decoding/index.md) classes when multibyte sequences span calls.

```python
# Goal: stateless encode/decode via registry functions
import codecs

data = "hello"
encoded = codecs.encode(data, "utf-8")
decoded, n = codecs.lookup("utf-8").decode(encoded)
assert decoded == data and n == len(encoded)
```

```python
# Goal: empty input returns empty output (required by contract)
import codecs

enc_fn = codecs.getencoder("utf-8")
dec_fn = codecs.getdecoder("utf-8")
assert enc_fn("", "strict") == (b"", 0)
assert dec_fn(b"", "strict") == ("", 0)
```

---

## Text vs binary codecs

| Direction | Typical input | Typical output | Example codec |
|-----------|---------------|----------------|---------------|
| Text encoding | `str` | `bytes` | `latin-1`, `utf-8` |
| Binary transform | bytes-like | `bytes` | `hex_codec`, `base64_codec` |
| Text transform | `str` | `str` | `rot_13` |

`bytes.decode()` only supports text decoders (output `str`). Binary transforms use `codecs.encode()` / `codecs.decode()` with the codec name.

```python
# Goal: hex transform (bytes to bytes) through codecs module
import codecs

blob = b"\x00\xff"
hexed = codecs.encode(blob, "hex")
assert hexed == b"00ff"
assert codecs.decode(hexed, "hex") == blob
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`str.encode` / `bytes.decode`** for simple UTF-8 | Thin wrappers over the same registry |
| Use **`codecs.encode`** for binary transforms | Not exposed on `bytes`/`str` methods |
| Check **consumed length** when parsing concatenated buffers | Partial consumption signals framing bugs |
| Keep stateless functions **pure** | Enables reuse from incremental/stream layers |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Storing partial multibyte state on `Codec` | Violates contract—use `IncrementalDecoder` |
| Passing `str` to binary transform encode | Use bytes-like input |
| Ignoring second tuple element | Useful for incremental composition and validation |
