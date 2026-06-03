#!/usr/bin/env python3
"""Generate per-term glossary pages from docs.python.org 3.14 glossary HTML."""

from __future__ import annotations

import html
import re
import sys
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY_DIR = ROOT / "docs" / "versions" / "3.14.5" / "glossary"
INDEX_PATH = GLOSSARY_DIR / "index.md"
MKDOCS_PATH = ROOT / "mkdocs.yml"
GLOSSARY_URL = "https://docs.python.org/3.14/glossary.html"
DOCS_BASE = "https://docs.python.org/3.14/"


def fetch_glossary_html() -> str:
    local = Path("/tmp/glossary.html")
    if local.is_file() and local.stat().st_size > 100_000:
        return local.read_text(encoding="utf-8")
    with urllib.request.urlopen(GLOSSARY_URL) as resp:
        data = resp.read().decode("utf-8")
    local.write_text(data, encoding="utf-8")
    return data


def slug_dir(slug: str) -> str:
    return slug


def parse_terms(soup: BeautifulSoup) -> list[dict]:
    dl = soup.find("dl", class_="glossary")
    if dl is None:
        raise RuntimeError("glossary dl not found")

    terms: list[dict] = []
    pending_dts: list[tuple[str, str]] = []

    for child in dl.children:
        if not isinstance(child, Tag):
            continue
        if child.name == "dt":
            term_id = child.get("id", "")
            if not term_id.startswith("term-"):
                continue
            slug = term_id[5:]
            title = child.get_text(strip=True).replace("¶", "").strip()
            pending_dts.append((slug, title))
        elif child.name == "dd" and pending_dts:
            for slug, title in pending_dts:
                terms.append(
                    {
                        "slug": slug,
                        "title": title,
                        "dd": child,
                    }
                )
            pending_dts = []

    return terms


def resolve_href(href: str, glossary_slugs: set[str]) -> str:
    if not href:
        return href
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("#term-"):
        slug = href[6:]
        if slug in glossary_slugs:
            return f"../{slug_dir(slug)}/index.md"
        return f"{GLOSSARY_URL}{href}"
    if href.startswith("#"):
        return f"{GLOSSARY_URL}{href}"
    return DOCS_BASE + href.lstrip("./")


def link_text(node: Tag) -> str:
    return html.unescape("".join(node.stripped_strings))


def format_link(node: Tag, glossary_slugs: set[str]) -> str:
    href = resolve_href(node.get("href", ""), glossary_slugs)
    text = link_text(node)
    if not text:
        text = href
    return f"[{text}]({href})"


def inline_text(node: Tag | NavigableString, in_link: bool = False) -> str:
    if isinstance(node, NavigableString):
        return html.unescape(str(node))

    if not isinstance(node, Tag):
        return ""

    if node.name == "a":
        raise ValueError("links must use format_link()")

    if node.name in ("code",):
        inner = "".join(inline_text(c, in_link=True) for c in node.children)
        if in_link:
            return inner
        return f"`{inner}`"

    if node.name == "span":
        return "".join(inline_text(c, in_link=in_link) for c in node.children)

    if node.name in ("strong", "b"):
        inner = "".join(inline_text(c, in_link=in_link) for c in node.children)
        return f"**{inner}**"

    if node.name in ("em", "i") or "dfn" in node.get("class", []):
        inner = "".join(inline_text(c, in_link=in_link) for c in node.children)
        return f"*{inner}*"

    return "".join(inline_text(c, in_link=in_link) for c in node.children)


def paragraph_to_md(node: Tag, glossary_slugs: set[str]) -> str:
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, Tag) and child.name == "a":
            parts.append(format_link(child, glossary_slugs))
        else:
            parts.append(inline_text(child))
    text = "".join(parts).strip()
    return text + "\n\n" if text else ""


def extract_code_block(pre: Tag) -> str:
    code = html.unescape(pre.get_text()).rstrip()
    return f"```python\n{code}\n```"


def has_highlight_class(tag: Tag) -> bool:
    return any("highlight" in cls for cls in tag.get("class", []))


def li_to_md(li: Tag, glossary_slugs: set[str]) -> str:
    parts: list[str] = []
    for child in li.children:
        if isinstance(child, NavigableString):
            text = html.unescape(str(child)).strip()
            if text:
                parts.append(text)
            continue
        if not isinstance(child, Tag):
            continue
        if child.name == "ul":
            parts.append("\n\n" + list_to_md(child, glossary_slugs, indent=2))
            continue
        if child.name == "p":
            parts.append(paragraph_to_md(child, glossary_slugs).strip())
        elif child.name == "a":
            parts.append(format_link(child, glossary_slugs))
        elif has_highlight_class(child) or child.find(class_=lambda c: c and any("highlight" in x for x in c)):
            pre = child.find("pre")
            if pre:
                parts.append("\n\n" + extract_code_block(pre) + "\n")
        elif child.name == "pre":
            parts.append("\n\n" + extract_code_block(child) + "\n")
        else:
            parts.append(inline_text(child))
    return "".join(parts).strip()


def list_to_md(node: Tag, glossary_slugs: set[str], indent: int = 0) -> str:
    pad = " " * indent
    lines: list[str] = []
    for li in node.find_all("li", recursive=False):
        body = li_to_md(li, glossary_slugs)
        if "```python" in body:
            intro, code = body.split("```python", 1)
            intro = intro.strip()
            code = "```python" + code
            lines.append(f"{pad}- {intro}")
            lines.append("")
            lines.extend(code.splitlines())
            lines.append("")
        elif "\n\n" in body:
            intro, rest = body.split("\n\n", 1)
            lines.append(f"{pad}- {intro.strip()}")
            lines.append("")
            lines.extend(rest.splitlines())
            lines.append("")
        else:
            lines.append(f"{pad}- {body}")
    return "\n".join(lines).rstrip() + "\n\n"


def block_to_md(node: Tag | NavigableString, glossary_slugs: set[str]) -> str:
    if isinstance(node, NavigableString):
        text = html.unescape(str(node)).strip()
        return text

    if not isinstance(node, Tag):
        return ""

    if node.name == "p":
        return paragraph_to_md(node, glossary_slugs)

    if node.name == "ul":
        return list_to_md(node, glossary_slugs)

    if node.name == "div" and has_highlight_class(node):
        pre = node.find("pre")
        if pre:
            return extract_code_block(pre) + "\n\n"
        return ""

    if node.name == "pre":
        return extract_code_block(node) + "\n\n"

    return "".join(block_to_md(c, glossary_slugs) for c in node.children)


def dd_to_md(dd: Tag, glossary_slugs: set[str]) -> str:
    parts = [block_to_md(child, glossary_slugs) for child in dd.children]
    md = "".join(parts)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def parse_index_terms() -> list[tuple[str, str]]:
    text = INDEX_PATH.read_text(encoding="utf-8")
    entries: list[tuple[str, str]] = []
    for line in text.splitlines():
        m = re.match(
            r"^- \[(.+?)\]\(\./(.+?)/index\.md\)$",
            line.strip(),
        )
        if m:
            entries.append((m.group(1), m.group(2)))
            continue
        m = re.match(
            r"^- \[(.+?)\]\(https://docs\.python\.org/3\.14/glossary\.html#term-(.+?)\)$",
            line.strip(),
        )
        if m:
            entries.append((m.group(1), m.group(2)))
    return entries


def write_term_page(term: dict, glossary_slugs: set[str]) -> None:
    slug = term["slug"]
    title = term["title"]
    body = dd_to_md(term["dd"], glossary_slugs)
    official = f"{GLOSSARY_URL}#term-{slug}"
    page_dir = GLOSSARY_DIR / slug_dir(slug)
    page_dir.mkdir(parents=True, exist_ok=True)
    content = f"# [{title}]({official})\n\n{body}"
    (page_dir / "index.md").write_text(content, encoding="utf-8")


def update_index(entries: list[tuple[str, str]]) -> None:
    lines = [
        "# [Glossary](https://docs.python.org/3.14/glossary.html)",
        "",
        "Definitions of terms used throughout the Python documentation.",
        "",
    ]
    for title, slug in entries:
        lines.append(f"- [{title}](./{slug_dir(slug)}/index.md)")
    lines.append("")
    INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")


def safe_nav_title(title: str) -> str:
    if title == "..." or title.startswith(">") or ":" in title:
        return f'"{title}"'
    return title


def update_mkdocs_nav(entries: list[tuple[str, str]]) -> None:
    text = MKDOCS_PATH.read_text(encoding="utf-8")
    nav_lines = ["      - Glossary:", "          - versions/3.14.5/glossary/index.md"]
    for title, slug in entries:
        safe = safe_nav_title(title)
        nav_lines.append(
            f"          - {safe}: versions/3.14.5/glossary/{slug_dir(slug)}/index.md"
        )
    new_block = "\n".join(nav_lines)
    patterns = [
        r"      - Glossary:\n(?:          - .+\n)+",
        r"      - Glossary: versions/3\.14\.5/glossary/index\.md\n",
    ]
    for pattern in patterns:
        if re.search(pattern, text):
            text = re.sub(pattern, new_block + "\n", text, count=1)
            MKDOCS_PATH.write_text(text, encoding="utf-8")
            return
    raise RuntimeError("Glossary nav entry not found in mkdocs.yml")


def main() -> int:
    html_text = fetch_glossary_html()
    soup = BeautifulSoup(html_text, "html.parser")
    terms = parse_terms(soup)
    term_by_slug = {t["slug"]: t for t in terms}
    glossary_slugs = set(term_by_slug)

    index_entries = parse_index_terms()
    if not index_entries:
        print("No index entries found", file=sys.stderr)
        return 1

    failed: list[str] = []
    created = 0
    for title, slug in index_entries:
        term = term_by_slug.get(slug)
        if term is None:
            failed.append(slug)
            continue
        write_term_page(term, glossary_slugs)
        created += 1

    update_index(index_entries)
    update_mkdocs_nav(index_entries)

    print(f"Created {created} glossary term pages")
    print(f"Failed ({len(failed)}): {', '.join(failed) if failed else 'none'}")
    sample = GLOSSARY_DIR / "abstract-base-class" / "index.md"
    print(f"Sample: {sample.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
