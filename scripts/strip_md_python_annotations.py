#!/usr/bin/env python3
"""Strip Python type annotations from ```python fenced blocks in markdown files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_IDENT = r"[A-Za-z_][\w.]*"
_QUOTED = r'(?:"[^"]*"|\'[^\']*\')'

KEYWORDS_BEFORE_COLON = frozenset({
    "if", "elif", "else", "for", "while", "class", "def", "return", "import",
    "from", "with", "try", "except", "raise", "assert", "match", "case",
    "lambda", "del", "global", "nonlocal", "yield", "pass", "break", "continue",
})

TYPING_NAMES = frozenset({
    "Any", "Optional", "Union", "List", "Dict", "Set", "Tuple",
    "TypeVar", "Generic", "Iterator", "Iterable", "Callable",
    "Protocol", "NamedTuple", "Literal", "Final", "ClassVar",
    "TYPE_CHECKING", "cast", "overload", "Annotated", "Hashable",
})


def _skip_ws(text: str, i: int) -> int:
    while i < len(text) and text[i] in " \t":
        i += 1
    return i


def _read_ident(text: str, i: int) -> int:
    m = re.match(_IDENT, text[i:])
    return i + m.end() if m else i


def _read_quoted(text: str, i: int) -> int:
    m = re.match(_QUOTED, text[i:])
    return i + m.end() if m else i


def parse_type(text: str, start: int) -> int | None:
    i = _skip_ws(text, start)
    if i >= len(text):
        return None

    if text.startswith("None", i) and (
        i + 4 >= len(text) or (not text[i + 4].isalnum() and text[i + 4] != "_")
    ):
        i += 4
    elif text[i] in "\"'":
        j = _read_quoted(text, i)
        if j == i:
            return None
        i = j
    else:
        j = _read_ident(text, i)
        if j == i:
            return None
        i = j

    while True:
        i = _skip_ws(text, i)
        if i < len(text) and text[i] == "[":
            depth = 0
            while i < len(text):
                if text[i] == "[":
                    depth += 1
                elif text[i] == "]":
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                i += 1
            else:
                return None
            continue

        i = _skip_ws(text, i)
        if i < len(text) and text[i] == "|":
            i += 1
            i = _skip_ws(text, i)
            if text.startswith("None", i) and (
                i + 4 >= len(text) or (not text[i + 4].isalnum() and text[i + 4] != "_")
            ):
                i += 4
            elif text[i] in "\"'":
                j = _read_quoted(text, i)
                if j == i:
                    return None
                i = j
            else:
                j = _read_ident(text, i)
                if j == i:
                    return None
                i = j
            continue
        break

    return i


def default_for_type(type_text: str) -> str:
    t = type_text.strip()
    if t == "int":
        return "0"
    if t == "str":
        return '""'
    if t == "float":
        return "0.0"
    if t == "bool":
        return "False"
    if t.startswith(("list[", "List[")):
        return "[]"
    if t.startswith(("dict[", "Dict[")):
        return "{}"
    if t.startswith(("set[", "Set[")):
        return "set()"
    if t.startswith(("tuple[", "Tuple[")):
        return "()"
    if t.startswith("deque[") or t == "deque":
        return "deque()"
    if "None" in t or "Optional" in t:
        return "None"
    return "None"


def strip_return_annotation(line: str) -> str:
    while True:
        arrow = line.find("->")
        if arrow == -1:
            break
        before = line[:arrow].rstrip()
        if not (before.endswith(")") or re.search(r"[\w)\]\"']\s*$", before)):
            break
        end = parse_type(line, arrow + 2)
        if end is None:
            break
        end = _skip_ws(line, end)
        if end < len(line) and line[end] == ":":
            line = line[:arrow].rstrip() + line[end:]
        else:
            break
    return line


def is_lambda_colon(line: str, name_start: int) -> bool:
    prefix = line[:name_start]
    return bool(re.search(r"\blambda\s+[\w*,\s]*$", prefix))


def strip_line_annotations(line: str, in_dataclass_body: bool = False) -> str:
    line = strip_return_annotation(line)

    changed = True
    while changed:
        changed = False
        for m in re.finditer(r"\b([A-Za-z_]\w*)\s*:", line):
            name = m.group(1)
            if name in KEYWORDS_BEFORE_COLON:
                continue
            if is_lambda_colon(line, m.start(1)):
                continue

            type_start = m.end()
            type_end = parse_type(line, type_start)
            if type_end is None:
                continue

            j = _skip_ws(line, type_end)
            if j < len(line) and line[j] in ",)=":
                line = line[: m.start(1)] + name + line[j:]
                changed = True
                break
            if j < len(line) and line[j] == "=":
                line = line[: m.start(1)] + name + line[j:]
                changed = True
                break
            if in_dataclass_body and (j >= len(line) or not line[j:].strip()):
                type_text = line[type_start:type_end]
                default = default_for_type(type_text)
                line = line[: m.start(1)] + f"{name} = {default}"
                changed = True
                break

    return line


def strip_typing_imports(code: str) -> str:
    lines = code.split("\n")
    out = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("from typing import"):
            names = stripped.split("import", 1)[1].strip()
            kept = []
            for part in re.split(r",\s*", names):
                part = part.strip()
                if part in TYPING_NAMES:
                    continue
                kept.append(part)
            if kept:
                out.append(f"from typing import {', '.join(kept)}")
            continue
        if stripped == "import typing" or stripped.startswith("import typing "):
            continue
        out.append(line)
    return "\n".join(out)


def strip_typevar_and_ignore(code: str) -> str:
    lines = []
    for line in code.split("\n"):
        if re.match(r"^\s*\w+\s*=\s*TypeVar\(", line):
            continue
        if re.match(r"^\s*#\s*type:\s*ignore", line):
            continue
        lines.append(line)
    return "\n".join(lines)


def strip_generic_bases(code: str) -> str:
    """Generic[K, V] -> plain class name in class headers."""
    lines = []
    for line in code.split("\n"):
        m = re.match(r"^(\s*class\s+\w+)\s*\([^)]*Generic\[[^\]]+\][^)]*\)\s*:", line)
        if m:
            cls = re.match(r"^(\s*class\s+\w+)", line)
            if cls:
                line = cls.group(1) + ":"
        lines.append(line)
    return "\n".join(lines)


def process_python_block(code: str) -> str:
    lines = code.split("\n")
    out: list[str] = []
    in_dataclass_body = False
    dataclass_indent = -1
    pending_dataclass = False

    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if stripped.startswith("@dataclass"):
            pending_dataclass = True
            out.append(line)
            continue

        if stripped.startswith("class "):
            in_dataclass_body = pending_dataclass
            pending_dataclass = False
            dataclass_indent = indent if in_dataclass_body else -1
            out.append(line)
            continue

        if in_dataclass_body and stripped and indent <= dataclass_indent:
            in_dataclass_body = False

        new_line = strip_line_annotations(line, in_dataclass_body=in_dataclass_body)
        out.append(new_line)

    result = "\n".join(out)
    result = strip_typing_imports(result)
    result = strip_typevar_and_ignore(result)
    result = strip_generic_bases(result)
    return result


PYTHON_BLOCK_RE = re.compile(r"(```python\n)(.*?)(```)", re.DOTALL)


def process_markdown(text: str) -> tuple[str, int]:
    changes = 0

    def replacer(m: re.Match) -> str:
        nonlocal changes
        prefix, code, suffix = m.group(1), m.group(2), m.group(3)
        new_code = process_python_block(code)
        if new_code != code:
            changes += 1
        return prefix + new_code + suffix

    new_text = PYTHON_BLOCK_RE.sub(replacer, text)
    return new_text, changes


def main(paths: list[str]) -> None:
    total_files = 0
    total_snippets = 0
    edited_files: list[str] = []

    for path_str in paths:
        path = Path(path_str)
        for md_file in sorted(path.rglob("*.md")):
            original = md_file.read_text(encoding="utf-8")
            new_text, snippets = process_markdown(original)
            if new_text != original:
                md_file.write_text(new_text, encoding="utf-8")
                edited_files.append(str(md_file))
                total_snippets += snippets
            total_files += 1

    print(f"Files scanned: {total_files}")
    print(f"Files edited: {len(edited_files)}")
    print(f"Python snippets changed: {total_snippets}")
    for f in edited_files:
        print(f"  {f}")


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "docs/dsa"
    main([root])
