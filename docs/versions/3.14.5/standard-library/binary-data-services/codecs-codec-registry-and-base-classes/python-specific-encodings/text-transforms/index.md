# [Text Transforms](https://docs.python.org/3/library/codecs.html#python-specific-encodings-text-transforms)

**Text transforms** map **`str` → `str`**. They are invoked with `codecs.encode()` / `codecs.decode()` (same codec both directions for `rot_13`). They are **not** supported by `str.encode()` (which only produces bytes). Documented on [docs.python.org](https://docs.python.org/3/library/codecs.html#python-specific-encodings-text-transforms).

---

## rot_13

| Codec | Aliases | Effect |
|-------|---------|--------|
| `rot_13` | `rot13` | Caesar cipher rotating A–Z and a–z by 13 |

Applying encode twice (or decode twice) restores the original ASCII letters; non-letters pass through unchanged.

```python
# Goal: rot13 obfuscation round-trip
import codecs

msg = "Hello, World!"
encoded = codecs.encode(msg, "rot_13")
assert encoded == "Uryyb, Jbeyq!"
assert codecs.decode(encoded, "rot_13") == msg
```

```python
# Goal: use iterencode for text transforms (not iterdecode)
import codecs

parts = list(codecs.iterencode(iter(["ab", "cd"]), "rot_13"))
assert "".join(parts) == codecs.encode("abcd", "rot_13")
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`iterencode`** for streaming str chunks | `iterdecode` expects bytes iterators |
| Treat as **reversible toy transform**, not crypto | Trivially broken |
| Alias **`rot13`** works after normalization | Same codec |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| **`str.encode('rot_13')`** | Raises; use `codecs.encode` |
| **`iterdecode` on rot_13** | Wrong iterator element type |
| Expecting Unicode letters outside ASCII | Only A–Z / a–z rotate |
