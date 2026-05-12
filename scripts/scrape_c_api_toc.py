#!/usr/bin/env python3
"""
Scrape docs.python.org/3/c-api/index.html hierarchical ToC into JSON.

Each toctree-l1 item is one repo top-level chapter (directory). Nested
toctree-l2 links are subsection pages; href may be another *.html or a
fragment on any file.

Usage:
  python3 scripts/scrape_c_api_toc.py [--json path]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request

INDEX = "https://docs.python.org/3/c-api/index.html"
BASE = "https://docs.python.org/3/c-api/"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "python-programming-guide-scraper/1"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8")


def slugify(title: str) -> str:
    t = title.replace("&mdash;", "-").replace("—", "-")
    t = re.sub(r"<[^>]+>", "", t)
    t = t.lower()
    t = re.sub(r"[.,;:!?()'\"«»`/]", "", t)
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    t = re.sub(r"\s+", "-", t.strip())
    t = re.sub(r"-+", "-", t)
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
        inner = re.sub(r"<[^>]+>", "", m.group(3))
        inner = re.sub(r"\s+", " ", inner).strip().replace("\xa0", " ")
        if href.startswith("../"):
            continue

        if level == 1:
            if current:
                chapters.append(current)
            current = {
                "chapter_title": inner,
                "chapter_slug": slugify(inner),
                "chapter_page": href.split("#")[0],
                "chapter_url": absolutize(href),
                "subsections": [],
            }
        elif level == 2 and current is not None:
            slug = href.split("#", 1)[1] if "#" in href else slugify(inner)
            current["subsections"].append(
                {"title": inner, "slug": slug, "canonical": absolutize(href)}
            )

    if current:
        chapters.append(current)
    return chapters


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", metavar="PATH", help="Write full tree JSON.")
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
