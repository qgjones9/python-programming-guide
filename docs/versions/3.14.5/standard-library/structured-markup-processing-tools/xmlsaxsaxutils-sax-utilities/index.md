# [xml.sax.saxutils — SAX Utilities](https://docs.python.org/3/library/xml.sax.utils.html)

[`xml.sax.saxutils`](https://docs.python.org/3/library/xml.sax.utils.html) collects **helper functions and handler classes** for SAX pipelines—escaping text for XML output, quoting attributes, and default handler implementations. Reference: [saxutils module](https://docs.python.org/3/library/xml.sax.utils.html).

---

## Escaping helpers

| Function | Role |
|----------|------|
| `escape(data, entities={})` | Escape `&`, `<`, `>` and optional extra entities |
| `quoteattr(data, entities={})` | Produce a double-quoted attribute value safe for XML |
| `unescape(data, entities={})` | Reverse minimal entity escaping |

These operate on **`str`**, not bytes.

---

## Handler utilities

| Class | Role |
|-------|------|
| `XMLGenerator` | `ContentHandler` that writes XML to a stream |
| `XMLFilterBase` | Base for SAX filter chains |

---

## Example — escape and quote attribute values

```python
# Goal: prepare user text for manual XML serialization
from xml.sax.saxutils import escape, quoteattr

raw = 'Tom & "Jerry"'
assert escape(raw) == 'Tom &amp; "Jerry"'
assert quoteattr(raw) == '\'Tom &amp; "Jerry"\''
```

---

## Related modules

- Emit structured XML more safely with [`xml.etree.ElementTree`](../xmletreeelementtree-the-elementtree-xml-api/index.md) instead of manual string building when possible.
- HTML output escaping uses [`html.escape`](../html-hypertext-markup-language-support/index.md), not `saxutils.escape`.
