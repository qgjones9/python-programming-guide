#!/usr/bin/env python3
"""Format scraped stdtypes bytes/bytearray/memoryview section into teaching markdown."""
from __future__ import annotations

import re
from pathlib import Path

SRC = Path(
    "/home/qjones/.cursor/projects/home-qjones-workspace-python-programming-guide/"
    "uploads/index-L3-L1132-0.md"
)
DST = Path(
    "/home/qjones/workspace/python-programming-guide/docs/versions/3.14.5/"
    "standard-library/built-in-types/binary-sequence-types-bytes-bytearray-memoryview/"
    "index.md"
)

BASE = "https://docs.python.org/3/library/stdtypes.html"

METHOD_CATEGORIES = [
    (
        "Search, test, and count",
        "find where subsequences occur, test boundaries, or count matches",
        ["count", "find", "rfind", "index", "rindex", "startswith", "endswith"],
    ),
    (
        "Split, join, and partition",
        "break binary data apart or concatenate bytes-like iterables",
        ["split", "rsplit", "splitlines", "partition", "rpartition", "join"],
    ),
    (
        "Strip, prefix, and suffix",
        "trim edges or remove/add fixed byte affixes",
        ["strip", "lstrip", "rstrip", "removeprefix", "removesuffix"],
    ),
    (
        "Padding and alignment",
        "pad or align binary data in a fixed-width field",
        ["center", "ljust", "rjust", "zfill", "expandtabs"],
    ),
    (
        "Transform and decode",
        "replace content, translate bytes, or decode to `str`",
        ["replace", "translate", "maketrans", "decode"],
    ),
    (
        "Case and title (ASCII)",
        "change ASCII letter case for display or comparisons",
        [
            "capitalize",
            "lower",
            "upper",
            "swapcase",
            "title",
        ],
    ),
    (
        "Classification (`is*` methods, ASCII)",
        "test ASCII character categories",
        ["isalnum", "isalpha", "isascii", "isdigit", "islower", "isspace", "istitle", "isupper"],
    ),
]

MEMORYVIEW_METHODS = [
    "__eq__",
    "tobytes",
    "hex",
    "tolist",
    "toreadonly",
    "release",
    "cast",
    "count",
    "index",
]

MEMORYVIEW_ATTRS = [
    "obj",
    "nbytes",
    "readonly",
    "format",
    "itemsize",
    "ndim",
    "shape",
    "strides",
    "suboffsets",
    "c_contiguous",
    "f_contiguous",
    "contiguous",
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
| `u` | Obsolete; same as `d`. | (8) |
| `x` | Signed hex (lowercase). | (2) alternate: `0x`. |
| `X` | Signed hex (uppercase). | (2) alternate: `0X`. |
| `e` | Float, exponential (lowercase). | (3) |
| `E` | Float, exponential (uppercase). | (3) |
| `f` | Float, decimal format. | (3) |
| `F` | Float, decimal format. | (3) |
| `g` | Float; uses `%e` or `%f` style by magnitude. | (4) |
| `G` | Like `g` but uppercase exponent. | (4) |
| `c` | Single byte (int or single-byte object). | |
| `b` | Bytes (buffer protocol or `__bytes__()`). | (5) |
| `s` | Alias for `b` (legacy Python 2/3). | (6) deprecated |
| `a` | Bytes via `repr(obj).encode('ascii', 'backslashreplace')`. | (5) |
| `r` | Alias for `a` (legacy Python 2/3). | (7) deprecated |
| `%` | Literal `%` in the result. | |

**Notes:** (1) octal alternate form; (2) hex alternate `0x`/`0X`; (3) precision defaults to 6 fractional digits; (4) `%g`/`%G` significant digits; (5) buffer/`__bytes__`; (6)(7) deprecated aliases; (8) `%u` obsolete. See [PEP 461](https://peps.python.org/pep-0461/) and [PEP 237](https://peps.python.org/pep-0237/).
"""

PROSE_RE = re.compile(
    r"^(Return |Like |Similar |If |When |Since |The |See |For |Unlike |Here |"
    r"Changed|Added|Note |See also|Bytes |Bytearray |Both |Some |A conversion|"
    r"Mapping |Minimum |Precision |Length |Rather |Format |Whitespace |"
    r"By default|class |Splitting |Consequently|This method|Representation|"
    r"Description|Flag$|Meaning$|Conversion$|Notes$|Unlike split|Also see|"
    r"Firstly|Only |As with |While |In addition|A reverse|Since 2 |There is|"
    r"Creating |Copying |From an|A zero-filled|memoryview |len\(|One-dimensional|"
    r"Multi-dimensional|Cast |Count |Raises |An integer|A bool|A string|Used |"
    r"For information|After this|The context|The destination|The itemsize|"
    r"If format|If the |If either|If sub |If sep |Note that|Lowercase |Uppercase |"
    r"A memoryview|Many objects|Cast 1D|import |def |Examples:|Examples$|"
    r"Resize |If the bytearray|This is equivalent|Since bytearray|Since bytes|"
    r"printf-style|Memory Views$|Bytes Objects$|Bytearray Objects$|"
    r"Bytes and Bytearray Operations$|In this |Bytes objects \(bytes)"
)


def load_lines() -> list[str]:
    return SRC.read_text(encoding="utf-8").splitlines()


def is_repl_line(line: str) -> bool:
    s = line.strip()
    if not s:
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
    if s.startswith("<") and ("memory" in s or "class" in s):
        return True
    if re.match(r"^[\w.]+\(", s):
        if any(w in s for w in (" is equal ", " must ", " will ", " that ", " which ", " allow ")):
            return False
        return True
    if s[0] in "'\"[{" or s.startswith("b'") or s.startswith('b"'):
        return True
    if s.startswith("(") and ")" in s:
        return True
    if s.startswith("[") and "]" in s:
        return True
    if "Error" in s and "~~~~" in s:
        return True
    if s.startswith("bytearray("):
        return True
    if re.match(r"^[\w.]+ == ", s):
        return True
    if re.match(r"^(import |from )", s):
        return True
    if re.match(r"^[\w.]+\s*=", s):
        return True
    if s.startswith("def "):
        return True
    if s.startswith("class ") and s.endswith(":"):
        return True
    if s.endswith(("\\", "%", "(", "{")):
        return True
    return False


def is_signature_line(line: str) -> bool:
    s = line.strip()
    return bool(
        re.match(r"^class (bytes|bytearray)\(", s)
        or re.match(r"^classmethod \w+", s)
        or re.match(r"^hex\(", s)
        or re.match(r"^resize\(", s)
    )


def format_signature_heading(line: str, owner: str) -> str:
    s = line.strip()
    if s.startswith("classmethod "):
        return f"### `{owner}.{s[len('classmethod '):]}`\n\n"
    if s.startswith("hex("):
        return f"### `{owner}.hex(...)`\n\n"
    if s.startswith("resize("):
        return f"### `bytearray.{s}`\n\n"
    if s.startswith("class "):
        return f"### `{s}`\n\n"
    return f"### `{s}`\n\n"


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
    m = re.match(r"^(Changed|Added|Removed) in version (\d+\.\d+)[:.]?\s*(.*)$", line)
    if m:
        kind, ver, rest = m.groups()
        if rest:
            return f"> **{kind} in version {ver}:** {rest}\n\n"
        return f"> **{kind} in version {ver}.**\n\n"
    return line + "\n\n"


def format_note_line(line: str) -> str:
    if line.startswith("Note "):
        return f"!!! note\n    {line[5:].strip()}\n\n"
    if line.startswith("See also "):
        rest = line[9:].strip()
        if rest.startswith("For "):
            return f"**See also:** {rest}\n\n"
        return f"**See also:** {rest}\n\n"
    return line + "\n\n"


def slice_section(lines: list[str], start: str, end: str | None) -> list[str]:
    i = lines.index(start)
    j = lines.index(end) if end and end in lines else len(lines)
    return lines[i:j]


def render_prose_chunk(
    chunk: list[str],
    skip_headers: set[str] | None = None,
    owner: str = "bytes",
) -> str:
    skip_headers = skip_headers or set()
    out: list[str] = []
    i = 0
    code_buf: list[str] = []

    while i < len(chunk):
        line = chunk[i]
        if line in skip_headers:
            i += 1
            continue
        if line in ("Flag", "Meaning", "Conversion", "Notes", "Representation", "Description"):
            i += 1
            continue
        if line == "The conversion flag characters are:":
            flush_code(out, code_buf)
            code_buf = []
            out.append(line + "\n\n" + PRINTF_FLAG_TABLE + "\n")
            i += 1
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
                if s.startswith("Changed in version") or s.startswith("Added in version"):
                    break
                if s.startswith("See also") or s == "Memory Views":
                    break
                if PROSE_RE.match(s) or (s and not is_repl_line(chunk[i]) and s[0].isupper()):
                    break
                i += 1
            continue
        if re.match(r"^(Changed|Added|Removed) in version", line.strip()):
            flush_code(out, code_buf)
            code_buf = []
            out.append(format_version_note(line.strip()))
            i += 1
            continue
        if is_signature_line(line):
            flush_code(out, code_buf)
            code_buf = []
            stripped_sig = line.strip()
            if stripped_sig.startswith("hex(") and out and out[-1].startswith("### `") and ".hex(" in out[-1]:
                i += 1
                continue
            sig_owner = "bytearray" if stripped_sig.startswith("resize(") else owner
            out.append(format_signature_heading(line, sig_owner))
            i += 1
            continue
        if line.startswith("Note ") or line.startswith("See also "):
            flush_code(out, code_buf)
            code_buf = []
            out.append(format_note_line(line))
            i += 1
            continue
        if is_repl_line(line):
            code_buf.append(line)
            i += 1
            while i < len(chunk):
                nxt = chunk[i]
                if not nxt.strip():
                    i += 1
                    continue
                if re.match(r"^(Changed|Added|Removed) in version", nxt.strip()):
                    break
                if nxt.startswith("Note ") or nxt.startswith("See also "):
                    break
                if is_signature_line(nxt) and not code_buf[-1].strip().endswith(("{", "(", "%", "\\")):
                    break
                if PROSE_RE.match(nxt.strip()) and not is_repl_line(nxt):
                    break
                code_buf.append(nxt)
                i += 1
            continue
        flush_code(out, code_buf)
        code_buf = []
        stripped = line.strip()
        if stripped in (
            "Single quotes:", "Double quotes:", "Triple quoted:",
            "A zero-filled bytes object of a specified length: bytes(10)",
            "From an iterable of integers: bytes(range(20))",
            "Copying existing binary data via the buffer protocol: bytes(obj)",
            "Creating an empty instance: bytearray()",
            "Creating a zero-filled instance with a given length: bytearray(10)",
        ):
            i += 1
            continue
        if stripped and stripped not in skip_headers:
            out.append(stripped + "\n\n")
        i += 1
    flush_code(out, code_buf)
    return "".join(out)


def parse_bytes_methods(lines: list[str]) -> dict[str, list[str]]:
    methods: dict[str, list[str]] = {}
    current: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal buf, current
        if current and buf:
            methods[current] = buf
        buf = []

    for line in lines:
        stripped = line.strip()
        m = re.match(r"^(?:static )?bytes\.(\w+)\(", stripped)
        if m:
            flush()
            current = m.group(1)
            buf = [stripped.replace("static bytes.", "bytes.")]
            continue
        if re.match(r"^bytearray\.\w+\(", stripped):
            if current is not None:
                continue
            continue
        if current is not None:
            if stripped == "printf-style Bytes Formatting":
                flush()
                current = None
                continue
            buf.append(line)
    flush()
    return methods


def parse_memoryview_methods(lines: list[str]) -> dict[str, list[str]]:
    methods: dict[str, list[str]] = {}
    current: str | None = None
    buf: list[str] = []
    in_methods = False

    def flush() -> None:
        nonlocal buf, current
        if current and buf:
            methods[current] = buf
        buf = []

    for line in lines:
        stripped = line.strip()
        if stripped == "memoryview has several methods:":
            in_methods = True
            continue
        if stripped == "There are also several readonly attributes available:":
            flush()
            current = None
            in_methods = False
            continue
        if not in_methods:
            continue
        m = re.match(r"^(__\w+|\w+)\(", stripped)
        if m and not stripped.startswith("class "):
            flush()
            current = m.group(1)
            buf = [stripped]
            continue
        if current is not None:
            buf.append(line)
    flush()
    return methods


def parse_memoryview_attrs(lines: list[str]) -> dict[str, list[str]]:
    attrs: dict[str, list[str]] = {}
    current: str | None = None
    buf: list[str] = []
    in_attrs = False

    def flush() -> None:
        nonlocal buf, current
        if current and buf:
            attrs[current] = buf
        buf = []

    for line in lines:
        stripped = line.strip()
        if stripped == "There are also several readonly attributes available:":
            in_attrs = True
            continue
        if not in_attrs:
            continue
        if stripped.startswith("For information on the thread safety"):
            flush()
            break
        if stripped in MEMORYVIEW_ATTRS:
            flush()
            current = stripped
            buf = []
            continue
        if current is not None:
            buf.append(line)
    flush()
    return attrs


def render_method_block(name: str, body: list[str], prefix: str = "bytes") -> str:
    sig = body[0].strip()
    if not sig.startswith(f"{prefix}."):
        sig = f"{prefix}.{sig}" if not sig.startswith("__") else sig
    out = [f"### `{sig}`\n\n"]
    i = 1
    code_buf: list[str] = []

    while i < len(body):
        line = body[i]
        stripped = line.strip()

        if re.match(r"^bytearray\.\w+\(", stripped):
            i += 1
            continue

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
                if body[i].strip() and not re.match(r"^bytearray\.\w+\(", body[i].strip()):
                    code_buf.append(body[i])
                i += 1
            continue

        if stripped and not PROSE_RE.match(stripped):
            if code_buf:
                code_buf.append(line)
                i += 1
                continue

        flush_code(out, code_buf)
        code_buf = []
        if stripped and not re.match(r"^bytearray\.\w+\(", stripped):
            out.append(stripped + "\n\n")
        i += 1

    flush_code(out, code_buf)
    return "".join(out)


def render_intro() -> str:
    return (
        f"# [Binary Sequence Types — bytes, bytearray, memoryview]({BASE}/"
        "#binary-sequence-types-bytes-bytearray-memoryview)\n\n"
        "Binary data in Python is handled by **`bytes`** (immutable) and **`bytearray`** "
        "(mutable)—sequences of integers in `0..255`. **`memoryview`** exposes another "
        "object's buffer without copying. Full specification remains on "
        f"[docs.python.org]({BASE}/#binary-sequence-types-bytes-bytearray-memoryview); "
        "this page explains how these types fit everyday I/O, networking, and parsing.\n\n"
        "---\n\n"
        "## Role of binary types in Python programs\n\n"
        "**`bytes`** is the natural result of **`str.encode()`** and of reading files opened "
        "in binary mode. **`bytearray`** is useful when you must mutate a buffer in place "
        "(for example resizing or patching packet fields). **`memoryview`** lets C extensions, "
        "`struct`, and `array` share memory efficiently.\n\n"
        "For typed numeric arrays (32-bit ints, doubles), see the [**`array`**](https://docs.python.org/3/library/array.html) "
        "module. Pair decoding with the [**Text Sequence Type — str**](../text-sequence-type-str/index.md) "
        "(`decode` / `encode`).\n\n"
        "Both `bytes` and `bytearray` implement [**common sequence operations**]"
        "(../sequence-types-list-tuple-range/common-sequence-operations/index.md). "
        "Indexing returns an **`int`**; slicing returns a **`bytes`** or **`bytearray`** "
        "object of length 1—unlike `str`, where `s[0]` and `s[0:1]` are both strings.\n\n"
        "---\n\n"
    )


def _trim_intro_chunk(chunk: list[str], marker: str) -> list[str]:
    for idx, line in enumerate(chunk):
        if line.strip().startswith(marker):
            return chunk[idx:]
    return chunk[1:]


def render_bytes_intro(chunk: list[str]) -> str:
    body = render_prose_chunk(
        _trim_intro_chunk(chunk, "Since 2 hexadecimal"),
        {"Bytes Objects"},
        owner="bytes",
    )
    return (
        f"## [Bytes objects]({BASE}/#bytes-objects)\n\n"
        "**`bytes`** objects are **immutable** sequences of single bytes (`0 <= x < 256`). "
        "Many wire formats are ASCII-based, so several methods mirror `str` but only for "
        "ASCII-compatible data—avoid those on arbitrary binary payloads.\n\n"
        "### Construction and literals\n\n"
        "| Form | Example |\n|------|--------|\n"
        "| Literal (ASCII only) | `b'hello'`, `b\"double quotes ok\"`, `b'''triple'''` |\n"
        "| Raw literal | `rb'\\n'` disables escape processing |\n"
        "| Zero-filled | `bytes(10)` |\n"
        "| From ints | `bytes(range(256))` |\n"
        "| Buffer copy | `bytes(existing_bytes_like)` |\n\n"
        "Literal rules match [String and Bytes literals](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals) "
        "with a **`b`** prefix; only ASCII code points may appear literally—use escapes for values above 127.\n\n"
        + body
        + "\n---\n\n"
    )


def render_bytearray_intro(chunk: list[str]) -> str:
    body = render_prose_chunk(
        _trim_intro_chunk(chunk, "Since 2 hexadecimal"),
        {"Bytearray Objects"},
        owner="bytearray",
    )
    return (
        f"## [Bytearray objects]({BASE}/#bytearray-objects)\n\n"
        "**`bytearray`** is the **mutable** counterpart to `bytes`. There is no literal "
        "syntax—always call the constructor. Mutable-sequence operations apply in addition "
        "to the shared bytes API below.\n\n"
        "| Form | Example |\n|------|--------|\n"
        "| Empty | `bytearray()` |\n"
        "| Zero-filled | `bytearray(10)` |\n"
        "| From ints | `bytearray(range(20))` |\n"
        "| Buffer copy | `bytearray(b'Hi!')` |\n\n"
        + body
        + "\n---\n\n"
    )


def render_category_table() -> str:
    rows = [
        f"| [`bytes.{n}()` / `bytearray.{n}()`](#bytes{n}) | {title} | {blurb} |"
        for title, blurb, names in METHOD_CATEGORIES
        for n in names
    ]
    return (
        f"## [Bytes and bytearray methods (reference)]({BASE}/#bytes-and-bytearray-operations)\n\n"
        "Methods below are shared by **`bytes`** and **`bytearray`** unless noted. "
        "Operands may be any **bytes-like object**; return type may depend on operand order. "
        "Methods do **not** accept `str` arguments (use encoded bytes instead).\n\n"
        "!!! note\n"
        "    ASCII-oriented methods (`isalpha`, `lower`, `split` with default whitespace, etc.) "
        "assume ASCII-compatible data. On arbitrary binary, prefer the **binary-safe** group "
        "or pass explicit byte arguments.\n\n"
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
            f"Methods in this group {blurb}. Each returns a **new** `bytes` or `bytearray` "
            "(or `str` / `bool` / `list`) unless noted; **`bytearray` methods never mutate in place**.\n\n"
        )
        for n in names:
            if n in methods:
                parts.append(f'<a id="bytes{n}"></a>\n\n')
                parts.append(render_method_block(n, methods[n]))
        parts.append("---\n\n")
    return "".join(parts)


def render_printf_section(chunk: list[str]) -> str:
    trimmed = _trim_intro_chunk(chunk, "When the right argument is a dictionary")
    body = render_prose_chunk(trimmed)
    return (
        f"## [printf-style bytes formatting]({BASE}/#printf-style-bytes-formatting)\n\n"
        "!!! note\n"
        "    These operations have historical quirks (e.g. failing to display tuples and dicts). "
        "Prefer **`bytes.join()`**, f-strings on `str`, or explicit struct packing for new code.\n\n"
        "The **`%`** operator on **`bytes`** / **`bytearray`** performs **printf-style interpolation**: "
        "`format % values` replaces conversion specifications in `format`, similar to C `sprintf`.\n\n"
        "- **Single argument:** `values` may be a non-tuple when the format expects one conversion.\n"
        "- **Multiple arguments:** `values` must be a **tuple** of the right length, or a **mapping** "
        "for `%(name)s` keys (no `*` width/precision from a mapping).\n\n"
        + body
        + "\n> **Added in version 3.5:** See [PEP 461 — Adding % formatting to bytes and bytearray]"
        "(https://peps.python.org/pep-0461/).\n\n---\n\n"
    )


def render_memoryview_intro(chunk: list[str]) -> str:
    end = chunk.index("memoryview has several methods:")
    trimmed = _trim_intro_chunk(chunk[1:end], "A memoryview has the notion")
    return (
        f"## [memoryview]({BASE}/#memory-views)\n\n"
        "**`memoryview`** references another object's **buffer protocol** memory **without copying**. "
        "Built-in exporters include `bytes`, `bytearray`, and `array.array`. "
        "An **element** is the atomic unit (often one byte).\n\n"
        "### `memoryview(object)`\n\n"
        "Create a memoryview referencing a **buffer protocol** object. "
        "**`memoryview`** is a **generic type** (3.14+) over the underlying element type.\n\n"
        + render_prose_chunk(trimmed)
        + "\n"
    )


def render_memoryview_methods(methods: dict[str, list[str]]) -> str:
    parts = ["### Methods\n\n"]
    for n in MEMORYVIEW_METHODS:
        if n in methods:
            parts.append(f'<a id="memoryview{n}"></a>\n\n')
            sig = methods[n][0].strip()
            parts.append(render_method_block(n, methods[n], prefix="memoryview").replace(
                f"### `{sig}`", f"### `memoryview.{sig}`", 1
            ) if not sig.startswith("memoryview") else render_method_block(n, methods[n], prefix="memoryview"))
    return "".join(parts)


def render_memoryview_attrs(attrs: dict[str, list[str]]) -> str:
    parts = ["### Read-only attributes\n\n"]
    for n in MEMORYVIEW_ATTRS:
        if n in attrs:
            parts.append(f"#### `memoryview.{n}`\n\n")
            parts.append(render_prose_chunk(attrs[n]))
    parts.append(
        "**See also:** [Thread safety for memoryview objects]"
        "(https://docs.python.org/3/library/stdtypes.html#thread-safety-for-memoryview-objects) "
        "in the free-threaded build.\n\n"
    )
    return "".join(parts)


def render_related() -> str:
    return (
        "---\n\n"
        "## Related topics in this guide\n\n"
        "| Subject | Description |\n"
        "|---------|-------------|\n"
        "| [Text Sequence Type — str](../text-sequence-type-str/index.md) | "
        "`str.encode()` / `bytes.decode()` and text processing paired with binary data. |\n"
        "| [Common Sequence Operations](../sequence-types-list-tuple-range/common-sequence-operations/index.md) | "
        "Indexing, slicing, and `in` shared by bytes-like types, lists, and tuples. |\n"
    )


def main() -> None:
    lines = load_lines()
    bytes_chunk = slice_section(lines, "Bytes Objects", "Bytearray Objects")
    bytearray_chunk = slice_section(lines, "Bytearray Objects", "Bytes and Bytearray Operations")
    ops_chunk = slice_section(lines, "Bytes and Bytearray Operations", "printf-style Bytes Formatting")
    printf_chunk = slice_section(lines, "printf-style Bytes Formatting", "Memory Views")
    mv_chunk = slice_section(lines, "Memory Views", None)

    methods = parse_bytes_methods(ops_chunk)
    mv_methods = parse_memoryview_methods(mv_chunk)
    mv_attrs = parse_memoryview_attrs(mv_chunk)

    doc = (
        render_intro()
        + render_bytes_intro(bytes_chunk)
        + render_bytearray_intro(bytearray_chunk)
        + render_methods(methods)
        + render_printf_section(printf_chunk)
        + render_memoryview_intro(mv_chunk)
        + render_memoryview_methods(mv_methods)
        + render_memoryview_attrs(mv_attrs)
        + render_related()
    )
    DST.write_text(doc, encoding="utf-8")
    print(f"Wrote {DST} ({len(doc)} chars, {doc.count(chr(10)) + 1} lines)")


if __name__ == "__main__":
    main()
