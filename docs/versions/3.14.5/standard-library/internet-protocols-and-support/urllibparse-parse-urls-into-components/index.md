# [urllib.parse — Parse URLs into components](https://docs.python.org/3/library/urllib.parse.html)

[`urllib.parse`](https://docs.python.org/3/library/urllib.parse.html) **splits and assembles URLs**: scheme, netloc, path, query, fragment, plus helpers for query encoding, path joining, and relative resolution. Essential for any HTTP client or redirect logic. Reference: [urllib.parse](https://docs.python.org/3/library/urllib.parse.html).

---

## Core functions

| Function | Role |
|----------|------|
| `urlparse(url)` / `urlunparse(parts)` | Six-component parse/build |
| `urlsplit(url)` / `urlunsplit(parts)` | Five-component variant (no params) |
| `urljoin(base, ref)` | Resolve relative URL against base |
| `parse_qs(qs)` / `parse_qsl(qs)` | Decode query string to dict or pairs |
| `urlencode(query, doseq=False)` | Encode mapping to `application/x-www-form-urlencoded` |
| `quote(string, safe='/')` / `unquote` | Percent-encode path segments |
| `quote_plus` / `unquote_plus` | Encode like form fields (`+` for space) |

---

## Example — build and decode a search URL

```python
# Goal: encode query parameters, parse them back, join relative links
import urllib.parse as up

base = "https://example.com/app/"
full = up.urljoin(base, "reports?id=1")
assert full == "https://example.com/app/reports?id=1"

qs = up.urlencode({"q": "café", "page": 2}, doseq=False)
params = up.parse_qs(qs)
assert params["q"] == ["café"]
assert params["page"] == ["2"]
```

---

## `ParseResult` fields

Named tuples expose `.scheme`, `.netloc`, `.path`, `.params`, `.query`, `.fragment` (urlparse) or omit `.params` (urlsplit). Use `.geturl()` to reconstruct the original form.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use `urlencode` for form bodies | Correct escaping of `&`, `=`, spaces |
| Prefer `urlsplit` for HTTP URLs | Rarely need obsolete `;params` segment |
| Never trust parsed host without IDNA/normalization | Homograph and unicode host issues |
