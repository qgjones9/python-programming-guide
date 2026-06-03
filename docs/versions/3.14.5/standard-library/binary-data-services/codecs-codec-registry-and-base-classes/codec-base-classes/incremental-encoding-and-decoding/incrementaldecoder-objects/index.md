# [IncrementalDecoder Objects](https://docs.python.org/3/library/codecs.html#incrementaldecoder-objects)

`codecs.IncrementalDecoder` decodes **partial byte streams** while buffering incomplete multibyte sequences. Obtain instances with `codecs.getincrementaldecoder(encoding)(errors='strict')`. Full contract on [docs.python.org](https://docs.python.org/3/library/codecs.html#incrementaldecoder-objects).

---

## Constructor and attributes

| Member | Role |
|--------|------|
| `IncrementalDecoder(errors='strict')` | Standard constructor |
| `.errors` | Active error handler; mutable |

---

## Methods

| Method | Behavior |
|--------|----------|
| `decode(object, final=False)` | Decode chunk; with `final=True`, flush buffers and finish |
| `reset()` | Clear buffered input and extra state |
| `getstate()` | Returns `(undecoded_buffer, extra_state_int)` |
| `setstate(state)` | Restore decoder; `(b'', 0)` must mean clean slate |

When `final=True` and bytes remain incomplete under `'strict'`, expect `UnicodeDecodeError`.

```python
# Goal: feed bytes from a simulated socket
import codecs

dec = codecs.getincrementaldecoder("utf-8")()
out = dec.decode(b"Hel")
out += dec.decode(b"lo \xc3")
out += dec.decode(b"\xa9", final=True)
assert out == "Hello é"
```

```python
# Goal: getstate/setstate preserves partial input
import codecs

dec = codecs.getincrementaldecoder("utf-8")()
dec.decode(b"\xc3")
state = dec.getstate()
dec2 = codecs.getincrementaldecoder("utf-8")()
dec2.setstate(state)
assert dec2.decode(b"\xa9", final=True) == "é"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Treat **`getstate()` buffer** as opaque bytes | Only round-trip through `setstate` |
| Use **`final=True`** on connection close | Surfaces truncated UTF-8 early |
| Pair with **`iterdecode`** for byte iterators | Handles loop and final flag |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Decoding without **`final`** on end-of-stream | Trailing partial code points silently buffered |
| Assuming **`getstate()[1] == 0`** always | Extra state may be non-zero for exotic codecs |
| Mixing decoders on same byte stream | One decoder instance per stream |
