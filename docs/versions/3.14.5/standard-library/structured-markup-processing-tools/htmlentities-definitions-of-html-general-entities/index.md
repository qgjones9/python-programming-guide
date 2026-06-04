# [html.entities — Definitions of HTML general entities](https://docs.python.org/3/library/html.entities.html)

[`html.entities`](https://docs.python.org/3/library/html.entities.html) exposes **lookup tables** mapping HTML entity names and code points used by [`html.unescape`](../html-hypertext-markup-language-support/index.md) and related tools. It is reference data, not a parser. Canonical tables: [Module contents](https://docs.python.org/3/library/html.entities.html#module-contents).

---

## Main mappings

| Name | Type | Purpose |
|------|------|---------|
| `html.entities.html5` | `dict[str, str]` | HTML5 named character references → single-character strings |
| `html.entities.name2codepoint` | `dict[str, int]` | Legacy entity name → Unicode code point |
| `html.entities.codepoint2name` | `dict[int, str]` | Code point → canonical entity name (where defined) |
| `html.entities.entitydefs` | `dict[str, str]` | Small legacy set (`lt`, `gt`, `amp`, `quot`, `apos`) |

---

## Example — resolve entity names to characters

```python
# Goal: look up HTML5 entity definitions programmatically
import html.entities as entities

assert entities.html5["amp"] == "&"
assert entities.html5["copy"] == "\u00a9"
assert entities.name2codepoint["ntilde"] == 0x00F1
assert entities.codepoint2name[0x00A9] == "copy"
```

---

## When you need this module

| Scenario | Approach |
|----------|----------|
| Custom unescape beyond `html.unescape` | Consult `html5` or `name2codepoint` |
| Generate entity names from code points | Reverse lookup via `codepoint2name` (may raise `KeyError`) |
| Normal HTML output escaping | Prefer [`html.escape`](../html-hypertext-markup-language-support/index.md) instead |
