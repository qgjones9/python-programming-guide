# [Non-ASCII characters in names](https://docs.python.org/3/reference/lexical_analysis.html#non-ascii-characters-in-names)


Names in Python can include non-ASCII (Unicode) characters, but there are extra normalization and validation rules beyond those for standard ASCII names. For example:

- Valid: `ř_1`, `蛇`, `साँप`
- **Invalid:** `r〰2`, `€`, `🐍`

This section details exactly which non-ASCII characters are permitted as names.

---

## Unicode Normalization

All names are normalized in [NFKC form](https://Unicode.org/reports/tr15/). This means Python converts certain typographic variants of characters to their standardized "basic" forms.  
For example:

```python
ﬁⁿₐˡᵢᶻₐᵗᵢᵒₙ = 3
print(finalization)  # 3 (ﬁⁿₐˡᵢᶻₐᵗᵢᵒₙ normalizes to 'finalization')
```

> **Note:**  
> - Normalization is performed only at the lexical analysis (parsing) stage.
> - Run-time string operations (e.g., accessing variables by string name) do **not** normalize:  
>   - `globals()["finalization"]` works  
>   - `globals()["ﬁⁿₐˡᵢᶻₐᵗᵢᵒₙ"]` does **not**

See [Unicode Normalization Forms](https://unicode.org/reports/tr15/) for the details.

---

## Valid Characters in Non-ASCII Names

Just as ASCII-only identifiers must start with a letter or underscore (not a digit),  
**non-ASCII names must follow these rules:**

- **First character:** Must be from the "letter-like" set (**xid_start**).
- **Subsequent characters:** May be from the "letter-like or digit-like" set (**xid_continue**).

These are based on the [Unicode® Standard Annex #31: Identifier and Pattern Syntax (UAX-31)](https://unicode.org/reports/tr31/).

> **Note:** Python’s implementation extends these sets (adds the underscore `_` to `xid_start`) and does **not** necessarily conform exactly to the UAX-31 standard.

- [UAX-31 reference](https://unicode.org/reports/tr31/)
- [Unicode Character Database](https://www.unicode.org/Public/UCD/latest/ucd/DerivedCoreProperties.txt)
- [[Python docs – Non-ASCII in names]](https://docs.python.org/3/reference/lexical_analysis.html#non-ascii-characters-in-names)

---

### Formal Definitions

#### xid_start and xid_continue

- `id_start` is defined as the union of:
  - Unicode categories:
    - `<Lu>`: Uppercase letters (A–Z, etc.)
    - `<Ll>`: Lowercase letters (a–z, etc.)
    - `<Lt>`: Titlecase letters
    - `<Lm>`: Modifier letters
    - `<Lo>`: Other letters
    - `<Nl>`: Letter numbers
  - `{ "_" }` (the underscore)
  - `<Other_ID_Start>`: Additional backwards-compatibility characters (see [PropList.txt](https://www.unicode.org/Public/UCD/latest/ucd/PropList.txt))

- `xid_start` is the subset of `id_start` whose [NFKC-normalized](https://unicode.org/reports/tr15/) form is itself a valid identifier start**.

- `id_continue` is defined as the union of:
  - **all of `id_start`**
  - `<Nd>`: Decimal numbers (0–9)
  - `<Pc>`: Connector punctuations
  - `<Mn>`: Nonspacing marks
  - `<Mc>`: Spacing combining marks
  - `<Other_ID_Continue>`: Additional backwards-compatibility (see [PropList.txt](https://www.unicode.org/Public/UCD/latest/ucd/PropList.txt))

- `xid_continue` is defined as the NFKC closure of `id_continue`.

> Unicode categories in use are those found in the version of the Unicode Character Database included with Python ([unicodedata module](https://docs.python.org/3/library/unicodedata.html)).

---

## Further Reading

- [PEP 3131 – Supporting Non-ASCII Identifiers](https://peps.python.org/pep-3131/)
- [PEP 672 – Unicode-related Security Considerations for Python](https://peps.python.org/pep-0672/)
- [Unicode® Standard Annex #31: Identifier and Pattern Syntax](https://unicode.org/reports/tr31/)
- [Python: Lexical Analysis—Non-ASCII characters in names](https://docs.python.org/3/reference/lexical_analysis.html#non-ascii-characters-in-names)
