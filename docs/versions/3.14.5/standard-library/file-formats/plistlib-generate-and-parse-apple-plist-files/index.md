# [plistlib — Generate and parse Apple .plist files](https://docs.python.org/3/library/plistlib.html)

The [`plistlib`](https://docs.python.org/3/library/plistlib.html) module reads and writes **Apple property list** files—XML or binary serialization of dicts, lists, strings, numbers, booleans, bytes, and datetimes. The top-level value is usually a **dict** with string keys. Use **`load`/`dump`** for files and **`loads`/`dumps`** for in-memory bytes. Full format constants and `UID` support remain on [docs.python.org](https://docs.python.org/3/library/plistlib.html).

---

## API — [Module functions](https://docs.python.org/3/library/plistlib.html)

| Function | Role |
|----------|------|
| `load(fp, *, fmt=None, dict_type=dict, aware_datetime=False)` | Read binary file; autodetect format when `fmt=None` |
| `loads(data, *, fmt=None, ...)` | Parse bytes (or XML `str` when `fmt=FMT_XML`, 3.13+) |
| `dump(value, fp, *, fmt=FMT_XML, sort_keys=True, ...)` | Write plist to binary file object |
| `dumps(value, *, fmt=FMT_XML, ...)` | Return plist as `bytes` |

| Constant | Meaning |
|----------|---------|
| `FMT_XML` | XML plist |
| `FMT_BINARY` | Binary plist (smaller/faster) |

| Class | Role |
|-------|------|
| `UID(data)` | Wraps int for NSKeyedArchiver compatibility (3.8+) |
| `InvalidFileException` | Raised on parse failure |

Supported value types: `str`, `int`, `float`, `bool`, `bytes`, `bytearray`, `datetime`, `tuple`, `list`, `dict` (string keys only).

```python
# Goal: round-trip a dict through XML plist bytes
import plistlib

payload = {"name": "Doodah", "count": 42, "enabled": True}
blob = plistlib.dumps(payload, fmt=plistlib.FMT_XML)
restored = plistlib.loads(blob)
assert restored == payload
```

```python
# Goal: write and read binary plist via file object
import io
import plistlib

data = {"items": ["A", "B", 12], "ratio": 0.5}
buf = io.BytesIO()
plistlib.dump(data, buf, fmt=plistlib.FMT_BINARY)
buf.seek(0)
assert plistlib.load(buf) == data
```

```python
# Goal: parse minimal XML plist fragment
import plistlib

xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>foo</key><string>bar</string>
</dict></plist>"""
assert plistlib.loads(xml)["foo"] == "bar"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Open files in **binary mode** (`'rb'`/`'wb'`) | API requires binary file objects |
| Use **`FMT_BINARY`** for production macOS tools | Smaller and faster than XML |
| Keep dict keys as **strings** | Non-string keys raise `TypeError` unless `skipkeys=True` |
| Set **`aware_datetime=True`** when timezone matters | Converts aware datetimes to UTC on write (3.13+) |
| Autodetect with **`fmt=None`** on read | Handles mixed XML/binary inputs |
| Validate **`InvalidFileException`** on untrusted files | Malformed XML triggers Expat errors |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Non-string dict keys | `TypeError` on dump | Normalize keys or `skipkeys=True` |
| Integer too large for binary plist | `OverflowError` | Stay within plist int range |
| Text mode file objects | Broken reads/writes | Use `'rb'`/`'wb'` |
| Assuming comments preserved | XML comments dropped on load/dump | Use dedicated Apple tools for round-trip editing |
| Nested unsupported types | `TypeError` | Convert custom objects before dump |
| Mixing naive and aware datetimes | Surprising UTC conversion | Pass `aware_datetime` consistently |
