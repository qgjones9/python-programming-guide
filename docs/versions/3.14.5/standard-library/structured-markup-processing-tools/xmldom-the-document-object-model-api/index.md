# [xml.dom — The Document Object Model API](https://docs.python.org/3/library/xml.dom.html)

[`xml.dom`](https://docs.python.org/3/library/xml.dom.html) defines **W3C DOM** interfaces—node types, traversal helpers, and exception classes—implemented concretely by [`xml.dom.minidom`](../xmldomminidom-minimal-dom-implementation/index.md). Use DOM when you need standard node APIs (`Node`, `Document`, `Element`) rather than ElementTree’s lighter model. Reference: [docs.python.org](https://docs.python.org/3/library/xml.dom.html).

---

## Key node types — [Objects in the DOM](https://docs.python.org/3/library/xml.dom.html#objects-in-the-dom)

| Constant / class | Role |
|------------------|------|
| `xml.dom.Node.ELEMENT_NODE` | Element nodes |
| `xml.dom.Node.TEXT_NODE` | Text content |
| `xml.dom.Document` | Root document; `createElement`, `createTextNode` |
| `xml.dom.Element` | Tagged element with attributes and children |
| `xml.dom.DOMException` | Hierarchy and operation errors |

---

## DOM vs ElementTree

| Aspect | DOM | ElementTree |
|--------|-----|-------------|
| Standard | W3C DOM Level 2 subset | Python-specific tree |
| Memory | Higher overhead per node | Leaner element objects |
| Typical import | `xml.dom.minidom` | `xml.etree.ElementTree` |

---

## Example — inspect node types

```python
# Goal: create a minimal DOM document and verify node interfaces
import xml.dom.minidom as minidom
import xml.dom as dom

doc = minidom.getDOMImplementation().createDocument(None, "root", None)
root = doc.documentElement
child = doc.createElement("item")
child.setAttribute("id", "1")
text = doc.createTextNode("data")
child.appendChild(text)
root.appendChild(child)

assert root.nodeType == dom.Node.ELEMENT_NODE
assert text.nodeType == dom.Node.TEXT_NODE
assert child.getAttribute("id") == "1"
assert root.toxml() == '<root><item id="1">data</item></root>'
```

---

## See also

- [xml.dom.minidom — Minimal DOM implementation](../xmldomminidom-minimal-dom-implementation/index.md)
- [xml.dom.pulldom — partial tree builder](../xmldompulldom-support-for-building-partial-dom-trees/index.md)
