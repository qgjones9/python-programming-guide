#!/usr/bin/env python3
"""Split standard-library index table into section indexes and regenerate mkdocs nav.

Hierarchy source of truth: https://docs.python.org/3/library/index.html (toctree).
Run ``python scripts/restructure_standard_library.py`` after editing
``scripts/standard-library-module-table.md``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
STD_LIB = ROOT / "docs/python/3.14.5/standard-library"
MKDOCS = ROOT / "mkdocs.yml"
NAV_PREFIX = "python/3.14.5/standard-library"
TABLE_SOURCE = ROOT / "scripts/standard-library-module-table.md"


def parse_table(text: str) -> list[tuple[str, str, str, str]]:
    """Return list of (category, link_text, rel_path, description)."""
    rows: list[tuple[str, str, str, str]] = []
    current_category = ""
    for line in text.splitlines():
        if not line.startswith("|") or line.startswith("|--"):
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) != 3:
            continue
        category, link_col, desc = parts
        if category:
            current_category = category
        match = re.search(r"\[([^\]]+)\]\(([^)]+)\)", link_col)
        if not match:
            continue
        link_text, rel_path = match.group(1), match.group(2)
        rows.append((current_category, link_text, rel_path, desc))
    return rows


def slug_from_path(rel_path: str) -> str:
    return rel_path.removesuffix("/index.md")


def group_sections(rows: list[tuple[str, str, str, str]]) -> list[dict]:
    sections: list[dict] = []
    index: dict[str, dict] = {}
    order: list[str] = []
    for category, link_text, rel_path, desc in rows:
        slug = slug_from_path(rel_path)
        top_slug = slug.split("/")[0]
        if top_slug not in index:
            section = {
                "category": category,
                "slug": top_slug,
                "rows": [],
            }
            index[top_slug] = section
            sections.append(section)
            order.append(top_slug)
        index[top_slug]["rows"].append((category, link_text, rel_path, desc))
    return sections


def render_section_table(rows: list[tuple[str, str, str, str]], slug: str) -> str:
    lines = [
        "| Module/Link | Description |",
        "|-------------|-------------|",
    ]
    for _category, link_text, rel_path, desc in rows:
        child_slug = slug_from_path(rel_path)
        if child_slug == slug:
            continue
        child_name = child_slug.split("/")[-1]
        link = f"[{link_text}]({child_name}/index.md)"
        lines.append(f"| {link} | {desc} |")
    return "\n".join(lines)


def strip_generated_tail(existing: str) -> str:
    """Remove prior table-of-contents blocks and local child index link headers."""
    lines = existing.splitlines()
    toc_idx = next(
        (i for i, line in enumerate(lines) if line.startswith("## Table of contents")),
        None,
    )
    if toc_idx is not None:
        lines = lines[:toc_idx]

    local_child_pattern = re.compile(r"^## \[.+\]\([^/\)]+\/index\.md\)\s*$")
    filtered = [line for line in lines if not local_child_pattern.match(line.strip())]

    while filtered and filtered[-1].strip() == "":
        filtered.pop()
    return "\n".join(filtered)


def update_section_index(section: dict) -> None:
    slug = section["slug"]
    path = STD_LIB / slug / "index.md"
    if not path.exists():
        print(f"WARN: missing section index: {path}")
        return

    existing = path.read_text(encoding="utf-8")
    header = strip_generated_tail(existing)
    child_rows = [
        row
        for row in section["rows"]
        if slug_from_path(row[2]) != slug or len(section["rows"]) == 1
    ]
    has_children = any(slug_from_path(row[2]) != slug for row in section["rows"])

    parts = [header, ""]
    if has_children:
        parts.extend(
            [
                "## Table of contents",
                "",
                "Mirrors the official Python 3 library index for this section. Each link opens a stub page whose H1 links to the canonical docs.",
                "",
                render_section_table(section["rows"], slug),
            ]
        )
    parts.append("")
    path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def render_root_index(sections: list[dict]) -> str:
    intro = """# [The Python Standard Library](https://docs.python.org/3/library/index.html#library-index)

While The Python Language Reference describes the exact syntax and semantics of the Python language, this library reference manual describes the standard library that is distributed with Python. It also describes some of the optional components that are commonly included in Python distributions.

Python’s standard library is very extensive, offering a wide range of facilities as indicated by the long table of contents listed below. The library contains built-in modules (written in C) that provide access to system functionality such as file I/O that would otherwise be inaccessible to Python programmers, as well as modules written in Python that provide standardized solutions for many problems that occur in everyday programming. Some of these modules are explicitly designed to encourage and enhance the portability of Python programs by abstracting away platform-specifics into platform-neutral APIs.

The Python installers for the Windows platform usually include the entire standard library and often also include many additional components. For Unix-like operating systems Python is normally provided as a collection of packages, so it may be necessary to use the packaging tools provided with the operating system to obtain some or all of the optional components.

In addition to the standard library, there is an active collection of hundreds of thousands of components (from individual programs and modules to packages and entire application development frameworks), available from the [Python Package Index](https://pypi.org/).

## Table of contents

Mirrors the [Python 3 library index](https://docs.python.org/3/library/index.html#library-index). Each section links to a category page in this repo; stub H1s link to the canonical docs.

| Section | Description |
|---------|-------------|
"""
    rows = []
    seen: set[str] = set()
    for section in sections:
        slug = section["slug"]
        if slug in seen:
            continue
        seen.add(slug)
        category = section["category"]
        rows.append(f"| [{category}]({slug}/index.md) | |")
    return intro + "\n".join(rows) + "\n"


def child_nav_title(link_text: str, rel_path: str, slug: str) -> str:
    child_slug = slug_from_path(rel_path)
    if child_slug == slug:
        return link_text
    return link_text


def yaml_quote(title: str) -> str:
    if any(ch in title for ch in ':"\'\\'):
        escaped = title.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return title


def render_nav_item(section: dict, indent: int = 2) -> list[str]:
    slug = section["slug"]
    base = " " * indent + "- "
    nav_path = f"{NAV_PREFIX}/{slug}/index.md"
    child_rows = [row for row in section["rows"] if slug_from_path(row[2]) != slug]
    if not child_rows:
        return [f"{base}{nav_path}"]

    section_title = yaml_quote(section["category"])
    child_indent = " " * (indent + 2)
    lines = [f"{base}{section_title}:", f"{child_indent}- {nav_path}"]
    for _category, link_text, rel_path, _desc in child_rows:
        child_slug = slug_from_path(rel_path)
        child_path = f"{NAV_PREFIX}/{child_slug}/index.md"
        title = yaml_quote(child_nav_title(link_text, rel_path, slug))
        lines.append(f"{child_indent}- {title}: {child_path}")
    return lines


def render_nav(sections: list[dict]) -> str:
    lines = [
        "      - The Python Standard Library:",
        f"        - {NAV_PREFIX}/index.md",
    ]
    for section in sections:
        lines.extend(render_nav_item(section, indent=8))
    return "\n".join(lines) + "\n"


def replace_mkdocs_nav(nav_block: str) -> None:
    text = MKDOCS.read_text(encoding="utf-8")
    start = text.index("      - The Python Standard Library:")
    end = text.index("      - The Python Language Reference:")
    updated = text[:start] + nav_block + text[end:]
    MKDOCS.write_text(updated, encoding="utf-8")


def load_table_rows() -> list[tuple[str, str, str, str]]:
    content = TABLE_SOURCE.read_text(encoding="utf-8")
    if "| Category | Module/Link | Description |" in content:
        table_start = content.index("| Category | Module/Link | Description |")
        return parse_table(content[table_start:])
    raise SystemExit(f"Table source missing expected header: {TABLE_SOURCE}")


OFFICIAL_LIBRARY_INDEX = "https://docs.python.org/3/library/index.html"


def _extract_ul(html: str, pos: int = 0) -> tuple[str | None, int]:
    start = html.find("<ul", pos)
    if start < 0:
        return None, pos
    depth = 0
    index = start
    while index < len(html):
        if html[index : index + 3] == "<ul":
            depth += 1
            index += 3
            continue
        if html[index : index + 5] == "</ul>":
            depth -= 1
            index += 5
            if depth == 0:
                return html[start:index], index
            continue
        index += 1
    return None, pos


def _parse_li_block(block: str) -> list[dict]:
    items: list[dict] = []
    pos = 0
    while True:
        match = re.search(r"<li[^>]*>", block[pos:])
        if not match:
            break
        li_start = pos + match.start()
        li_open_end = pos + match.end()
        depth = 0
        index = li_start
        while index < len(block):
            if block[index : index + 3] == "<li":
                depth += 1
                index += 3
                continue
            if block[index : index + 5] == "</li>":
                depth -= 1
                index += 5
                if depth == 0:
                    break
                continue
            index += 1
        li_inner = block[li_open_end : index - 5]
        pos = index
        anchor = re.search(
            r'<a class="reference internal" href="([^"]+)">(.*?)</a>',
            li_inner,
            re.DOTALL,
        )
        if not anchor:
            continue
        href = anchor.group(1)
        title = re.sub(r"<[^>]+>", "", anchor.group(2))
        title = re.sub(r"\s+", " ", title).strip()
        rest = li_inner[anchor.end() :]
        children: list[dict] = []
        while "<ul" in rest:
            ul_start = rest.index("<ul")
            sub_ul, ul_end = _extract_ul(rest, ul_start)
            if sub_ul:
                children = _parse_ul(sub_ul)
            rest = rest[ul_start + ul_end :]
        items.append({"title": title, "href": href, "children": children})
    return items


def _parse_ul(ul_html: str) -> list[dict]:
    inner = re.sub(r"^<ul[^>]*>|</ul>$", "", ul_html.strip(), flags=re.DOTALL)
    return _parse_li_block(inner)


def fetch_official_tree(url: str = OFFICIAL_LIBRARY_INDEX) -> list[dict]:
    """Return top-level library index nodes from docs.python.org."""
    html = urlopen(url, timeout=30).read().decode("utf-8", errors="replace")
    start = html.find("toctree-wrapper")
    if start < 0:
        raise RuntimeError("Could not find toctree-wrapper in official library index")
    root_ul, _ = _extract_ul(html, start)
    if not root_ul:
        raise RuntimeError("Could not parse official library toctree")
    return _parse_ul(root_ul)


def verify_against_official(
    rows: list[tuple[str, str, str, str]],
    official: list[dict],
) -> list[str]:
    """Compare local table and filesystem to the official toctree; return error lines."""
    errors: list[str] = []
    slug_by_title = {
        title: rel.removesuffix("/index.md")
        for _cat, title, rel, _desc in rows
        if title in {node["title"] for node in official}
    }
    top_dirs = {path.name for path in STD_LIB.iterdir() if path.is_dir()}

    for node in official:
        slug = slug_by_title.get(node["title"])
        if not slug:
            errors.append(f"missing table row for official section: {node['title']}")
            continue
        if slug not in top_dirs:
            errors.append(f"missing directory for {node['title']}: {slug}")
            continue
        table_child_count = sum(
            1
            for _c, _t, rel, _d in rows
            if rel.startswith(f"{slug}/") and rel != f"{slug}/index.md"
        )
        local_child_count = sum(
            1 for child in (STD_LIB / slug).iterdir() if child.is_dir()
        )
        official_child_count = len(node["children"])
        if table_child_count != official_child_count:
            errors.append(
                f"{node['title']}: table children {table_child_count} "
                f"!= official {official_child_count}"
            )
        if local_child_count != official_child_count:
            errors.append(
                f"{node['title']}: local children {local_child_count} "
                f"!= official {official_child_count}"
            )

    extra_dirs = top_dirs - set(slug_by_title.values())
    for slug in sorted(extra_dirs):
        errors.append(f"extra top-level directory not in official index: {slug}")

    table_paths = {rel for _c, _t, rel, _d in rows}
    for rel in sorted(table_paths):
        if not (STD_LIB / rel).exists():
            errors.append(f"table path missing on disk: {rel}")

    local_paths = {
        path.relative_to(STD_LIB).as_posix()
        for path in STD_LIB.rglob("index.md")
    }
    for rel in sorted(local_paths - table_paths - {"index.md"}):
        errors.append(f"disk path not listed in table: {rel}")

    return errors


def main() -> None:
    rows = load_table_rows()
    official = fetch_official_tree()
    verify_errors = verify_against_official(rows, official)
    if verify_errors:
        print("Official hierarchy verification failed:", file=sys.stderr)
        for err in verify_errors:
            print(f"  - {err}", file=sys.stderr)
        raise SystemExit(1)

    sections = group_sections(rows)

    for section in sections:
        update_section_index(section)

    (STD_LIB / "index.md").write_text(render_root_index(sections), encoding="utf-8")
    replace_mkdocs_nav(render_nav(sections))
    print(
        f"Verified against official index ({len(official)} sections). "
        f"Updated {len(sections)} section indexes and mkdocs nav."
    )


if __name__ == "__main__":
    main()
