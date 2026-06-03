# [unicodedata — Unicode Database](https://docs.python.org/3/library/unicodedata.html)

[`unicodedata`](https://docs.python.org/3/library/unicodedata.html) exposes the **Unicode Character Database (UCD)**—names, categories, numeric values, bidirectional classes, and normalization—for every Unicode scalar value. The bundled data tracks a specific UCD release (`unicodedata.unidata_version`). Full function list remains on [docs.python.org](https://docs.python.org/3/library/unicodedata.html); see also the [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html).

---

## Lookup functions

| Function | Returns | On missing data |
|----------|---------|-----------------|
| `lookup(name)` | Single-character `str` for UCD name | `KeyError` |
| `name(chr, default=None)` | Character name | `ValueError` or `default` |
| `decimal(chr, default=None)` | Decimal digit value (int) | `ValueError` or `default` |
| `digit(chr, default=None)` | Digit value including superscripts | `ValueError` or `default` |
| `numeric(chr, default=None)` | Numeric value as `float` | `ValueError` or `default` |
| `category(chr)` | Two-letter general category (`Lu`, `Nd`, …) | always defined |
| `bidirectional(chr)` | Bidirectional class (`L`, `R`, `NSM`, …) | `''` if undefined |
| `combining(chr)` | Canonical combining class (int) | `0` if undefined |
| `east_asian_width(chr)` | `W`, `F`, `Na`, `H`, `A`, `N` | always defined |
| `mirrored(chr)` | `1` if mirrored in bidi text else `0` | always defined |
| `decomposition(chr)` | Decomposition mapping string | `''` if none |

```python
# Goal: name lookup matches \N{...} escapes
import unicodedata

assert unicodedata.lookup("LEFT CURLY BRACKET") == "{"
assert unicodedata.lookup("MIDDLE DOT") == "\N{MIDDLE DOT}"
assert unicodedata.name("½") == "VULGAR FRACTION ONE HALF"
assert unicodedata.numeric("½") == 0.5
assert unicodedata.category("A") == "Lu"
```

---

## Normalization — [normalize](https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize)

Unicode strings can encode the same text with different code-point sequences (composed vs decomposed accents, compatibility glyphs). Normalization forms:

| Form | Steps | Typical use |
|------|-------|-------------|
| **NFD** | Canonical decomposition | Compare base + combining marks |
| **NFC** | Decompose then re-compose | Web/storage canonical form |
| **NFKD** | Compatibility decomposition | Fold compatibility characters |
| **NFKC** | Compatibility decompose + compose | Identifier / password folding |

```python
# Goal: NFC vs NFD equality after normalization
import unicodedata

composed = "\u00c7"       # LATIN CAPITAL LETTER C WITH CEDILLA
decomposed = "C\u0327"    # C + COMBINING CEDILLA
assert composed != decomposed
assert unicodedata.normalize("NFC", decomposed) == composed
assert unicodedata.normalize("NFD", composed) == decomposed
```

[`is_normalized(form, unistr)`](https://docs.python.org/3/library/unicodedata.html#unicodedata.is_normalized) (3.8+) checks whether a string is already in the requested form—avoid redundant work in hot paths.

```python
# Goal: skip normalization when already NFC
import unicodedata

text = "Straße"
assert unicodedata.is_normalized("NFC", text)
result = text if unicodedata.is_normalized("NFC", text) else unicodedata.normalize("NFC", text)
assert result == text
```

---

## Module constants

| Name | Role |
|------|------|
| `unidata_version` | UCD version string bundled with this interpreter |
| `ucd_3_2_0` | Alternate module object frozen at Unicode 3.2.0 (legacy IDNA) |

---

## Best practices and pitfalls

| Practice | Why |
|----------|-----|
| Normalize before **casefold** / equality | `casefold()` is not normalization—combine with NFKC for identifiers |
| Prefer **NFC** for storage | Smaller and conventional for most Latin/Cyrillic text |
| Use **NFKC** for security-sensitive identifiers | Strips compatibility variants (e.g. full-width digits) |
| Check **`is_normalized`** before writing | Saves CPU when pipelines re-process unchanged text |
| Do not assume normalized strings **look** identical | Combining marks may still render similarly but compare equal |

**Pitfall:** two visually identical strings can compare unequal if one uses combining characters and the other precomposed glyphs—always normalize at system boundaries (input, persistence, crypto).

```python
# Goal: identifier folding pipeline
import unicodedata

def fold_identifier(text):
    return unicodedata.normalize("NFKC", text).casefold()

assert fold_identifier("ＡＢＣ") == "abc"
```
