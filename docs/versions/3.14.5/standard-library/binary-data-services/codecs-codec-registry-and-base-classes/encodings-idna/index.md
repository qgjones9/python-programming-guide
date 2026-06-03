# [encodings.idna — Internationalized Domain Names in Applications](https://docs.python.org/3/library/codecs.html#module-encodings.idna)

The **`encodings.idna`** module implements **IDNA 2003** ([RFC 3490](https://www.rfc-editor.org/rfc/rfc3490.html), [RFC 3492](https://www.rfc-editor.org/rfc/rfc3492.html) punycode) plus **nameprep** ([RFC 3454](https://www.rfc-editor.org/rfc/rfc3454.html)). The **`idna`** codec converts Unicode domain labels to **ACE** (`xn--…`) and back. For **IDNA 2008** (RFC 5891), use the third-party [idna](https://pypi.org/project/idna/) package. Full module API on [docs.python.org](https://docs.python.org/3/library/codecs.html#module-encodings.idna).

---

## Codec behavior

| Direction | Behavior |
|-----------|----------|
| Encode (`str` → `bytes`) | Split on label separators (RFC 3490 §3.1); ACE-encode each label |
| Decode (`bytes` → `str`) | Split on `.`; decode ACE labels to Unicode |

Only **`errors='strict'`** is supported for the `idna` codec.

```python
# Goal: ACE encoding via idna codec
import codecs

domain = "bücher.example"
ace_bytes = codecs.encode(domain, "idna")
assert b"xn--" in ace_bytes
assert codecs.decode(ace_bytes, "idna") == domain
```

---

## Module functions

| Function | Role |
|----------|------|
| `encodings.idna.nameprep(label)` | RFC 3454 nameprep (query string profile; `AllowUnassigned=True`) |
| `encodings.idna.ToASCII(label)` | Label → ASCII ACE (RFC 3490) |
| `encodings.idna.ToUnicode(label)` | ACE label → Unicode |

```python
# Goal: label-level ToASCII / ToUnicode
from encodings.idna import ToASCII, ToUnicode

ace = ToASCII("München")
uni = ToUnicode(ace)
assert uni == "münchen"
assert ace.startswith(b"xn--")
```

---

## Integration elsewhere

| Component | Behavior |
|-----------|----------|
| [`socket`](https://docs.python.org/3/library/socket.html) | Unicode host names converted to ACE on connect |
| [`http.client`](https://docs.python.org/3/library/http.client.html) | IDNA in `Host` header when sending Unicode names |
| Reverse DNS | **No** automatic Unicode; decode ACE in application code |

```python
# Goal: nameprep normalizes case and mapping
from encodings.idna import nameprep

# nameprep applies case folding and character mappings
prepped = nameprep("Straße")
assert isinstance(prepped, str)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **IDNA 2008 library** for modern DNS standards | Stdlib is IDNA 2003 |
| Validate labels before ToASCII | Prevents look-alike homograph issues at app layer |
| Present **Unicode** to users, ACE in logs/DNS | Transparency per RFC guidance |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Non-strict **`errors`** on idna codec | Unsupported |
| Assuming **socket** decodes reverse lookups | Manual `ToUnicode` |
| Mixing **IDNA 2003 and 2008** in one system | Pick one standard per product |
