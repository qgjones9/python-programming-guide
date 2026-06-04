# [json — JSON encoder and decoder](https://docs.python.org/3/library/json.html)

The [`json`](https://docs.python.org/3/library/json.html) module serializes Python objects to [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) JSON and parses JSON back into Python types (`dict`, `list`, `str`, `int`, `float`, `bool`, `None`). It is the usual choice for HTTP APIs, config files, and logs. Full parameter lists and security notes are on [docs.python.org](https://docs.python.org/3/library/json.html).

---

## Purpose

| Aspect | Behavior |
|--------|----------|
| Encode | `json.dumps` → `str`; `json.dump` → file-like text stream |
| Decode | `json.loads` → object; `json.load` → from file |
| Types | No `datetime`, `Decimal`, or `set` unless you customize |
| Order | Dict key order preserved (3.7+ insertion order) |
| CLI | `python -m json` pretty-prints or validates JSON |

---

## Basic encode and decode

```python
# Goal: dumps/loads round-trip for nested structures
import json

obj = ["foo", {"bar": ["baz", None, 1.0, 2]}]
text = json.dumps(obj)
assert json.loads(text) == obj
```

```python
# Goal: compact wire format and sorted keys for stable hashes
import json

data = {"c": 0, "b": 0, "a": 0}
compact = json.dumps(data, sort_keys=True, separators=(",", ":"))
assert compact == '{"a":0,"b":0,"c":0}'
```

```python
# Goal: stream to StringIO like a file handle
import json
from io import StringIO

buf = StringIO()
json.dump(["streaming API"], buf)
assert json.load(StringIO(buf.getvalue())) == ["streaming API"]
```

---

## Custom types — `default` and `object_hook`

```python
# Goal: encode complex numbers with a marker dict
import json

def encode_complex(obj):
    if isinstance(obj, complex):
        return {"__complex__": True, "real": obj.real, "imag": obj.imag}
    raise TypeError(f"Cannot serialize {type(obj)}")

wire = json.dumps(1 + 2j, default=encode_complex)
assert json.loads(wire)["real"] == 1.0
```

```python
# Goal: decode marker dict back to complex via object_hook
import json

def as_complex(dct):
    if dct.get("__complex__"):
        return complex(dct["real"], dct["imag"])
    return dct

value = json.loads(
    '{"__complex__": true, "real": 1, "imag": 2}',
    object_hook=as_complex,
)
assert value == (1 + 2j)
```

```python
# Goal: subclass JSONEncoder for reusable serialization
import json

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        return super().default(obj)

assert json.dumps(2 + 1j, cls=ComplexEncoder) == "[2.0, 1.0]"
```

---

## Parsing options and safety

| Parameter | Use |
|-----------|-----|
| `parse_float` | e.g. `decimal.Decimal` for money |
| `parse_int` | Custom integer handling |
| `object_pairs_hook` | Ordered processing of object keys |

**Untrusted JSON:** limit input size and nesting; decoding can be expensive. Prefer `json.JSONDecoder` with strict checks for specialized parsers.

```python
# Goal: parse floats as Decimal for exact arithmetic
import decimal
import json

value = json.loads("1.1", parse_float=decimal.Decimal)
assert value == decimal.Decimal("1.1")
```

---

## Pretty printing and CLI

```python
# Goal: indented output for human-readable config
import json

pretty = json.dumps({"6": 7, "4": 5}, sort_keys=True, indent=4)
assert '"4": 5' in pretty and pretty.startswith("{\n")
```

Run `python -m json` on stdin to validate and pretty-print; invalid JSON exits non-zero with a parse error message.

---

## Standard compliance notes

| Topic | Detail |
|-------|--------|
| `NaN` / `Infinity` | Allowed by Python’s encoder by default; not strict JSON — use `allow_nan=False` for strict output |
| Duplicate keys | Last duplicate wins in `loads` |
| YAML subset | Default `dumps` output is also valid YAML 1.2 (do not rely on this for security boundaries) |

---

## See also

- [`mailbox`](../mailbox-manipulate-mailboxes-in-various-formats/index.md) — sometimes stores metadata as JSON in custom tools
- [Command-line interface](https://docs.python.org/3/library/json.html#module-json.tool) — `python -m json`
