#!/usr/bin/env python3
"""Generate MkDocs nav YAML from the docs/ directory tree."""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
SKIP_DIRS = {"stylesheets", "__pycache__"}

# Match docs/versions/3.14.5/index.md "Documentation books" table order.
PYTHON_314_5_BOOK_ORDER = (
    "tutorial",
    "standard-library",
    "language-reference",
    "extending-and-embedding-python-interpreter",
    "python-c-api-reference-manual",
)


def sort_child_dirs(parent: Path, child_dirs: list[Path]) -> list[Path]:
    rel = parent.relative_to(DOCS_DIR).as_posix()
    if rel == "versions/3.14.5":
        order = {name: index for index, name in enumerate(PYTHON_314_5_BOOK_ORDER)}
        return sorted(
            child_dirs,
            key=lambda path: (order.get(path.name, len(order)), path.name),
        )
    return sorted(child_dirs, key=lambda path: path.name)


def title_from_index(index_path: Path) -> str:
    text = index_path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("#"):
            continue
        title = line.lstrip("#").strip()
        link_match = re.match(r"\[(.+?)\]\(.+?\)", title)
        if link_match:
            return link_match.group(1)
        return title
    return index_path.parent.name.replace("-", " ").title()


def build_nav(directory: Path, docs_root: Path) -> list | dict | None:
    index_path = directory / "index.md"
    if not index_path.is_file():
        return None

    rel = directory.relative_to(docs_root).as_posix()
    nav_path = f"{rel}/index.md" if rel != "." else "index.md"
    title = title_from_index(index_path)

    child_dirs = sort_child_dirs(
        directory,
        [
            p
            for p in directory.iterdir()
            if p.is_dir() and p.name not in SKIP_DIRS and not p.name.startswith(".")
        ],
    )

    children: list = []
    for child_dir in child_dirs:
        child_nav = build_nav(child_dir, docs_root)
        if child_nav is not None:
            children.append(child_nav)

    if not children:
        return {title: nav_path}

    section: list = [{title: nav_path}]
    section.extend(children)
    return {title: section}


def _yaml_safe_title(title: str) -> str:
    if ":" in title:
        return f'"{title}"'
    if title and title[0] in ">!@&*?|-":
        return f'"{title}"'
    return title


def nav_to_yaml(nav_item, indent: int = 1) -> str:
    pad = "  " * indent
    if isinstance(nav_item, dict):
        lines: list[str] = []
        for title, value in nav_item.items():
            safe_title = _yaml_safe_title(title)
            if isinstance(value, str):
                lines.append(f"{pad}- {safe_title}: {value}")
            elif isinstance(value, list):
                lines.append(f"{pad}- {safe_title}:")
                for child in value:
                    lines.append(nav_to_yaml(child, indent + 1))
            else:
                raise TypeError(f"Unexpected nav value type: {type(value)!r}")
        return "\n".join(lines)
    raise TypeError(f"Unexpected nav item type: {type(nav_item)!r}")


def main() -> int:
    docs_root = DOCS_DIR
    top_level: list = [{"Home": "index.md"}]

    for child_dir in sorted(docs_root.iterdir()):
        if not child_dir.is_dir() or child_dir.name in SKIP_DIRS:
            continue
        child_nav = build_nav(child_dir, docs_root)
        if child_nav is not None:
            top_level.append(child_nav)

    print("nav:")
    for item in top_level:
        print(nav_to_yaml(item, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
