# [html — HyperText Markup Language support](https://docs.python.org/3/library/html.html)

The [`html`](https://docs.python.org/3/library/html.html) module provides **HTML escaping and unescaping** for safely embedding plain text in HTML documents and for decoding entity references. It does not parse full documents—that role belongs to [`html.parser`](../htmlparser-simple-html-and-xhtml-parser/index.md). Canonical reference: [docs.python.org](https://docs.python.org/3/library/html.html).

---

## Core functions — [Module contents](https://docs.python.org/3/library/html.html#module-contents)

| Function | Role |
|----------|------|
| `html.escape(s, quote=True)` | Replace `&`, `<`, `>`, and optionally `"` with entities |
| `html.unescape(s)` | Decode `&name;` and `&#…;` references to Unicode text |

Both functions accept **`str`** only (not `bytes`).

---

## When to use `escape` vs `unescape`

| Direction | Use case |
|-----------|----------|
| `escape` | Inserting user-supplied text into HTML templates |
| `unescape` | Converting stored HTML entities back to characters for display or further processing |

For XML attribute values in SAX/DOM pipelines, see [`xml.sax.saxutils`](../xmlsaxsaxutils-sax-utilities/index.md).

---

## Example — round-trip safety

```python
# Goal: escape user text before HTML insertion, then decode entities
import html

raw = 'Tom & Jerry say "hi"'
escaped = html.escape(raw, quote=True)
assert "&amp;" in escaped and "&quot;" in escaped

restored = html.unescape(escaped)
assert restored == raw
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Escape **at output**, not at storage | Keeps canonical data in plain text |
| Pass `quote=True` inside double-quoted attributes | Prevents attribute-breakout attacks |
| Do not rely on `unescape` for security | Decoding entities does not remove script tags |
