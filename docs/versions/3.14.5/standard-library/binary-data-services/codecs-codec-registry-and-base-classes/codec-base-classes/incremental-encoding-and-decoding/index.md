# [Incremental Encoding and Decoding](https://docs.python.org/3/library/codecs.html#incremental-encoding-and-decoding)

**Incremental** codecs process input in **multiple chunks** while retaining internal state (partial multibyte sequences, compression dictionaries, etc.). The joined output matches what a single stateless call would produce on the concatenated input. Base classes: `codecs.IncrementalEncoder` and `codecs.IncrementalDecoder`. Full API on [docs.python.org](https://docs.python.org/3/library/codecs.html#incremental-encoding-and-decoding).

---

## Why incremental?

| Scenario | Benefit |
|----------|---------|
| Socket / pipe reads | Decode before full message arrives |
| Large file processing | Bound memory; stream through `iterencode` |
| Interactive protocols | Flush encoder with `final=True` at message end |

```python
# Goal: decode UTF-8 split across two chunks
import codecs

dec = codecs.getincrementaldecoder("utf-8")()
part_a = dec.decode(b"\xc3")
part_b = dec.decode(b"\xa9", final=True)
assert part_a + part_b == "é"
```

---

## Shared lifecycle

| Method | Encoder | Decoder |
|--------|---------|---------|
| `encode/decode(obj, final=False)` | Process chunk; set `final=True` on last call | Same; decoder must flush on final |
| `reset()` | Drop state and buffered output | Return to initial state |
| `getstate()` / `setstate()` | Optional persistence (pickle-friendly int or tuple) | Decoder state is `(buffer, extra)` tuple |

Changing the `.errors` attribute switches strategies mid-life of the object.

```python
# Goal: incremental encode matches one-shot encode
import codecs

text = "hello 世界"
enc = codecs.getincrementalencoder("utf-8")()
inc = enc.encode(text[:3]) + enc.encode(text[3:], final=True)
one_shot = text.encode("utf-8")
assert inc == one_shot
```

---

## `final=True` semantics

On the **last** `decode()` call, `final=True` forces completion: trailing incomplete sequences trigger error handling (usually `UnicodeDecodeError` under `'strict'`). Encoders flush any buffered output when `final=True`.

```python
# Goal: incomplete sequence fails on final flush
import codecs

dec = codecs.getincrementaldecoder("utf-8")()
dec.decode(b"\xc3")  # partial é
failed = False
try:
    dec.decode(b"", final=True)
except UnicodeDecodeError:
    failed = True
assert failed
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Always **`final=True`** on last chunk | Flushes state; detects truncated input |
| Call **`reset()`** between logical messages | Avoids carry-over bytes |
| Use **`codecs.iterencode` / `iterdecode`** for iterators | Generator wrappers around incremental objects |
| Persist with **`getstate`/`setstate`** only when documented | Not all third-party codecs implement rich state |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [IncrementalEncoder Objects](incrementalencoder-objects/index.md) | Encoder methods and state |
| [IncrementalDecoder Objects](incrementaldecoder-objects/index.md) | Decoder buffer and `final` flush |
