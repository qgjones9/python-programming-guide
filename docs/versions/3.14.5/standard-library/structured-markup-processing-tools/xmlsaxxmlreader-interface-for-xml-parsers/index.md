# [xml.sax.xmlreader — Interface for XML parsers](https://docs.python.org/3/library/xml.sax.reader.html)

[`xml.sax.xmlreader`](https://docs.python.org/3/library/xml.sax.reader.html) specifies the **`XMLReader` interface** that SAX parser implementations expose: set content/error handlers, toggle features and properties, and parse from a system identifier or [`InputSource`](https://docs.python.org/3/library/xml.sax.reader.html#xml.sax.xmlreader.InputSource). Application code rarely subclasses these types; use [`xml.sax.make_parser()`](../xmlsax-support-for-sax2-parsers/index.md) instead.

---

## XMLReader responsibilities

| Method / attribute | Role |
|--------------------|------|
| `setContentHandler(handler)` | Receive document events |
| `setErrorHandler(handler)` | Receive parse warnings/errors |
| `setFeature(name, value)` | Enable namespaces, validation, etc. |
| `parse(source)` | Drive parsing from `InputSource` or system id |
| `getProperty(name)` | Parser-specific properties (lexical handler, …) |

Standard feature URI: `http://xml.org/sax/features/namespaces`.

---

## Example — configure a reader before parse

```python
# Goal: obtain XMLReader, toggle namespace feature, attach a ContentHandler
from xml.sax import make_parser
from xml.sax.handler import ContentHandler, feature_namespaces


class NoopHandler(ContentHandler):
    pass


reader = make_parser()
reader.setFeature(feature_namespaces, True)
assert reader.getFeature(feature_namespaces) is True
reader.setContentHandler(NoopHandler())
assert reader.getContentHandler().__class__.__name__ == "NoopHandler"
```

---

## InputSource

Wrap bytes or character streams with encoding hints when not parsing from a file URL. `InputSource.setCharacterStream` accepts a text stream; `setByteStream` accepts binary data.
