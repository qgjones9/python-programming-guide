#!/usr/bin/env python3
"""Update built-in-functions parent index with short descriptions."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/versions/3.14.5/standard-library/built-in-functions"
INDEX = DOCS / "index.md"

ROWS: list[tuple[str, str, str]] = [
    ("abs", "abs()", "abs/index.md"),
    ("aiter", "aiter()", "aiter/index.md"),
    ("all", "all()", "all/index.md"),
    ("anext", "anext()", "anext/index.md"),
    ("any", "any()", "any/index.md"),
    ("ascii", "ascii()", "ascii/index.md"),
    ("bin", "bin()", "bin/index.md"),
    ("bool", "bool()", "bool/index.md"),
    ("breakpoint", "breakpoint()", "breakpoint/index.md"),
    ("bytearray", "bytearray()", "bytearray/index.md"),
    ("bytes", "bytes()", "bytes/index.md"),
    ("callable", "callable()", "callable/index.md"),
    ("chr", "chr()", "chr/index.md"),
    ("classmethod", "classmethod()", "classmethod/index.md"),
    ("compile", "compile()", "compile/index.md"),
    ("complex", "complex()", "complex/index.md"),
    ("delattr", "delattr()", "delattr/index.md"),
    ("dict", "dict()", "dict/index.md"),
    ("dir", "dir()", "dir/index.md"),
    ("divmod", "divmod()", "divmod/index.md"),
    ("enumerate", "enumerate()", "enumerate/index.md"),
    ("eval", "eval()", "eval/index.md"),
    ("exec", "exec()", "exec/index.md"),
    ("filter", "filter()", "filter/index.md"),
    ("float", "float()", "float/index.md"),
    ("format", "format()", "format/index.md"),
    ("frozenset", "frozenset()", "frozenset/index.md"),
    ("getattr", "getattr()", "getattr/index.md"),
    ("globals", "globals()", "globals/index.md"),
    ("hasattr", "hasattr()", "hasattr/index.md"),
    ("hash", "hash()", "hash/index.md"),
    ("help", "help()", "help/index.md"),
    ("hex", "hex()", "hex/index.md"),
    ("id", "id()", "id/index.md"),
    ("input", "input()", "input/index.md"),
    ("int", "int()", "int/index.md"),
    ("isinstance", "isinstance()", "isinstance/index.md"),
    ("issubclass", "issubclass()", "issubclass/index.md"),
    ("iter", "iter()", "iter/index.md"),
    ("len", "len()", "len/index.md"),
    ("list", "list()", "list/index.md"),
    ("locals", "locals()", "locals/index.md"),
    ("map", "map()", "map/index.md"),
    ("max", "max()", "max/index.md"),
    ("memoryview", "memoryview()", "memoryview/index.md"),
    ("min", "min()", "min/index.md"),
    ("next", "next()", "next/index.md"),
    ("object", "object()", "object/index.md"),
    ("oct", "oct()", "oct/index.md"),
    ("open", "open()", "open/index.md"),
    ("ord", "ord()", "ord/index.md"),
    ("pow", "pow()", "pow/index.md"),
    ("print", "print()", "print/index.md"),
    ("property", "property()", "property/index.md"),
    ("range", "range()", "range/index.md"),
    ("repr", "repr()", "repr/index.md"),
    ("reversed", "reversed()", "reversed/index.md"),
    ("round", "round()", "round/index.md"),
    ("set", "set()", "set/index.md"),
    ("setattr", "setattr()", "setattr/index.md"),
    ("slice", "slice()", "slice/index.md"),
    ("sorted", "sorted()", "sorted/index.md"),
    ("staticmethod", "staticmethod()", "staticmethod/index.md"),
    ("str", "str()", "str/index.md"),
    ("sum", "sum()", "sum/index.md"),
    ("super", "super()", "super/index.md"),
    ("tuple", "tuple()", "tuple/index.md"),
    ("type", "type()", "type/index.md"),
    ("vars", "vars()", "vars/index.md"),
    ("zip", "zip()", "zip/index.md"),
    ("import", "__import__()", "import/index.md"),
]


def load_descriptions() -> dict[str, str]:
    desc: dict[str, str] = {}
    scripts = ROOT / "scripts"

    part1 = scripts / "builtin-fn-descriptions-part1.json"
    if part1.exists():
        for item in json.loads(part1.read_text(encoding="utf-8")):
            desc[item["slug"]] = item["description"]

    part2 = scripts / "builtin-fn-descriptions-part2.json"
    if part2.exists():
        for item in json.loads(part2.read_text(encoding="utf-8")):
            desc[item["slug"]] = item["description"]

    for name in ("part3", "part4"):
        path = scripts / f"builtin-fn-descriptions-{name}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                desc.update(data)
            else:
                for item in data:
                    desc[item["slug"]] = item["description"]

    for slug, _, _ in ROWS:
        if slug in desc:
            continue
        page = DOCS / slug / "index.md"
        text = page.read_text(encoding="utf-8")
        m = re.search(r"## Description\s*\n\s*\n(.+)", text)
        if m:
            first = m.group(1).strip().split("\n")[0]
            desc[slug] = first.rstrip(".")
    return desc


def main() -> None:
    descriptions = load_descriptions()
    missing = [slug for slug, _, _ in ROWS if slug not in descriptions]
    if missing:
        raise SystemExit(f"Missing descriptions for: {', '.join(missing)}")

    lines = [
        "# [Built-in Functions](https://docs.python.org/3/library/functions.html)",
        "",
        "Teaching notes for Python's built-in functions. Each page links to the canonical "
        "docs.python.org entry and adds practical examples, use cases, and guidance.",
        "",
        "## Table of contents",
        "",
        "| Function | Description |",
        "|----------|-------------|",
    ]
    for slug, title, href in ROWS:
        link = f"[{title}]({href})"
        short = descriptions[slug].replace("|", "\\|")
        lines.append(f"| {link} | {short} |")
    lines.append("")

    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated index with {len(ROWS)} entries")


if __name__ == "__main__":
    main()
