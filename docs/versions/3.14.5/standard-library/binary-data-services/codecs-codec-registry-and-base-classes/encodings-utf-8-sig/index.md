# [encodings.utf_8_sig — UTF-8 codec with BOM signature](https://docs.python.org/3/library/codecs.html#module-encodings.utf_8_sig)

**`utf_8_sig`** (alias **`utf-8-sig`**) is a UTF-8 variant that **writes** the UTF-8 BOM (`EF BB BF`) once at the start of encoded output and **skips** an initial BOM on decode. Microsoft Notepad popularized this pattern for UTF-8 detection. General UTF-8 use should **avoid** BOM per Unicode guidance. Module summary on [docs.python.org](https://docs.python.org/3/library/codecs.html#module-encodings.utf_8_sig).

---

## Encode vs decode

| Operation | Behavior |
|-----------|----------|
| **Encode** | Prepend UTF-8 BOM before first output (stateful encoder: once per stream) |
| **Decode** | If first three bytes are BOM, consume them; otherwise standard UTF-8 |

After decode, any U+FEFF in content is a normal character (ZWNBSP), not stripped.

```python
# Goal: utf-8-sig adds BOM on encode, strips on decode
import codecs

text = "hello"
encoded = codecs.encode(text, "utf-8-sig")
assert encoded.startswith(codecs.BOM_UTF8)
assert codecs.decode(encoded, "utf-8-sig") == text
assert codecs.decode(encoded, "utf-8") == "\ufeff" + text
```

```python
# Goal: plain UTF-8 without BOM for comparison
import codecs

plain = "data".encode("utf-8")
assert not plain.startswith(codecs.BOM_UTF8)
sig = codecs.encode("data", "utf-8-sig")
assert sig.startswith(codecs.BOM_UTF8)
```

---

## When to use

| Scenario | Recommendation |
|----------|----------------|
| Excel / Notepad **CSV** interchange on Windows | `utf-8-sig` helps auto-detection |
| **JSON**, HTTP, Unix config files | Use **`utf-8`** without BOM |
| Detecting encoding from raw bytes | BOM + valid UTF-8 structure is a strong hint |

---

## Best practices

| Practice | Why |
|----------|-----|
| Be consistent within a **file format** | Mixing BOM and non-BOM breaks hashes |
| Read with **`utf-8-sig`**, write with **`utf-8`** | Normalize storage |
| Do not double-encode BOM | Stateful writer emits BOM once |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| **`utf-8` decoder** leaves BOM as `\ufeff` | Use `utf-8-sig` reader for legacy files |
| Assuming BOM on **every** UTF-8 file | Most UTF-8 text has no BOM |
| **`utf-8-sig` in protocols** | Peers may reject leading BOM |
