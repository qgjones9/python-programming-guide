#!/usr/bin/env python3
"""
Scrape extending/index.html — two Sphinx toctree blocks plus synthetic chapters
for on-page sections (recommended / creating-* / embedding runtime intro).

Produces JSON consumed by enrich_extending_markdown.py.

Usage::
  python3 scripts/scrape_extending_toc.py --json \\
    docs/3.14.5/extending-and-embedding-python-interpreter/_extending_toc.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request

INDEX = "https://docs.python.org/3/extending/index.html"
BASE = "https://docs.python.org/3/extending/"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "python-programming-guide-scraper/1"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8")


def strip_section_numbers(title: str) -> str:
    return re.sub(r"^\s*\d+(?:\.\d+)*\.\s*", "", title).strip()


def slugify(title: str) -> str:
    t = title.replace("&mdash;", "-").replace("—", "-").replace("&rsquo;", "'")
    t = re.sub(r"<[^>]+>", "", t)
    t = t.lower()
    t = re.sub(r"[.,;:!?'\"«»`]", "", t)
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


def parse_toc_fragment(block: str) -> list[dict]:
    link_re = re.compile(
        r'<li class="toctree-l([12])">'
        r'.*?<a class="reference internal" href="([^"]+)">(.*?)</a>',
        re.DOTALL,
    )

    chapters: list[dict] = []
    current: dict | None = None

    for m in link_re.finditer(block):
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
            slug = (
                href.split("#", 1)[1]
                if "#" in href
                else slugify(strip_section_numbers(inner))
            )
            current["subsections"].append(
                {
                    "title": inner,
                    "slug": slug,
                    "canonical": absolutize(href),
                }
            )

    if current:
        chapters.append(current)

    for ch in chapters:
        seen: set[str] = set()
        for s in ch["subsections"]:
            if s["slug"] in seen:
                raise RuntimeError(f"duplicate subsection slug {s['slug']!r}")
            seen.add(s["slug"])
    return chapters


def extract_toctree_segments(html: str) -> tuple[str, str]:
    splits = html.split('<div class="toctree-wrapper compound">')
    if len(splits) < 3:
        raise RuntimeError("expected ≥2 extending toctree wrappers")
    segments: list[str] = []
    for chunk in splits[1:3]:
        end = chunk.find("</div>\n</section>")
        if end < 0:
            end = chunk.find("</div>")
        segments.append(chunk[:end])
    return segments[0], segments[1]


def parse(html: str) -> list[dict]:
    w1, w2 = extract_toctree_segments(html)
    extension_chapters = parse_toc_fragment(w1)
    embedding_group = parse_toc_fragment(w2)

    out: list[dict] = [
        {
            "chapter_title": "Recommended third party tools",
            "chapter_slug": "recommended-third-party-tools",
            "chapter_page": "index.html",
            "chapter_url": absolutize("index.html#recommended-third-party-tools"),
            "subsections": [],
        },
        {
            "chapter_title": "Creating extensions without third party tools",
            "chapter_slug": "creating-extensions-without-third-party-tools",
            "chapter_page": "index.html",
            "chapter_url": absolutize("index.html#creating-extensions-without-third-party-tools"),
            "subsections": [],
        },
    ]
    out.extend(extension_chapters)
    out.append(
        {
            "chapter_title": "Embedding the CPython runtime in a larger application",
            "chapter_slug": "embedding-the-cpython-runtime-in-a-larger-application",
            "chapter_page": "index.html",
            "chapter_url": absolutize(
                "index.html#embedding-the-cpython-runtime-in-a-larger-application"
            ),
            "subsections": [],
        }
    )
    out.extend(embedding_group)

    slugs = [c["chapter_slug"] for c in out]
    if len(slugs) != len(set(slugs)):
        raise RuntimeError(f"duplicate chapter slugs: {slugs}")

    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args()

    chapters = parse(fetch(INDEX))
    text = json.dumps(chapters, indent=2) + "\n"

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
