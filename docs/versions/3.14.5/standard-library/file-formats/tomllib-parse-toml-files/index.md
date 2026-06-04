# [tomllib — Parse TOML files](https://docs.python.org/3/library/tomllib.html)

The [`tomllib`](https://docs.python.org/3/library/tomllib.html) module (added in **3.11**) parses **TOML 1.0.0** into Python objects. It is **read-only**—use [Tomli-W](https://pypi.org/project/tomli-w/) or [TOML Kit](https://pypi.org/project/tomlkit/) to write or preserve formatting. Files must be opened in **binary mode** (`'rb'`). Full type mapping and `TOMLDecodeError` attributes remain on [docs.python.org](https://docs.python.org/3/library/tomllib.html).

---

## API — [Module functions](https://docs.python.org/3/library/tomllib.html)

| Function | Input | Returns |
|----------|-------|---------|
| `load(fp, *, parse_float=float)` | Binary readable file object | `dict` (root table) |
| `loads(s, *, parse_float=float)` | `str` TOML document | `dict` |

| Exception | When |
|-----------|------|
| `TOMLDecodeError` | Invalid syntax; exposes `msg`, `doc`, `pos`, `lineno`, `colno` (3.14+) |

The optional **`parse_float`** hook receives each float token string—useful for `decimal.Decimal` instead of binary floats.

---

## Type conversion — [Conversion Table](https://docs.python.org/3/library/tomllib.html#conversion-table)

| TOML type | Python type |
|-----------|-------------|
| table | `dict` |
| array | `list` |
| string | `str` |
| integer | `int` |
| float | `float` (or `parse_float` result) |
| boolean | `bool` |
| offset date-time | `datetime.datetime` (aware, with `tzinfo`) |
| local date-time | `datetime.datetime` (`tzinfo=None`) |
| local date | `datetime.date` |
| local time | `datetime.time` |
| array of tables | `list` of `dict` |

```python
# Goal: parse inline TOML with tables and arrays
import tomllib

doc = """
title = "Widget"
tags = ["a", "b"]

[owner]
name = "Ada"
"""
data = tomllib.loads(doc)
assert data["title"] == "Widget"
assert data["tags"] == ["a", "b"]
assert data["owner"]["name"] == "Ada"
```

```python
# Goal: load TOML from an in-memory binary file
import io
import tomllib

raw = b'version = "1.0.0"\nrequires-python = ">=3.11"\n'
with io.BytesIO(raw) as fp:
    meta = tomllib.load(fp)
assert meta["version"] == "1.0.0"
assert meta["requires-python"] == ">=3.11"
```

```python
# Goal: custom parse_float with Decimal
import tomllib
from decimal import Decimal

def as_decimal(num_str):
    return Decimal(num_str)

data = tomllib.loads('price = 19.99', parse_float=as_decimal)
assert data["price"] == Decimal("19.99")
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Open with **`'rb'`** | API requires binary file objects |
| **Cap input size** on untrusted TOML | Parser can consume large CPU/memory |
| Use **`parse_float=Decimal`** for money | Binary float rounding surprises |
| Pair with **Tomli-W** only for simple writes | TOML Kit preserves comments and layout |
| Validate required keys after parse | Missing keys fail at runtime otherwise |
| Prefer **`pyproject.toml`** standard keys | Ecosystem tools expect `[project]`, `[tool.*]` |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Opening with text mode `'r'` | Type/encoding errors | Use `'rb'` and explicit UTF-8 bytes |
| Expecting write support | No `dump` in stdlib | Add Tomli-W or TOML Kit |
| Huge documents from network | DoS via parse cost | Enforce max bytes before `loads` |
| `parse_float` returning dict/list | `ValueError` | Return only scalar numeric types |
| Inline vs standard tables | Same Python type (`dict`) | Structure affects merge semantics in TOML |
| Date/time timezone assumptions | Mix of aware and naive objects | Check conversion table per field type |
