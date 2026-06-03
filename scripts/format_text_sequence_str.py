#!/usr/bin/env python3
"""Format scraped stdtypes str section into teaching markdown."""
from __future__ import annotations

import re
from pathlib import Path

SRC = Path(
    "/home/qjones/.cursor/projects/home-qjones-workspace-python-programming-guide/uploads/index-L2-L1093-0.md"
)
DST = Path(
    "/home/qjones/workspace/python-programming-guide/docs/versions/3.14.5/standard-library/built-in-types/text-sequence-type-str/index.md"
)

METHOD_CATEGORIES = [
    (
        "Search, test, and count",
        "find where substrings occur, test boundaries, or count matches",
        ["find", "rfind", "index", "rindex", "count", "startswith", "endswith"],
    ),
    (
        "Split, join, and partition",
        "break text apart or concatenate iterables of strings",
        ["split", "rsplit", "splitlines", "partition", "rpartition", "join"],
    ),
    (
        "Strip, prefix, and suffix",
        "trim edges or remove/add fixed affixes",
        ["strip", "lstrip", "rstrip", "removeprefix", "removesuffix"],
    ),
    (
        "Case and title",
        "change letter case for display or comparisons",
        ["capitalize", "casefold", "lower", "upper", "swapcase", "title"],
    ),
    (
        "Padding and alignment",
        "pad or align text in a fixed-width field",
        ["center", "ljust", "rjust", "zfill", "expandtabs"],
    ),
    (
        "Transform and encode",
        "replace content, map characters, or encode to bytes",
        ["replace", "translate", "encode"],
    ),
    (
        "Formatting helpers",
        "build strings from templates or mappings",
        ["format", "format_map"],
    ),
    (
        "Classification (`is*` methods)",
        "test Unicode categories and identifier rules",
        [
            "isalnum",
            "isalpha",
            "isascii",
            "isdecimal",
            "isdigit",
            "isidentifier",
            "islower",
            "isnumeric",
            "isprintable",
            "isspace",
            "istitle",
            "isupper",
        ],
    ),
]

TAIL_SECTIONS = [
    (
        "Formatted String Literals (f-strings)",
        "formatted-string-literals-f-strings",
        "https://docs.python.org/3/library/stdtypes.html#formatted-string-literals-f-strings",
    ),
    (
        "Template String Literals (t-strings)",
        "template-string-literals-t-strings",
        "https://docs.python.org/3/library/stdtypes.html#template-string-literals-t-strings",
    ),
    (
        "printf-style String Formatting",
        "printf-style-string-formatting",
        "https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting",
    ),
]

PRINTF_FLAG_TABLE = """
| Flag | Meaning |
|------|---------|
| `#` | “Alternate form” for the conversion (see notes below). |
| `0` | Zero-pad numeric values. |
| `-` | Left-adjust the converted value (overrides `0` if both are given). |
| ` ` (space) | Leave a blank before a positive number from a signed conversion. |
| `+` | Always show a sign (`+` or `-`); overrides the space flag. |

A length modifier (`h`, `l`, or `L`) may appear but is **ignored** in Python (`%ld` behaves like `%d`).
"""

PRINTF_CONVERSION_TABLE = """
| Conversion | Meaning | Notes |
|------------|---------|-------|
| `d` | Signed integer decimal. | |
| `i` | Signed integer decimal. | |
| `o` | Signed octal. | (1) alternate: leading `0o`. |
| `u` | Obsolete; same as `d`. | (6) |
| `x` | Signed hex (lowercase). | (2) alternate: `0x`. |
| `X` | Signed hex (uppercase). | (2) alternate: `0X`. |
| `e` | Float, exponential (lowercase). | (3) |
| `E` | Float, exponential (uppercase). | (3) |
| `f` | Float, decimal format. | (3) |
| `F` | Float, decimal format. | (3) |
| `g` | Float; uses `%e` or `%f` style by magnitude. | (4) |
| `G` | Like `g` but uppercase exponent. | (4) |
| `c` | Single character (int or length-1 str). | |
| `r` | String via `repr()`. | (5) |
| `s` | String via `str()`. | (5) |
| `a` | String via `ascii()`. | (5) |
| `%` | Literal `%` in the result. | |

**Notes:** (1) octal alternate form; (2) hex alternate `0x`/`0X`; (3) precision defaults to 6 fractional digits; (4) `%g`/`%G` precision counts significant digits; (5) no NUL (`\\0`) termination for `%s`; (6) `%u` is obsolete. See [PEP 237](https://peps.python.org/pep-0237/) for integer display rules.
"""

FSTR_SECTION = """
> **Added in version 3.6.**

> **Changed in version 3.7:** `await` and `async for` may appear in f-string expressions.

> **Changed in version 3.8:** Debug specifier `=` added.

> **Changed in version 3.12:** Many expression restrictions removed (nested strings, comments, backslashes allowed).

An **f-string** (formatted string literal) is prefixed with **`f`** or **`F`**. Curly braces `{…}` embed expressions evaluated at runtime. Each field may include, in order:

1. The **expression**
2. An optional **debug specifier** (`=`)
3. An optional **conversion** (`!s`, `!r`, `!a`)
4. An optional **format specifier** after `:`

See [f-strings in Lexical Analysis](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) for full syntax.

### Debug specifier (`=`)

> **Added in version 3.8.**

With `=`, the output includes the **expression source**, `=`, and the **value**—ideal for quick debugging:

```python
number = 14.3
assert f'{number=}' == 'number=14.3'
assert f'{ number  -  4  = }' == ' number  -  4  = 10.3'  # whitespace preserved
```

### Conversion specifiers (`!s`, `!r`, `!a`)

By default, values are converted with **`str()`**. With a debug specifier but **no** format specifier, **`repr()`** is used instead.

| Specifier | Calls | Typical use |
|-----------|-------|-------------|
| `!s` | `str()` | User-facing text |
| `!r` | `repr()` | Unambiguous, developer-oriented |
| `!a` | `ascii()` | ASCII-only escapes |

```python
from fractions import Fraction
one_third = Fraction(1, 3)
assert f'{one_third}' == '1/3'
assert f'{one_third = }' == 'one_third = Fraction(1, 3)'
assert f'{one_third!s} is {one_third!r}' == '1/3 is Fraction(1, 3)'
string = "¡kočka 😸!"
assert f'{string = !a}' == "string = '\\xa1ko\\u010dka \\U0001f638!'"
```

### Format specifier (`:`)

After conversion, **`format()`** applies the part after `:`. Nested fields inside the format spec (e.g. `{amount:.{precision}f}`) are evaluated **eagerly**.

```python
from fractions import Fraction
one_third = Fraction(1, 3)
assert f'{one_third:.6f}' == '0.333333'
assert f'{one_third:_^+10}' == '___+1/3___'
assert f'{one_third!r:_^20}' == '___Fraction(1, 3)___'
assert f'{one_third = :~>10}~' == 'one_third = ~~~~~~~1/3~'
```

See [Format string syntax](https://docs.python.org/3/library/string.html#formatstrings) for the mini-language after `:`.
"""

TSTR_SECTION = """
A **t-string** (template string literal, **3.14+**) is prefixed with **`t`** or **`T`**. Syntax mirrors f-strings, but evaluation differs:

| Aspect | f-string | t-string |
|--------|----------|----------|
| Result type | `str` | `string.templatelib.Template` |
| Formatting | `format()` runs immediately | Specifiers become `Interpolation` objects for later processing |
| `=` debug | Uses `repr()` by default when no other conversion | Expression text appended to preceding literal; default conversion `r` unless overridden |

**Deferred formatting:** Code that consumes the `Template` decides how to interpret format specifiers and conversions—useful for safe templating where you must not evaluate arbitrary format logic at literal creation time.

**Nested format specs:** `{amount:.{precision}f}` evaluates `{precision}` first to build the format_spec (e.g. `'.2f'` when `precision` is `2`).

**Debug (`=`):** The expression text (including `=` and surrounding spaces) is appended to the literal portion; an `Interpolation` is still created, defaulting to repr conversion unless you supply an explicit conversion or format specifier.
"""

PRINTF_SECTION = """
!!! note
    These operations have historical quirks (e.g. displaying tuples and dicts). Prefer **f-strings**, **`str.format()`**, or **`string.Template`** for new code.

The **`%`** operator performs **printf-style interpolation**: `format % values` replaces conversion specifications in `format`, similar to C `sprintf`.

```python
assert '%s has %d quote types.' % ('Python', 2) == 'Python has 2 quote types.'
assert '%(language)s has %(number)03d quote types.' % {'language': 'Python', 'number': 2} == 'Python has 002 quote types.'
```

- **Single argument:** `values` may be a non-tuple object when the format expects one conversion.
- **Multiple arguments:** `values` must be a **tuple** with exactly the right length, or a **mapping** when using `%(name)s` keys (no `*` width/precision from mapping).

A conversion specifier has, in order: `%`, optional `(name)`, flags, width, precision, ignored length modifier, and **conversion type**.

The conversion flag characters are:

"""

SPLITLINES_BOUNDARIES = """
| Escape / code | Description |
|---------------|-------------|
| `\\n` | Line Feed |
| `\\r` | Carriage Return |
| `\\r\\n` | Carriage Return + Line Feed |
| `\\v`, `\\x0b` | Line Tabulation |
| `\\f`, `\\x0c` | Form Feed |
| `\\x1c` | File Separator |
| `\\x1d` | Group Separator |
| `\\x1e` | Record Separator |
| `\\x85` | Next Line (C1) |
| `\\u2028` | Line Separator |
| `\\u2029` | Paragraph Separator |

> **Changed in version 3.2:** `\\v` and `\\f` are recognized as line boundaries.
"""

PROSE_RE = re.compile(
    r"^(Return |Like |Similar |If |When |Since |Casefolding |The |See |For |Unlike |Here |"
    r"Keyword|Example:|Changed|Added|Note |See also|Strings |In this |A conversion|Mapping |"
    r"Minimum |Precision |Length |An f-string|An t-string|Rather |Format specifiers|"
    r"Whitespace |By default|Debug specifier|Conversion specifier|Format specifier|"
    r"class |For floating|Notes:|Since Python|encoding |errors |Perform |Splitting |"
    r"Consequently|This method|Representation|Description|Flag$|Meaning$|Conversion$|"
    r"Notes$|Unlike split)"
)


def load_str_lines() -> list[str]:
    lines: list[str] = []
    for line in SRC.read_text().splitlines():
        if line.startswith("Binary Sequence Types"):
            break
        lines.append(line)
    return lines


def is_repl_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if " can be used " in s or s.endswith(" section.") or "Accordingly" in s:
        return False
    if s in ("Representation", "Description", "Flag", "Meaning", "Conversion", "Notes"):
        return False
    if s.startswith(">>>"):
        return True
    if s.startswith("Traceback") or s.startswith("File "):
        return True
    if s in ("True", "False", "None"):
        return True
    if re.match(r"^-?\d+$", s):
        return True
    if s.startswith("<class"):
        return True
    if re.match(r"^[\w.]+\(", s):
        return True
    if s[0] in "'\"[" or s.startswith("b'") or s.startswith('b"'):
        return True
    if s.startswith("(") and ")" in s:
        return True
    if "Error" in s and "~~~~" in s:
        return True
    return False


def flush_code(out: list[str], buf: list[str]) -> None:
    if not buf:
        return
    cleaned = []
    for ln in buf:
        if ln.strip().startswith(">>>"):
            cleaned.append(ln.strip()[4:].strip())
        else:
            cleaned.append(ln)
    out.append("```python\n" + "\n".join(cleaned) + "\n```\n\n")


def format_version_note(line: str) -> str:
    m = re.match(r"^(Changed|Added|Removed) in version (\d+\.\d+): (.+)$", line)
    if m:
        kind, ver, rest = m.groups()
        return f"> **{kind} in version {ver}:** {rest}\n\n"
    return line + "\n\n"


def format_note_line(line: str) -> str:
    if line.startswith("Note "):
        return f"!!! note\n    {line[5:].strip()}\n\n"
    if line.startswith("See also "):
        return f"**See also:** {line[9:].strip()}\n\n"
    return line + "\n\n"


def parse_methods(lines: list[str]) -> dict[str, list[str]]:
    methods: dict[str, list[str]] = {}
    current: str | None = None
    buf: list[str] = []

    def flush():
        nonlocal buf, current
        if current and buf:
            methods[current] = buf
        buf = []

    for line in lines:
        m = re.match(r"^str\.(\w+)\(", line.strip())
        if m:
            flush()
            current = m.group(1)
            buf = [line]
            continue
        if current is not None:
            if line in {t[0] for t in TAIL_SECTIONS} or line == "String Methods":
                flush()
                current = None
                continue
            buf.append(line)
    flush()
    # Drop splitlines line-boundary table rows from scraped body (replaced by SPLITLINES_BOUNDARIES).
    if "splitlines" in methods:
        body = methods["splitlines"]
        pruned: list[str] = [body[0]]
        skip = False
        for line in body[1:]:
            if line.strip() == "This method splits on the following line boundaries":
                skip = True
                pruned.append(line)
                continue
            if skip:
                if line.strip().startswith("Changed in version") or line.strip().startswith("For example"):
                    skip = False
                    pruned.append(line)
                continue
            pruned.append(line)
        methods["splitlines"] = pruned
    return methods


def render_method_block(name: str, body: list[str]) -> str:
    sig = body[0].strip()
    out = [f"### `{sig}`\n\n"]
    i = 1
    code_buf: list[str] = []

    while i < len(body):
        line = body[i]
        stripped = line.strip()

        if re.match(r"^(Changed|Added|Removed) in version", stripped):
            flush_code(out, code_buf)
            code_buf = []
            out.append(format_version_note(stripped))
            i += 1
            continue

        if stripped.startswith("Note ") or stripped.startswith("See also "):
            flush_code(out, code_buf)
            code_buf = []
            out.append(format_note_line(stripped))
            i += 1
            continue

        if is_repl_line(line):
            code_buf.append(line)
            i += 1
            while i < len(body) and (is_repl_line(body[i]) or not body[i].strip()):
                if body[i].strip():
                    code_buf.append(body[i])
                i += 1
            continue

        if stripped and not PROSE_RE.match(stripped):
            # orphan output line — attach to code if pending
            if code_buf:
                code_buf.append(line)
                i += 1
                continue

        flush_code(out, code_buf)
        code_buf = []
        if stripped:
            out.append(stripped + "\n\n")
        i += 1

    flush_code(out, code_buf)
    return "".join(out)


def render_intro() -> str:
    return (
        "# [Text Sequence Type — str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)\n\n"
        "Textual data in Python is represented by **`str`** objects—**strings**. "
        "A string is an **immutable sequence of Unicode code points**: you can index and slice it like other sequences, "
        "but you cannot change a character in place. Full specification and edge cases remain on "
        "[docs.python.org](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str); "
        "this page explains how strings fit into everyday programming and how each major API behaves.\n\n"
        "---\n\n"
        "## Role of `str` in Python programs\n\n"
        "Strings are the default type for **human-readable text**, **identifiers**, **paths**, **URLs**, **JSON text**, "
        "and most data read from or written to files and networks after decoding. Because there is **no separate "
        "character type**, a single “character” is simply a string of length 1—for example `s[0]` and `s[0:1]` "
        "are equal for non-empty `s`.\n\n"
        "Immutability means every “change” builds a **new** string. For many small concatenations, "
        "`str.join()` on a list of fragments (or `io.StringIO`) is more efficient than repeated `+`.\n\n"
        "Strings implement all [**common sequence operations**](../sequence-types-list-tuple-range/common-sequence-operations/index.md) "
        "(indexing, slicing, membership, concatenation, repetition, length). "
        "They do **not** support mutable-sequence assignment (`s[i] = x`).\n\n"
        "---\n\n"
        "## String literals\n\n"
        "Literal syntax is defined in [String and Bytes literals](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals). "
        "In practice you will use:\n\n"
        "| Form | Example | When to use it |\n"
        "|------|---------|----------------|\n"
        "| Single-quoted | `'allows embedded \"double\" quotes'` | Default short text |\n"
        "| Double-quoted | `\"allows embedded 'single' quotes\"` | Same as single; pick quotes that avoid escaping |\n"
        "| Triple-quoted | `'''line1\\nline2'''`, `\"\"\"doc\"\"\"` | Multiline strings; **all** indentation on those lines is kept |\n"
        "| Adjacent literals | `\"spam \" \"eggs\"` → `\"spam eggs\"` | Implicit concatenation when only whitespace separates literals in one expression |\n"
        "| Raw `r\"...\"` | `r'\\n'` is backslash + `n`, not newline | Regex, Windows paths, literal backslashes |\n"
        "| `u\"...\"` (3.3+) | No effect on meaning | Legacy Python 2 marker only; cannot combine with `r` |\n\n"
        "```python\n"
        "assert \"spam \" \"eggs\" == \"spam eggs\"\n"
        "assert len('🐍') == 1\n"
        "assert 'abc'[0] == 'abc'[0:1] == 'a'\n"
        "```\n\n"
        "> **Changed in version 3.3:** The `u` prefix is permitted again for compatibility; it does not alter string semantics.\n\n"
        "---\n\n"
        "## Constructing strings with `str()`\n\n"
        "The built-in **`str`** constructor is overloaded. Behavior depends on whether you pass **`encoding`** or **`errors`**.\n\n"
        "### Informal string (`str(object)`)\n\n"
        "With no encoding arguments, `str(object)` calls `type(object).__str__(object)`—the **informal**, user-facing form. "
        "For an existing `str`, that is the string itself. Without `__str__`, Python falls back to `repr(object)`.\n\n"
        "```python\n"
        "assert str(42) == '42'\n"
        "assert str('hi') == 'hi'\n"
        "assert str(b'Zoot!') == \"b'Zoot!'\"\n"
        "```\n\n"
        "### Decoding bytes (`str(bytes, encoding, errors='strict')`)\n\n"
        "When **`encoding`** or **`errors`** is supplied, `object` must be **bytes-like**. "
        "`str(b, enc, err)` is equivalent to `b.decode(enc, err)`. "
        "See [Binary Sequence Types — bytes, bytearray, memoryview](../binary-sequence-types-bytes-bytearray-memoryview/index.md).\n\n"
        "```python\n"
        "raw = 'Python'.encode('utf-8')\n"
        "assert str(raw, 'utf-8') == 'Python'\n"
        "assert str() == ''\n"
        "```\n\n"
        "---\n\n"
        "## String methods — overview\n\n"
        "Strings add many methods beyond shared sequence operators. "
        "They also support **f-strings**, **`str.format()`**, and legacy **`%` printf-style** formatting.\n\n"
        "The [**Text Processing Services**](https://docs.python.org/3/library/text.html) library (`re`, `json`, `pathlib`, etc.) builds on these primitives.\n\n"
    )


def render_category_table() -> str:
    rows = [
        f"| [`str.{n}()`](#str{n}) | {title} | {blurb} |"
        for title, blurb, names in METHOD_CATEGORIES
        for n in names
    ]
    return (
        "## String methods (reference)\n\n"
        "| Method | Category | Typical use |\n"
        "|--------|----------|-------------|\n"
        + "\n".join(rows)
        + "\n\n---\n\n"
    )


def render_methods(methods: dict[str, list[str]]) -> str:
    parts = [render_category_table()]
    for title, blurb, names in METHOD_CATEGORIES:
        parts.append(f"### {title}\n\n")
        parts.append(
            f"Methods in this group {blurb}. Each returns a **new** string (or list/bool) "
            "unless noted; the original `str` is unchanged.\n\n"
        )
        for n in names:
            if n in methods:
                parts.append(f'<a id="str{n}"></a>\n\n')
                if n == "splitlines":
                    parts.append(
                        "Line boundaries recognized by `splitlines()` (superset of universal newlines):\n\n"
                        + SPLITLINES_BOUNDARIES
                        + "\n"
                    )
                parts.append(render_method_block(n, methods[n]))
        parts.append("---\n\n")
    return "".join(parts)


def slice_section(lines: list[str], start: str, end: str | None) -> list[str]:
    i = lines.index(start)
    j = lines.index(end) if end and end in lines else len(lines)
    return lines[i:j]


def render_prose_chunk(chunk: list[str], skip_headers: set[str]) -> str:
    out: list[str] = []
    i = 0
    code_buf: list[str] = []

    while i < len(chunk):
        line = chunk[i]
        if line in skip_headers:
            i += 1
            continue
        if line == "The conversion flag characters are:":
            flush_code(out, code_buf)
            code_buf = []
            out.append(line + "\n\n" + PRINTF_FLAG_TABLE + "\n")
            i += 1
            # skip until conversion types
            while i < len(chunk) and chunk[i] != "The conversion types are:":
                i += 1
            continue
        if line == "The conversion types are:":
            flush_code(out, code_buf)
            code_buf = []
            out.append(line + "\n\n" + PRINTF_CONVERSION_TABLE + "\n")
            i += 1
            while i < len(chunk):
                s = chunk[i].strip()
                if s in ("Flag", "Meaning", "Conversion", "Notes") or (
                    len(s) <= 3 and s.startswith(("'", '"')) and s.endswith(("'", '"'))
                ):
                    i += 1
                    continue
                if s.startswith("Changed in version") or s == "Binary Sequence Types — bytes, bytearray, memoryview":
                    break
                if PROSE_RE.match(s) or (s and not is_repl_line(chunk[i]) and s[0].isupper()):
                    break
                i += 1
            continue
        if line in ("Flag", "Meaning", "Conversion", "Notes", "Representation", "Description"):
            i += 1
            continue
        if re.match(r"^(Changed|Added|Removed) in version", line):
            flush_code(out, code_buf)
            code_buf = []
            out.append(format_version_note(line))
            i += 1
            continue
        if line.startswith("Note "):
            flush_code(out, code_buf)
            code_buf = []
            out.append(format_note_line(line))
            i += 1
            continue
        if is_repl_line(line):
            code_buf.append(line)
            i += 1
            while i < len(chunk) and (is_repl_line(chunk[i]) or not chunk[i].strip()):
                if chunk[i].strip():
                    code_buf.append(chunk[i])
                i += 1
            continue
        flush_code(out, code_buf)
        code_buf = []
        if line.strip():
            out.append(line.strip() + "\n\n")
        i += 1
    flush_code(out, code_buf)
    return "".join(out)


def render_tail_sections(lines: list[str]) -> str:
    parts: list[str] = []
    for idx, (title, slug, url) in enumerate(TAIL_SECTIONS):
        if title not in lines:
            continue
        parts.append(f"## [{title}]({url}) {{#{slug}}}\n\n")
        if title.startswith("Formatted"):
            parts.append(FSTR_SECTION)
        elif title.startswith("Template"):
            parts.append(TSTR_SECTION)
        else:
            parts.append(PRINTF_SECTION + PRINTF_FLAG_TABLE + "\nThe conversion types are:\n\n")
            parts.append(PRINTF_CONVERSION_TABLE)
            parts.append(
                "\n> **Changed in version 3.1:** `%f` for very large magnitudes is no longer silently switched to `%g`.\n\n"
                "Since Python `str` has an explicit length, `%s` does **not** treat `\\0` as end-of-string.\n"
            )
    return "".join(parts)


def main() -> None:
    lines = load_str_lines()
    methods = parse_methods(lines)
    doc = render_intro() + render_methods(methods) + render_tail_sections(lines)
    doc += (
        "\n---\n\n"
        "## Related topics in this guide\n\n"
        "| Subject | Description |\n"
        "|---------|-------------|\n"
        "| [Common Sequence Operations](../sequence-types-list-tuple-range/common-sequence-operations/index.md) | "
        "Indexing, slicing, and `in` shared by `str`, `list`, `tuple`, and others. |\n"
        "| [Binary Sequence Types — bytes, bytearray, memoryview](../binary-sequence-types-bytes-bytearray-memoryview/index.md) | "
        "Bytes-like objects, decoding, and the buffer protocol paired with `str.encode()`. |\n"
    )
    DST.write_text(doc, encoding="utf-8")
    print(f"Wrote {DST} ({len(doc)} chars, {doc.count(chr(10)) + 1} lines)")


if __name__ == "__main__":
    main()
