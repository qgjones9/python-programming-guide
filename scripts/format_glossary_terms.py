#!/usr/bin/env python3
"""Format scraped glossary term index.md files (layout only)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY_DIR = ROOT / "docs" / "versions" / "3.14.5" / "glossary"

H1_RE = re.compile(
    r"^# \[[^\]]+\]\(https://docs\.python\.org/3\.14/glossary\.html#term-[^\)]+\)\s*$"
)
LIST_RE = re.compile(r"^(\s*)[-*+]\s+")
TABLE_ROW_RE = re.compile(r"^\|")
CODE_FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
HARD_BREAK_RE = re.compile(r"[.!?]\s*$")


def shell_sorted(names: list[str]) -> list[str]:
    import subprocess

    if not names:
        return []
    proc = subprocess.run(
        ["sort"],
        input="\n".join(names) + "\n",
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in proc.stdout.splitlines() if line]


def sorted_term_dirs(start: str, end: str) -> list[str]:
    names = shell_sorted(
        [p.name for p in GLOSSARY_DIR.iterdir() if p.is_dir()],
    )
    if start not in names or end not in names:
        raise SystemExit(f"Range bounds not found: {start!r} .. {end!r}")
    return names[names.index(start) : names.index(end) + 1]


def is_prose_continuation(prev: str, nxt: str) -> bool:
    prev = prev.rstrip()
    nxt = nxt.lstrip()
    if not prev or not nxt:
        return False
    if LIST_RE.match(nxt) or CODE_FENCE_RE.match(nxt) or TABLE_ROW_RE.match(nxt):
        return False
    if HARD_BREAK_RE.search(prev):
        return False
    return True


def needs_formatting(text: str) -> bool:
    lines = text.splitlines()
    prev: str | None = None
    in_fence = False
    for line in lines[1:]:
        if CODE_FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            prev = None
            continue
        if in_fence or not line.strip():
            prev = None
            continue
        if LIST_RE.match(line) or TABLE_ROW_RE.match(line):
            prev = None
            continue
        if prev is not None and is_prose_continuation(prev, line):
            return True
        prev = line
    return False


def join_prose_lines(lines: list[str]) -> str:
    parts: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if parts and parts[-1].endswith(("-", "–", "—")):
            parts[-1] = parts[-1][:-1] + stripped
        elif parts:
            parts.append(" " + stripped)
        else:
            parts.append(stripped)
    return "".join(parts)


def parse_list_item(lines: list[str], start: int) -> tuple[str, int]:
    m = LIST_RE.match(lines[start])
    assert m
    indent = len(m.group(1))
    body = lines[start][m.end() :].strip()
    i = start + 1
    while i < len(lines):
        raw = lines[i]
        if not raw.strip():
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and is_prose_continuation(body, lines[j]):
                i = j
                body = join_prose_lines([body, lines[j].strip()])
                i += 1
                continue
            break
        if LIST_RE.match(raw) or CODE_FENCE_RE.match(raw) or TABLE_ROW_RE.match(raw):
            break
        if is_prose_continuation(body, raw) or (
            len(raw) - len(raw.lstrip()) > indent and not LIST_RE.match(raw)
        ):
            body = join_prose_lines([body, raw.strip()])
            i += 1
            continue
        break
    return body, i


def list_items_to_table(items: list[str]) -> list[str] | None:
    rows: list[str] = []
    for item in items:
        if " — " in item:
            term, _, rest = item.partition(" — ")
        elif " - " in item and item.index(" - ") < 80:
            term, _, rest = item.partition(" - ")
        else:
            return None
        rows.append(f"| {term.strip()} | {rest.strip()} |")
    if len(rows) < 3:
        return None
    return ["| Term | Description |", "|------|-------------|", *rows]


def format_body_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        if CODE_FENCE_RE.match(line):
            block = [line]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                if CODE_FENCE_RE.match(lines[i]) and len(block) > 1:
                    i += 1
                    break
                i += 1
            if out and out[-1] != "":
                out.append("")
            out.extend(block)
            out.append("")
            continue

        if LIST_RE.match(line):
            items: list[str] = []
            while i < len(lines) and LIST_RE.match(lines[i]):
                body, i = parse_list_item(lines, i)
                items.append(body)
            table = list_items_to_table(items)
            if out and out[-1] != "":
                out.append("")
            if table:
                out.extend(table)
            else:
                for item in items:
                    out.append(f"- {item}")
            out.append("")
            continue

        if TABLE_ROW_RE.match(line):
            block = []
            while i < len(lines) and TABLE_ROW_RE.match(lines[i]):
                block.append(lines[i])
                i += 1
            if out and out[-1] != "":
                out.append("")
            out.extend(block)
            out.append("")
            continue

        prose: list[str] = [line.rstrip()]
        i += 1
        while i < len(lines):
            if not lines[i].strip():
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and is_prose_continuation(prose[-1], lines[j]):
                    prose.append(lines[j].rstrip())
                    i = j + 1
                    continue
                break
            nxt = lines[i]
            if LIST_RE.match(nxt) or CODE_FENCE_RE.match(nxt) or TABLE_ROW_RE.match(nxt):
                break
            if not is_prose_continuation(prose[-1], nxt):
                break
            prose.append(nxt.rstrip())
            i += 1
        if out and out[-1] != "":
            out.append("")
        out.append(join_prose_lines(prose))
        out.append("")

    while out and out[-1] == "":
        out.pop()
    return out


def format_file(path: Path) -> tuple[bool, str | None]:
    original = path.read_text(encoding="utf-8")
    if not needs_formatting(original):
        return False, None

    lines = original.splitlines()
    if not lines or not H1_RE.match(lines[0]):
        return False, f"unexpected H1 in {path}"

    h1 = lines[0]
    body_lines = lines[1:]
    while body_lines and not body_lines[0].strip():
        body_lines = body_lines[1:]

    formatted_body = format_body_lines(body_lines)
    result = h1 + "\n\n" + "\n".join(formatted_body) + "\n"

    if result == original:
        return False, None

    path.write_text(result, encoding="utf-8")
    return True, None


def all_term_dirs() -> list[str]:
    return shell_sorted(
        [p.name for p in GLOSSARY_DIR.iterdir() if p.is_dir() and (p / "index.md").is_file()],
    )


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if a != "--all"]
    if "--all" in argv[1:]:
        dirs = all_term_dirs()
    else:
        start = args[0] if args else "docstring"
        end = args[1] if len(args) > 1 else "iterator"
        dirs = sorted_term_dirs(start, end)

    edited = 0
    skipped = 0
    issues: list[str] = []

    for name in dirs:
        path = GLOSSARY_DIR / name / "index.md"
        if not path.is_file():
            issues.append(f"missing {path}")
            continue
        try:
            changed, issue = format_file(path)
        except Exception as exc:  # noqa: BLE001 — report and continue
            issues.append(f"{name}: {exc}")
            continue
        if issue:
            issues.append(issue)
        if changed:
            edited += 1
        else:
            skipped += 1

    print(f"Edited: {edited}")
    print(f"Skipped: {skipped}")
    if issues:
        print("Issues:")
        for item in issues:
            print(f"  - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
