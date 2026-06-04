# [xml.sax — Support for SAX2 parsers](https://docs.python.org/3/library/xml.sax.html)

[`xml.sax`](https://docs.python.org/3/library/xml.sax.html) provides **SAX2 parser drivers** and helpers for **event-driven XML parsing**. Handlers ([`xml.sax.handler`](../xmlsaxhandler-base-classes-for-sax-handlers/index.md)) receive `startElement`, `characters`, and `endElement` callbacks without building a full in-memory tree. Reference: [xml.sax module](https://docs.python.org/3/library/xml.sax.html).

---

## Parsing entry points

| Function | Input |
|----------|-------|
| `xml.sax.parse(filename_or_stream, handler)` | File path or readable object |
| `xml.sax.parseString(string, handler)` | `str` or `bytes` XML |
| `xml.sax.make_parser()` | Factory returning an `XMLReader` |

Register features on the reader (namespaces, validation) via [`xml.sax.xmlreader`](../xmlsaxxmlreader-interface-for-xml-parsers/index.md).

---

## Example — count elements with a handler

```python
# Goal: SAX parse a string and count element names
from xml.sax import parseString
from xml.sax.handler import ContentHandler


class Counter(ContentHandler):
    def __init__(self):
        self.counts = {}

    def startElement(self, name, attrs):
        self.counts[name] = self.counts.get(name, 0) + 1


handler = Counter()
parseString("<doc><a/><a/><b/></doc>", handler)
assert handler.counts == {"doc": 1, "a": 2, "b": 1}
```

---

## Error handling

| Exception | Source |
|-----------|--------|
| `xml.sax.SAXParseException` | Well-formedness errors during parse |
| Handler’s `error`, `fatalError`, `warning` | Override on `ErrorHandler` |

Use SAX when document size makes DOM/ElementTree memory use unacceptable.
