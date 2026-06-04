# [Structured Markup Processing Tools](https://docs.python.org/3/library/markup.html)

Python’s standard library covers **HTML**, **XML**, and related structured markup through a family of parsers and tree APIs. [`html.parser`](htmlparser-simple-html-and-xhtml-parser/index.md) offers a lightweight event-style HTML scanner; the [`xml`](xml-processing-modules/index.md) package provides **ElementTree** (fast, Pythonic), **DOM** (W3C tree model), **SAX** (streaming callbacks), and **Expat** (C-backed low-level parsing). Full API reference remains on [docs.python.org](https://docs.python.org/3/library/markup.html); this hub orients you to each module and typical use cases.

---

## Choosing a parser or API

| Task | Start here |
|------|------------|
| Escape/unescape text for HTML output | [`html`](html-hypertext-markup-language-support/index.md) |
| Scan HTML tags and attributes without building a tree | [`html.parser`](htmlparser-simple-html-and-xhtml-parser/index.md) |
| Look up named HTML entities (`&amp;`, …) | [`html.entities`](htmlentities-definitions-of-html-general-entities/index.md) |
| Read/write config or data XML (most apps) | [`xml.etree.ElementTree`](xmletreeelementtree-the-elementtree-xml-api/index.md) |
| Full DOM traversal, legacy XML tools | [`xml.dom.minidom`](xmldomminidom-minimal-dom-implementation/index.md) |
| Build DOM subtrees lazily (large documents) | [`xml.dom.pulldom`](xmldompulldom-support-for-building-partial-dom-trees/index.md) |
| Stream huge XML with constant memory | [`xml.sax`](xmlsax-support-for-sax2-parsers/index.md) |
| Lowest-level Expat bindings | [`xml.parsers.expat`](xmlparsersexpat-fast-xml-parsing-using-expat/index.md) |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Prefer **ElementTree** for new code | Simple API, good performance, included in the stdlib |
| Never parse **untrusted HTML/XML** with vulnerable legacy parsers | Use defusedxml or dedicated sanitizers for external input |
| Pick **SAX or iterparse** for multi-gigabyte XML | DOM loads entire documents into memory |
| Use **`html.escape`** when inserting user text into HTML | Prevents XSS in generated markup |
| Declare **namespaces** explicitly in ElementTree searches | Tag names include `{uri}local` when namespaces are used |

```python
# Goal: compare lightweight HTML escape vs ElementTree for XML data
import html
import xml.etree.ElementTree as ET

user = "<script>alert(1)</script>"
safe_html = html.escape(user)
assert "&lt;script&gt;" in safe_html

root = ET.fromstring("<item id='1'>ok</item>")
assert root.tag == "item" and root.get("id") == "1"
```

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [html — HyperText Markup Language support](html-hypertext-markup-language-support/index.md) | Escape, unescape, and HTML-safe text helpers |
| [html.parser — Simple HTML and XHTML parser](htmlparser-simple-html-and-xhtml-parser/index.md) | Event-driven HTML tag scanner |
| [html.entities — Definitions of HTML general entities](htmlentities-definitions-of-html-general-entities/index.md) | Entity name/codepoint tables |
| [XML Processing Modules](xml-processing-modules/index.md) | Overview of the `xml` package |
| [xml.etree.ElementTree — The ElementTree XML API](xmletreeelementtree-the-elementtree-xml-api/index.md) | Element trees, XPath subset, serialization |
| [xml.dom — The Document Object Model API](xmldom-the-document-object-model-api/index.md) | W3C DOM types and exceptions |
| [xml.dom.minidom — Minimal DOM implementation](xmldomminidom-minimal-dom-implementation/index.md) | Lightweight DOM trees |
| [xml.dom.pulldom — Support for building partial DOM trees](xmldompulldom-support-for-building-partial-dom-trees/index.md) | Pull parser over DOM fragments |
| [xml.sax — Support for SAX2 parsers](xmlsax-support-for-sax2-parsers/index.md) | Streaming parse drivers |
| [xml.sax.handler — Base classes for SAX handlers](xmlsaxhandler-base-classes-for-sax-handlers/index.md) | ContentHandler, ErrorHandler, … |
| [xml.sax.saxutils — SAX Utilities](xmlsaxsaxutils-sax-utilities/index.md) | Escaping helpers and default handlers |
| [xml.sax.xmlreader — Interface for XML parsers](xmlsaxxmlreader-interface-for-xml-parsers/index.md) | XMLReader parser interface |
| [xml.parsers.expat — Fast XML parsing using Expat](xmlparsersexpat-fast-xml-parsing-using-expat/index.md) | Expat error constants and parser model |
