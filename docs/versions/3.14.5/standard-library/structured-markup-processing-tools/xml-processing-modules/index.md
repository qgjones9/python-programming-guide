# [XML Processing Modules](https://docs.python.org/3/library/xml.html)

The [`xml`](https://docs.python.org/3/library/xml.html) package groups Python’s **XML parsers and APIs**. [`xml.etree.ElementTree`](../xmletreeelementtree-the-elementtree-xml-api/index.md) is the recommended default; [`xml.dom`](../xmldom-the-document-object-model-api/index.md) and [`xml.sax`](../xmlsax-support-for-sax2-parsers/index.md) mirror W3C DOM and SAX models; [`xml.parsers.expat`](../xmlparsersexpat-fast-xml-parsing-using-expat/index.md) wraps the Expat C library. Overview: [docs.python.org](https://docs.python.org/3/library/xml.html).

---

## API comparison

| API | Memory model | Best for |
|-----|--------------|----------|
| ElementTree | In-memory tree (or incremental `iterparse`) | Config files, APIs, most application XML |
| DOM (minidom) | Full W3C node graph | Interop with DOM-centric libraries |
| pulldom | Lazy DOM slices | Large docs where only fragments are needed |
| SAX | Event stream, caller-driven | Very large files, constant memory |
| Expat | Low-level C parser | Custom parsers, error constants |

---

## Security note

The standard library XML modules are **not hardened against malicious XML** (billion laughs, external entities). For untrusted input, use [defusedxml](https://pypi.org/project/defusedxml/) or disable dangerous features explicitly.

---

## Example — same snippet, ElementTree vs SAX

```python
# Goal: read a title element with ElementTree and with SAX
import xml.etree.ElementTree as ET
from xml.sax import parseString
from xml.sax.handler import ContentHandler


xml_text = "<doc><title>Hello</title></doc>"

title_et = ET.fromstring(xml_text).findtext("title")
assert title_et == "Hello"


class TitleHandler(ContentHandler):
    def __init__(self):
        self.in_title = False
        self.parts = []

    def startElement(self, name, attrs):
        self.in_title = name == "title"

    def characters(self, content):
        if self.in_title:
            self.parts.append(content)

    def endElement(self, name):
        if name == "title":
            self.in_title = False


handler = TitleHandler()
parseString(xml_text, handler)
assert "".join(handler.parts) == "Hello"
```

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [xml.etree.ElementTree — The ElementTree XML API](xmletreeelementtree-the-elementtree-xml-api/index.md) | Element trees and XPath subset |
| [xml.dom — The Document Object Model API](xmldom-the-document-object-model-api/index.md) | DOM node types and exceptions |
| [xml.dom.minidom — Minimal DOM implementation](xmldomminidom-minimal-dom-implementation/index.md) | Lightweight DOM documents |
| [xml.dom.pulldom — Support for building partial DOM trees](xmldompulldom-support-for-building-partial-dom-trees/index.md) | Pull-based partial DOM |
| [xml.sax — Support for SAX2 parsers](xmlsax-support-for-sax2-parsers/index.md) | SAX parse drivers |
| [xml.sax.handler — Base classes for SAX handlers](xmlsaxhandler-base-classes-for-sax-handlers/index.md) | Handler base classes |
| [xml.sax.saxutils — SAX Utilities](xmlsaxsaxutils-sax-utilities/index.md) | Escaping and helper handlers |
| [xml.sax.xmlreader — Interface for XML parsers](xmlsaxxmlreader-interface-for-xml-parsers/index.md) | XMLReader interface |
| [xml.parsers.expat — Fast XML parsing using Expat](xmlparsersexpat-fast-xml-parsing-using-expat/index.md) | Expat bindings |
