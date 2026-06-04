# [uuid — UUID objects according to **RFC 9562**](https://docs.python.org/3/library/uuid.html)

[`uuid`](https://docs.python.org/3/library/uuid.html) creates and parses **128-bit universally unique identifiers** per [RFC 9562](https://www.rfc-editor.org/rfc/rfc9562.html) (successor to RFC 4122). Supports versions 1–5, 6–8 where implemented, bytes/int/str forms, and `UUID` fields (time, clock_seq, node). Reference: [uuid module](https://docs.python.org/3/library/uuid.html).

---

## Generation functions

| Function | Version | Source |
|----------|---------|--------|
| `uuid.uuid1()` | 1 | Timestamp + MAC (or random node) |
| `uuid.uuid3(ns, name)` | 3 | MD5 hash of namespace + name |
| `uuid.uuid4()` | 4 | Random |
| `uuid.uuid5(ns, name)` | 5 | SHA-1 hash of namespace + name |

Predefined namespaces: `uuid.NAMESPACE_DNS`, `URL`, `OID`, `X500`.

---

## Example — generate, stringify, parse

```python
# Goal: uuid4 round-trip and deterministic uuid5
import uuid

random_id = uuid.uuid4()
text = str(random_id)
restored = uuid.UUID(text)
assert restored == random_id
assert restored.version == 4

name_id = uuid.uuid5(uuid.NAMESPACE_DNS, "example.com")
assert name_id.version == 5
assert uuid.uuid5(uuid.NAMESPACE_DNS, "example.com") == name_id
assert name_id.bytes == uuid.UUID(bytes=name_id.bytes).bytes
```

---

## UUID object API

| Attribute / method | Role |
|--------------------|------|
| `.hex`, `.bytes`, `.int`, `str(u)` | Serializations |
| `.urn` | `urn:uuid:…` form |
| `.variant`, `.version` | Metadata |
| `UUID(fields=(time_low, …))` | Construct from components |

Use **uuid4** for opaque IDs; **uuid5** when the same namespace+name must always yield the same UUID.
