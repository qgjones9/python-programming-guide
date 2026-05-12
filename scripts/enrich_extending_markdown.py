#!/usr/bin/env python3
"""
Scaffold + enrich docs/3.14.5/extending-and-embedding-python-interpreter/**/index.md.

Uses illustrative ```c snippets (no mandatory compile). Mirrors *Extending and Embedding*.

Prerequisite::

    python3 scripts/scrape_extending_toc.py --json \\
      docs/3.14.5/extending-and-embedding-python-interpreter/_extending_toc.json

Usage::

    python3 scripts/enrich_extending_markdown.py
"""

from __future__ import annotations

import json
from pathlib import Path

MANUAL_ROOT = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "3.14.5"
    / "extending-and-embedding-python-interpreter"
)

EXT_BASE = "https://docs.python.org/3/extending/"

C_API_FROM_CHAPTER_PARENT = "../python-c-api-reference-manual/index.md"
C_API_FROM_SUBPAGE = "../../python-c-api-reference-manual/index.md"

C_SNIPPETS = [
    """```c
#include <Python.h>

/* Minimal PyInit prototype; publish methods via PyMethodDef/PyModuleDef (see guide). */
static PyMethodDef _methods[] = {
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef _mod = {
    PyModuleDef_HEAD_INIT, "demo", NULL, -1, _methods,
};

PyMODINIT_FUNC
PyInit_demo(void)
{
    return PyModule_Create(&_mod);
}
```""",
    """```c
#include <Python.h>

/* Hold the GIL around almost every C-API entry point unless docs say otherwise. */
PyGILState_STATE _gstate = PyGILState_Ensure();
/* … Py_DECREF / constructors … */
PyGILState_Release(_gstate);
```""",
    """```c
#include <Python.h>

/* Returned PyObject pointers are usually new refs—pair Py_DECREF once done. */
PyObject *tmp = PyLong_FromLong(7);
if (tmp == NULL) {
    return NULL;
}
Py_DECREF(tmp);
```""",
]


def pick_snippet(key: str) -> str:
    h = sum(ord(c) for c in key)
    return C_SNIPPETS[h % len(C_SNIPPETS)]


def esc_md(s: str) -> str:
    return s.replace("\n", " ").strip()


def annotate_sibling_hints(chapters: list[dict]) -> None:
    for i, ch in enumerate(chapters):
        slug = ch["chapter_slug"]

        if slug == "creating-extensions-without-third-party-tools":
            sibs: list[dict] = []
            j = i + 1
            while (
                j < len(chapters)
                and chapters[j]["chapter_slug"]
                != "embedding-the-cpython-runtime-in-a-larger-application"
            ):
                sibs.append(chapters[j])
                j += 1
            ch["_extension_branch"] = sibs

        elif slug == "embedding-the-cpython-runtime-in-a-larger-application":
            if i + 1 < len(chapters):
                ch["_embedding_chapter"] = chapters[i + 1]


def render_standalone_intro(ch: dict, kind: str) -> str:
    title = ch["chapter_title"]
    url = ch["chapter_url"]

    extras: list[str] = []

    if kind == "recommended":
        extras.extend(
            [
                "- Prefer maintained bindgens (PyO3/pybind11/Cython, etc.) linked from the upstream guide before handwriting everything in raw C.",
                "- Dive into *[Python/C API](https://docs.python.org/3/c-api/index.html)* when you bypass higher-level scaffolding.",
                "",
                "## See also",
                "",
                "- [Creating extensions without third party tools](creating-extensions-without-third-party-tools/index.md)",
                "",
            ]
        )

    elif kind == "creating":
        sibs = ch.get("_extension_branch") or []
        extras.append("- This heading is prose on `extending/index.html`; the procedural chapters collected below form the toolchain chapter list.")
        extras.append("")
        extras.append("- **See also**: [PEP 489 – Multi-phase extension module initialization](https://peps.python.org/pep-0489/).")
        extras.append("")
        extras.append("## Chapters under this banner")
        extras.append("")
        for s in sibs:
            extras.append(f"- [{s['chapter_title']}]({s['chapter_slug']}/index.md)")
        extras.append("")

    elif kind == "embedding-intro":
        nxt = ch.get("_embedding_chapter")
        extras.append("- Embedding calls `Py_Initialize` / teardown sequences; pitfalls differ from extension modules shipped as `.so`/`.pyd`.")
        extras.append("")
        if nxt:
            extras.append(f"- Follow **[{esc_md(nxt['chapter_title'])}]({nxt['chapter_slug']}/index.md)** for the runnable walkthrough.")
        extras.append("")

    core = [
        f"# [{title}]({url})",
        "",
        f"Section from **[Extending & Embedding — {esc_md(title)}]({url})** (book index page). Narrative prose stays on docs.python.org.",
        "",
        f"- Canonical: [{esc_md(title)}]({url})",
        *extras,
        pick_snippet(ch["chapter_slug"]),
        "",
    ]
    return "\n".join(core)


def render_chapter_parent(ch: dict) -> str:
    title = ch["chapter_title"]
    url = ch["chapter_url"]
    lines: list[str] = [
        f"# [{title}]({url})",
        "",
        f"Scratch notes backing [**{title}**]({url}) inside "
        f"*[Extending and Embedding](https://docs.python.org/3/extending/index.html#extending-index)*.",
        "",
    ]
    for sub in ch["subsections"]:
        lines.append(f"### [{sub['title']}]({sub['canonical']})")
        lines.append("")
        lines.append(f"- Full write-up: [{esc_md(sub['title'])}]({sub['canonical']}).")
        lines.append(
            f"- Cross-check refcount / error conventions with the "
            f"*[Python/C API Reference]({C_API_FROM_CHAPTER_PARENT})* mirror when coding against `Python.h`."
        )
        lines.append("")
        lines.append(pick_snippet(ch["chapter_slug"] + "/" + sub["slug"]))
        lines.append("")

    lines.append("## Sections in this repo")
    lines.append("")
    for s in ch["subsections"]:
        lines.append(f"- [{s['title']}]({s['slug']}/index.md)")
    lines.append("")
    return "\n".join(lines)


def render_standalone_fallback(ch: dict) -> str:
    title = ch["chapter_title"]
    url = ch["chapter_url"]
    return "\n".join(
        [
            f"# [{title}]({url})",
            "",
            f"Single-section chapter **[{title}]({url})** in *Extending and Embedding*.",
            "",
            "- Use the canonical page for setuptools / compiler flags / platform quirks.",
            "",
            pick_snippet(ch["chapter_slug"]),
            "",
        ]
    )


def render_leaf(ch: dict, sub: dict) -> str:
    ch_entry = EXT_BASE + ch["chapter_page"]
    return "\n".join(
        [
            f"# [{sub['title']}]({sub['canonical']})",
            "",
            f"Local notes on **{esc_md(sub['title'])}** within [*{esc_md(ch['chapter_title'])}*]({ch_entry}).",
            "",
            f"- Detailed rules: **[{esc_md(sub['title'])}]({sub['canonical']})**.",
            f"- Companion reference: *[Python/C API Reference]({C_API_FROM_SUBPAGE})* for every `Py*` symbol you call.",
            "",
            pick_snippet(sub["slug"]),
            "",
            f"Parent: [{ch['chapter_title']}](../index.md)",
            "",
        ]
    )


def render_root_index(chapters: list[dict]) -> str:
    lines = [
        "# [Extending and Embedding the Python Interpreter](https://docs.python.org/3/extending/index.html#extending-index)",
        "",
        "Structured mirror of "
        "**[Extending and Embedding the Python Interpreter]"
        "(https://docs.python.org/3/extending/index.html#extending-index)**. "
        "`_extending_toc.json` records every Sphinx TOC link (two compound toctrees "
        "+ on-page introductions). Companion: "
        "**[Python/C API Reference]"
        "(../python-c-api-reference-manual/index.md)**.",
        "",
        "## Table of Contents",
        "",
        "Anchors mirror [the official TOC](https://docs.python.org/3/extending/index.html#extending-index). Internal paths end with `index.md`.",
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


def main() -> None:
    toc = MANUAL_ROOT / "_extending_toc.json"
    if not toc.exists():
        raise SystemExit(f"Missing {toc}")

    chapters: list[dict] = json.loads(toc.read_text(encoding="utf-8"))
    annotate_sibling_hints(chapters)
    MANUAL_ROOT.mkdir(parents=True, exist_ok=True)

    for ch in chapters:
        slug = ch["chapter_slug"]
        cdir = MANUAL_ROOT / slug
        cdir.mkdir(parents=True, exist_ok=True)

        if ch["subsections"]:
            body = render_chapter_parent(ch)
            for sub in ch["subsections"]:
                leaf = cdir / sub["slug"]
                leaf.mkdir(parents=True, exist_ok=True)
                (leaf / "index.md").write_text(render_leaf(ch, sub), encoding="utf-8")
        else:
            if slug == "recommended-third-party-tools":
                body = render_standalone_intro(ch, "recommended")
            elif slug == "creating-extensions-without-third-party-tools":
                body = render_standalone_intro(ch, "creating")
            elif slug == "embedding-the-cpython-runtime-in-a-larger-application":
                body = render_standalone_intro(ch, "embedding-intro")
            else:
                body = render_standalone_fallback(ch)

        (cdir / "index.md").write_text(body, encoding="utf-8")

    (MANUAL_ROOT / "index.md").write_text(render_root_index(chapters), encoding="utf-8")


if __name__ == "__main__":
    main()
