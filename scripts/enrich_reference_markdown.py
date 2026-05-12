#!/usr/bin/env python3
"""
Scaffold + enrich docs/3.14.5/language-reference from _reference_toc.json.

Uses runnable ```python fenced examples (# comments). Regenerates root index TOC.

Prerequisite::

    python3 scripts/scrape_reference_toc.py --json docs/3.14.5/language-reference/_reference_toc.json

Usage::

    python3 scripts/enrich_reference_markdown.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

MANUAL_ROOT = Path(__file__).resolve().parent.parent / "docs" / "3.14.5" / "language-reference"
REF_BOOK = "https://docs.python.org/3/reference/index.html"

PY_SNIPPETS = [
    """```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```""",
    """```python
# Names bind to objects; multiple names may reference the same value (aliases).
nums = []
alias = nums
alias.append(1)
assert nums == [1]
```""",
    """```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```""",
    """```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```""",
    """```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```""",
    """```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```""",
    """```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```""",
    """```python
# Statements execute for effect; expressions inside them still follow semantics.
seen = []

def record():
    seen.append(True)
    return "done"


record()
assert seen == [True]
```""",
]


def pick_snippet(key: str) -> str:
    h = sum(ord(c) for c in key)
    return PY_SNIPPETS[h % len(PY_SNIPPETS)]


def esc_md(s: str) -> str:
    return s.replace("\n", " ").strip()


def render_chapter_parent(ch: dict) -> str:
    title = ch["chapter_title"]
    url = ch["chapter_url"]
    lines: list[str] = [
        f"# [{title}]({url})",
        "",
        f"Local notes for [**{title}**]({url}) in "
        f"*[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. "
        "This mirror is shorthand; wording and grammar are authoritative only on docs.python.org.",
        "",
    ]
    for sub in ch["subsections"]:
        can = sub["canonical"]
        st = sub["title"]
        lines.append(f"### [{st}]({can})")
        lines.append("")
        lines.append(f"- Canonical: **[{esc_md(st)}]({can})** — definitions, judgments, and edge cases.")
        lines.append("- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.")
        lines.append("- Prefer the linked anchors when bisecting language changes across minor versions.")
        lines.append("")
        lines.append(pick_snippet(ch["chapter_slug"] + "/" + sub["slug"]))
        lines.append("")

    lines.append("## Sections in this repo")
    lines.append("")
    for s in ch["subsections"]:
        lines.append(f"- [{s['title']}]({s['slug']}/index.md)")
    lines.append("")
    return "\n".join(lines)


def render_chapter_standalone(ch: dict) -> str:
    title = ch["chapter_title"]
    url = ch["chapter_url"]
    return "\n".join(
        [
            f"# [{title}]({url})",
            "",
            f"No sub-pages in this mirror; read [**{title}**]({url}) on docs.python.org for the full grammar and commentary.",
            "",
            f"- Canonical: [{esc_md(title)}]({url})",
            "- Cross-check wording with PEPs cited from that page when behavior evolved across releases.",
            "- Standard library objects are specified in *[The Python Standard Library](https://docs.python.org/3/library/index.html)*, not necessarily here.",
            "",
            pick_snippet(ch["chapter_slug"]),
            "",
        ]
    )


def render_leaf(ch: dict, sub: dict) -> str:
    can = sub["canonical"]
    st = sub["title"]
    ch_title = ch["chapter_title"]
    ch_entry = f"https://docs.python.org/3/reference/{ch['chapter_page']}"
    return "\n".join(
        [
            f"# [{st}]({can})",
            "",
            f"Scratch notes on **{esc_md(st)}** within "
            f"[*{esc_md(ch_title)}*]({ch_entry}); language lawyers should keep the **[official §]({can})** open.",
            "",
            f"- Normative wording lives at **[docs.python.org]({can})** — especially footnotes about implementation.",
            "- The reference is terse; *[The Tutorial](https://docs.python.org/3/tutorial/index.html)* motivates many of the same constructs.",
            "- When behavior touches imports, loaders, or `__main__`, also skim *The import system* chapter as needed.",
            "",
            pick_snippet(sub["slug"]),
            "",
            f"Parent: [{ch_title}](../index.md)",
            "",
        ]
    )


def render_root_index(chapters: list[dict]) -> str:
    lines = [
        "# [The Python Language Reference](https://docs.python.org/3/reference/index.html#reference-index)",
        "",
        "Structured mirror of "
        "**[The Python Language Reference]"
        "(https://docs.python.org/3/reference/index.html#reference-index)** "
        "(syntax and core semantics). Subpages anchor to Sphinx fragments enumerated in **`_reference_toc.json`**.",
        "",
        "- Informal onboarding: *[The Tutorial](https://docs.python.org/3/tutorial/index.html)*.",
        "- Built-ins and modules: *[The Python Standard Library](https://docs.python.org/3/library/index.html)*.",
        "- C embedding: *[Python/C API](https://docs.python.org/3/c-api/index.html)* and *[Extending and Embedding]"
        "(https://docs.python.org/3/extending/index.html)*.",
        "",
        "## Table of Contents",
        "",
        "Mirrors the [reference manual index]"
        "(https://docs.python.org/3/reference/index.html#reference-index). "
        "Each heading links into this repo (`…/index.md`); stub H1s link to **`reference/*.html#…`**.",
        "",
    ]
    for ch in chapters:
        slug = ch["chapter_slug"]
        lines.append(f"## [{ch['chapter_title']}]({slug}/index.md)")
        lines.append("")
        for s in ch["subsections"]:
            lines.append(f"### [{s['title']}]({slug}/{s['slug']}/index.md)")
            lines.append("")
    return "\n".join(lines)


def validate_python_snippets_under(root: Path) -> None:
    failing: list[tuple[Path, int, BaseException]] = []
    for md in sorted(root.rglob("index.md")):
        text = md.read_text(encoding="utf-8")
        blocks = re.findall(r"```python\n(.*?)```", text, re.DOTALL)
        for i, code in enumerate(blocks):
            try:
                compile(code, str(md), "exec")
                ns: dict[str, object] = {}
                exec(code, ns, ns)  # one mapping so nested defs see module-level names
            except Exception as exc:  # noqa: BLE001
                failing.append((md, i, exc))
    if failing:
        for path, idx, exc in failing:
            print("FAIL", path, "block", idx, exc)
        raise SystemExit(1)


def main() -> None:
    toc_path = MANUAL_ROOT / "_reference_toc.json"
    if not toc_path.exists():
        raise SystemExit(f"Missing {toc_path}")

    chapters: list[dict] = json.loads(toc_path.read_text(encoding="utf-8"))
    MANUAL_ROOT.mkdir(parents=True, exist_ok=True)

    for ch in chapters:
        cdir = MANUAL_ROOT / ch["chapter_slug"]
        cdir.mkdir(parents=True, exist_ok=True)

        if ch["subsections"]:
            for sub in ch["subsections"]:
                (cdir / sub["slug"]).mkdir(parents=True, exist_ok=True)
            (cdir / "index.md").write_text(render_chapter_parent(ch), encoding="utf-8")
            for sub in ch["subsections"]:
                lp = cdir / sub["slug"] / "index.md"
                lp.write_text(render_leaf(ch, sub), encoding="utf-8")
        else:
            (cdir / "index.md").write_text(render_chapter_standalone(ch), encoding="utf-8")

    (MANUAL_ROOT / "index.md").write_text(render_root_index(chapters), encoding="utf-8")
    validate_python_snippets_under(MANUAL_ROOT)


if __name__ == "__main__":
    main()
