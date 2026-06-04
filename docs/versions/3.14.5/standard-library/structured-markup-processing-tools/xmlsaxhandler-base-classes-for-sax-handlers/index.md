# [xml.sax.handler — Base classes for SAX handlers](https://docs.python.org/3/library/xml.sax.handler.html)

[`xml.sax.handler`](https://docs.python.org/3/library/xml.sax.handler.html) defines **base handler classes** SAX parsers invoke during streaming parse. Subclass `ContentHandler` for element events; mix in `ErrorHandler` or use [`xml.sax.saxutils`](../xmlsaxsaxutils-sax-utilities/index.md) defaults. Reference: [handler module](https://docs.python.org/3/library/xml.sax.handler.html).

---

## Primary handler classes

| Class | Callbacks (selected) |
|-------|----------------------|
| `ContentHandler` | `startDocument`, `startElement`, `characters`, `endElement`, `endDocument` |
| `ErrorHandler` | `error`, `fatalError`, `warning` |
| `DTDHandler` | Notation and unparsed entity declarations |
| `EntityResolver` | Resolve external entities (`resolveEntity`) |

Feature flags such as `feature_namespaces` live on [`XMLReader`](../xmlsaxxmlreader-interface-for-xml-parsers/index.md) implementations.

---

## Example — accumulate character data per element

```python
# Goal: subclass ContentHandler to capture text inside <msg> elements
from xml.sax.handler import ContentHandler


class MessageCollector(ContentHandler):
    def __init__(self):
        self._depth = 0
        self.messages = []

    def startElement(self, name, attrs):
        if name == "msg":
            self._depth += 1
            self._buf = []

    def characters(self, content):
        if self._depth:
            self._buf.append(content)

    def endElement(self, name):
        if name == "msg" and self._depth:
            self.messages.append("".join(self._buf))
            self._depth -= 1


from xml.sax import parseString

handler = MessageCollector()
parseString("<root><msg>a</msg><msg>b</msg></root>", handler)
assert handler.messages == ["a", "b"]
```

---

## Default no-op implementations

All methods on base handler classes are **empty stubs**—override only what you need. For quick debugging, `xml.sax.saxutils.XMLGenerator` writes SAX events back to XML text.
