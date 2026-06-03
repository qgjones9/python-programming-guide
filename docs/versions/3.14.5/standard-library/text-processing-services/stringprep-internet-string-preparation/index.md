# [stringprep — Internet String Preparation](https://docs.python.org/3/library/stringprep.html)

[`stringprep`](https://docs.python.org/3/library/stringprep.html) exposes the **RFC 3454** table data used to prepare Unicode strings before they appear on the wire in Internet protocols (host names, user parts, profile-specific identifiers). The module does **not** implement a full profile—applications such as **nameprep** (internationalized domain names) combine these predicates and maps with normalization and bidirectional rules. Full table listing remains on [docs.python.org](https://docs.python.org/3/library/stringprep.html).

---

## How tables are exposed

RFC tables are implemented as **functions**, not dict literals—the Unicode database backs membership and mapping tests efficiently.

| Table kind | Python API shape | Example |
|------------|------------------|---------|
| Set (membership) | `in_table_* (code) -> bool` | `in_table_c11(' ')` |
| Mapping | `map_table_* (code) -> str` | `map_table_b2(code)` |

**Code** arguments are strings of length 1 (a single Unicode character).

---

## Table groups (RFC 3454)

| Group | Functions | Purpose |
|-------|-----------|---------|
| **A.1** | `in_table_a1` | Unassigned code points (Unicode 3.2 baseline) |
| **B.1** | `in_table_b1` | Map to nothing (delete) |
| **B.2** | `map_table_b2` | Case fold with NFKC |
| **B.3** | `map_table_b3` | Case fold without normalization |
| **C.1** | `in_table_c11`, `in_table_c12`, `in_table_c11_c12` | Space characters |
| **C.2** | `in_table_c21`, `in_table_c22`, `in_table_c21_c22` | Control characters |
| **C.3–C.9** | `in_table_c3` … `in_table_c9` | Prohibited / deprecated / tagging |
| **D.1–D.2** | `in_table_d1`, `in_table_d2` | Bidirectional character sets |

```python
# Goal: detect prohibited space and control characters
import stringprep

assert stringprep.in_table_c11(" ") is True
assert stringprep.in_table_c11("a") is False
assert stringprep.in_table_c21("\x07") is True  # BEL control
assert stringprep.in_table_c11_c12("\u00a0") is True  # NBSP
```

---

## Case-folding maps

`map_table_b2` and `map_table_b3` return a replacement string for characters that participate in case folding; otherwise they return the original character.

```python
# Goal: apply RFC B.2 case folding to a single character
import stringprep

folded = stringprep.map_table_b2("K")
assert folded == "k"
assert stringprep.map_table_b2("5") == "5"
```

A minimal (non-compliant) preparation sketch chains mapping + prohibition checks—real profiles add normalization, bidirectional constraints, and unassigned checks:

```python
# Goal: reject controls and map case (illustrative only)
import stringprep

def sketch_prepare(text):
    out = []
    for char in text:
        if stringprep.in_table_c21_c22(char):
            raise ValueError("control character")
        if stringprep.in_table_b1(char):
            continue
        out.append(stringprep.map_table_b2(char))
    return "".join(out)

assert sketch_prepare("Example") == "example"
try:
    sketch_prepare("\x00")
except ValueError as exc:
    assert "control" in str(exc)
else:
    raise AssertionError("expected ValueError")
```

---

## Best practices and pitfalls

| Practice | Why |
|----------|-----|
| Follow a **named profile** (e.g. nameprep, SASLprep) | RFC 3454 alone is incomplete |
| Combine with [`unicodedata.normalize`](../unicodedata-unicode-database/index.md) | B.2 assumes NFKC context in real profiles |
| Operate on **code points**, not UTF-16 code units | Python `str` iterates Unicode scalars |
| Use **`idna`** for domain names | Higher-level IDNA codec wraps stringprep rules |
| Do not hand-roll full IDNA | Edge cases span tables, normalization, and bidi |

**Pitfall:** `in_table_a1` reflects the Unicode **3.2** unassigned set baked into RFC 3454—modern unassigned code points need profile-specific updates beyond this module.

For domain names prefer the standard library [`encodings.idna`](https://docs.python.org/3/library/codecs.html#encodings.idna) codec rather than calling stringprep tables directly.
