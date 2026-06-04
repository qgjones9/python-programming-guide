# [mimetypes — Map filenames to MIME types](https://docs.python.org/3/library/mimetypes.html)

The [`mimetypes`](https://docs.python.org/3/library/mimetypes.html) module maps **filename extensions** and **URLs** to **`type/subtype`** strings suitable for `Content-Type` headers, and can reverse-map types to extensions. It reads system **`mime.types`** files plus built-in tables. Reference: [docs.python.org](https://docs.python.org/3/library/mimetypes.html).

---

## Purpose

| Function | Returns |
|----------|---------|
| `guess_type(url, strict=True)` | `(type, encoding)` — encoding is compression (e.g. `gzip`), not CTE |
| `guess_file_type(path, strict=True)` | Same, but for paths (3.13+) |
| `guess_extension(type)` | Leading-dot extension or `None` |
| `guess_all_extensions(type)` | All known extensions for a type |
| `add_type(type, ext, strict=True)` | Register custom mapping |

When `strict=True` (default), only **IANA-registered** types are considered from the standard tables; `strict=False` also uses `common_types` (e.g. `image/pict`).

---

## Guessing from names

```python
# Goal: PNG file → image/png, no Content-Encoding
import mimetypes

mime, encoding = mimetypes.guess_type("photo.png")
assert mime == "image/png" and encoding is None
```

```python
# Goal: compound extension splits type and compression
import mimetypes

mime, encoding = mimetypes.guess_type("archive.tar.gz")
assert mime == "application/x-tar" and encoding == "gzip"
```

```python
# Goal: guess type from a path (guess_file_type on 3.13+, else guess_type)
import mimetypes
from pathlib import Path

path = Path("data.json")
guess = getattr(mimetypes, "guess_file_type", None)
if guess is not None:
    mime, enc = guess(path)
else:
    mime, enc = mimetypes.guess_type(str(path))
assert mime == "application/json" and enc is None
```

---

## Reverse lookup

```python
# Goal: MIME type → preferred extension
import mimetypes

ext = mimetypes.guess_extension("text/javascript")
assert ext == ".js"
all_ext = mimetypes.guess_all_extensions("image/jpeg")
assert ".jpg" in all_ext or ".jpeg" in all_ext
```

```python
# Goal: register a custom type for tooling
import mimetypes

mimetypes.add_type("application/x-myapp", ".mya", strict=False)
mime, _ = mimetypes.guess_type("config.mya", strict=False)
assert mime == "application/x-myapp"
```

---

## MimeTypes class

Use `mimetypes.MimeTypes(filenames=(), strict=True)` when an application needs an **isolated** database (e.g. test fixtures) without mutating global maps.

```python
# Goal: isolated MimeTypes instance
import mimetypes

db = mimetypes.MimeTypes(strict=True)
db.add_type("text/x-custom", ".cst", strict=False)
assert db.guess_type("file.cst", strict=False)[0] == "text/x-custom"
```

---

## Initialization and data files

| Symbol | Role |
|--------|------|
| `mimetypes.init(files=None)` | Load `knownfiles` and optional extra paths |
| `mimetypes.knownfiles` | Typical `/etc/mime.types` locations |
| `mimetypes.suffix_map` | e.g. `.tgz` → `.tar.gz` |
| `mimetypes.encodings_map` | `.gz` → `gzip` |
| `mimetypes.types_map` | extension → MIME |

On Windows, `init()` also consults the registry (since 3.2).

---

## Command line

```text
python -m mimetypes filename.png
python -m mimetypes --extension text/javascript
python -m mimetypes --lenient filename.pict
```

`--lenient` enables `common_types` for rare extensions.

---

## Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| `encoding` is **gzip**, not `quoted-printable` | Set transfer encoding in `email` separately |
| Unknown extension returns `(None, None)` | `add_type` or ship a custom `mime.types` |
| Passing paths to `guess_type` | Soft-deprecated since 3.13 — use `guess_file_type` |
| OS-only types | Only extensions known to Python + OS tables are recognized |

---

## See also

- [`email`](../email-an-email-and-mime-handling-package/index.md) — `Content-Type` on `EmailMessage`
- [`urllib.request`](../../internet-protocols-and-support/urllib/index.md) — HTTP responses often need guessed types for downloads
