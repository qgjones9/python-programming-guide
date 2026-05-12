#!/usr/bin/env python3
"""
Scrape docs.python.org/3/reference/index.html into a chapter tree JSON.

Same toctree-l1 / toctree-l2 pattern as the C API scraper. Chapter slugs omit
leading section numbers for stable directory names.

Usage:
  python3 scripts/scrape_reference_toc.py --json docs/3.14.5/language-reference/_reference_toc.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request

INDEX = "https://docs.python.org/3/reference/index.html"
BASE = "https://docs.python.org/3/reference/"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "python-programming-guide-scraper/1"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8")


def strip_section_numbers(title: str) -> str:
    return re.sub(r"^\s*\d+(?:\.\d+)*\.\s*", "", title).strip()


def slugify(title: str) -> str:
    t = title.replace("&mdash;", "-").replace("—", "-")
    t = re.sub(r"<[^>]+>", "", t)
    t = t.lower()
    t = re.sub(r"[.,;:!?'\"«»`]", "", t)
    # keep () for nothing - remove parens content? e.g. identifiers - keep hyphen
    t = re.sub(r"[\(\)]", " ", t)
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    t = re.sub(r"\s+", "-", t.strip())
    t = re.sub(r"-+", "-", t)
    return t


def clean_anchor_text(html: str) -> str:
    t = re.sub(r"<[^>]+>", "", html)
    t = re.sub(r"\s+", " ", t).strip().replace("\xa0", " ")
    return t


def absolutize(href: str) -> str:
    href = href.strip()
    if href.startswith(("http://", "https://")):
        return href
    return BASE + href


def parse(html: str) -> list[dict]:
    pos = html.find('<div class="toctree-wrapper compound">')
    if pos < 0:
        raise RuntimeError("toctree-wrapper not found")
    subset = html[pos:]
    end = subset.find("</section>")
    if end > 0:
        subset = subset[:end]

    link_re = re.compile(
        r'<li class="toctree-l([12])">'
        r'.*?<a class="reference internal" href="([^"]+)">(.*?)</a>',
        re.DOTALL,
    )

    chapters: list[dict] = []
    current: dict | None = None

    for m in link_re.finditer(subset):
        level = int(m.group(1))
        href = m.group(2).strip()
        inner = clean_anchor_text(m.group(3))
        if href.startswith("../"):
            continue

        if level == 1:
            if current:
                chapters.append(current)
            page = href.split("#")[0]
            current = {
                "chapter_title": inner,
                "chapter_slug": slugify(strip_section_numbers(inner)),
                "chapter_page": page,
                "chapter_url": absolutize(href.split("#")[0]),
                "subsections": [],
            }
        elif level == 2 and current is not None:
            slug = href.split("#", 1)[1] if "#" in href else slugify(strip_section_numbers(inner))
            current["subsections"].append(
                {
                    "title": inner,
                    "slug": slug,
                    "canonical": absolutize(href),
                }
            )

    if current:
        chapters.append(current)

    # Sanity: unique slugs per chapter
    for ch in chapters:
        seen: set[str] = set()
        for s in ch["subsections"]:
            if s["slug"] in seen:
                raise RuntimeError(f"duplicate subsection slug {s['slug']!r} in {ch['chapter_slug']}")
            seen.add(s["slug"])

    return chapters


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args()

    html = fetch(INDEX)
    chapters = parse(html)
    text = json.dumps(chapters, indent=2) + "\n"
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
