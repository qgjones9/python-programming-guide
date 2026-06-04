# [File Formats](https://docs.python.org/3/library/fileformats.html)

The standard library ships parsers for **tabular**, **INI-style**, **TOML**, **FTP credential**, and **Apple plist** file formats—miscellaneous structured files that are not markup languages or email. Use [`csv`](csv-csv-file-reading-and-writing/index.md) for spreadsheet/database interchange; [`configparser`](configparser-configuration-file-parser/index.md) for INI-style app settings; [`tomllib`](tomllib-parse-toml-files/index.md) (3.11+, read-only) for modern config such as `pyproject.toml`; [`netrc`](netrc-netrc-file-processing/index.md) for FTP login files; [`plistlib`](plistlib-generate-and-parse-apple-plist-files/index.md) for macOS/iOS property lists. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/fileformats.html).

Related material: [`json`](../data-types/json-json-encoder-and-decoder/index.md) for JSON config, [`pickle`](../data-persistence/pickle-python-object-serialization/index.md) for Python-native serialization (not cross-language), and [`io`](../built-in-types/binary-sequence-types-bytes-bytearray-memoryview/index.md) for text vs binary file modes.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`csv`](csv-csv-file-reading-and-writing/index.md) | Read/write comma- or custom-delimited tabular data |
| [`configparser`](configparser-configuration-file-parser/index.md) | INI-style sections and key/value settings |
| [`tomllib`](tomllib-parse-toml-files/index.md) | Parse TOML 1.0.0 (read-only; 3.11+) |
| [`netrc`](netrc-netrc-file-processing/index.md) | Parse `~/.netrc` FTP login credentials |
| [`plistlib`](plistlib-generate-and-parse-apple-plist-files/index.md) | Read/write Apple XML or binary `.plist` files |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Export/import spreadsheet rows | [`csv`](csv-csv-file-reading-and-writing/index.md) with `DictReader` / `DictWriter` |
| Legacy Windows-style INI config | [`configparser`](configparser-configuration-file-parser/index.md) |
| Modern `pyproject.toml` / tool config | [`tomllib`](tomllib-parse-toml-files/index.md) (parse); Tomli-W or TOML Kit to write |
| FTP client auto-login from `~/.netrc` | [`netrc`](netrc-netrc-file-processing/index.md) |
| macOS/iOS app preference files | [`plistlib`](plistlib-generate-and-parse-apple-plist-files/index.md) |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Open text CSV/INI with **`encoding=`** and **`newline=''`** for CSV | Avoid platform newline translation and mojibake |
| Open TOML/plist with **`'rb'`** | `tomllib.load` and `plistlib.load` require binary file objects |
| Treat parsed config as **untrusted input** | Limit size; validate paths and types before acting |
| Prefer **typed getters** (`getint`, `getboolean`) in configparser | Raw strings need manual conversion |
| Use **`DictReader`** when rows have headers | Cleaner than positional column indexes |
| Pick **one config format** per project | Mixing INI, TOML, and JSON confuses operators |

```python
# Goal: round-trip a small CSV in memory
import csv
import io

buf = io.StringIO()
writer = csv.writer(buf)
writer.writerow(["name", "score"])
writer.writerow(["alice", "98"])
buf.seek(0)
rows = list(csv.DictReader(buf))
assert rows[0]["name"] == "alice" and rows[0]["score"] == "98"
```

```python
# Goal: parse minimal TOML from bytes
import tomllib

data = tomllib.loads('title = "demo"\ncount = 3')
assert data["title"] == "demo" and data["count"] == 3
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| CSV opened without `newline=''` | Extra `\r` on Windows rows | Always `open(..., newline='')` for csv module |
| Assuming CSV auto-converts types | All fields are strings unless `QUOTE_NONNUMERIC` | Cast with `int()` / `float()` explicitly |
| `bool("False")` on config values | Always `True` for non-empty strings | Use `ConfigParser.getboolean()` |
| Parsing huge TOML from untrusted sources | CPU/memory exhaustion | Cap input size before `loads` / `load` |
| plist dict keys not strings | `TypeError` on dump | Normalize keys or set `skipkeys=True` |
| Relying on `tomllib` to write TOML | Module is read-only (3.11+) | Use Tomli-W or TOML Kit for output |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [csv — CSV File Reading and Writing](csv-csv-file-reading-and-writing/index.md) | Dialects, `reader`/`writer`, `DictReader`/`DictWriter` |
| [configparser — Configuration file parser](configparser-configuration-file-parser/index.md) | INI sections, defaults, typed getters, interpolation |
| [tomllib — Parse TOML files](tomllib-parse-toml-files/index.md) | TOML 1.0.0 decode, type mapping, `parse_float` hook |
| [netrc — netrc file processing](netrc-netrc-file-processing/index.md) | Host credentials, macros, POSIX permission checks |
| [plistlib — Generate and parse Apple .plist files](plistlib-generate-and-parse-apple-plist-files/index.md) | XML/binary plists, `UID`, datetime handling |
