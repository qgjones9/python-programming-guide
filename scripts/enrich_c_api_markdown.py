#!/usr/bin/env python3
"""
Rewrite docs/.../python-c-api-reference-manual/**/index.md from _c_api_toc.json.

Generates enriched parents (per-subsection headings + illustrative ```c blocks)
and leaves (anchored H1, bullets, ```c , Parent footer).

Requires `_c_api_toc.json`; generate with::

  python3 scripts/scrape_c_api_toc.py --json docs/.../_c_api_toc.json

Usage::

  python3 scripts/enrich_c_api_markdown.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_MANUAL = (
    Path(__file__).resolve().parent.parent / "docs" / "3.14.5" / "python-c-api-reference-manual"
)

C_API_BASE_URL = "https://docs.python.org/3/c-api/"

C_SNIPPETS = [
    """```c
#include <Python.h>

// Many C APIs return either a pointer or NULL; NULL means failure and the error
// indicator may be set (check with PyErr_Occurred()). Clear or propagate when appropriate.
PyObject *value = PyLong_FromLong(2026);
if (value == NULL) {
    return NULL;  /* let the interpreter surface the pending exception */
}
Py_DECREF(value);
```""",
    """```c
#include <Python.h>

/* Reference borrowing vs new refs: borrowed pointers stay alive only while outer
 * invariants guarantee the owner is not mutated; call Py_INCREF if you stash them. */
PyObject *borrowed = PyTuple_GET_ITEM(tuple_arg, 0);  /* borrowed from tuple */
Py_INCREF(borrowed);
/* ... stash borrowed where needed ... */
Py_DECREF(borrowed);
```""",
    """```c
#include <Python.h>

// When holding the GIL, most object APIs expect the main interpreter state;
// embedding code must bracket calls appropriately (see official section on threads).
PyGILState_STATE gstate = PyGILState_Ensure();
(void)PyRun_SimpleStringFlags("pass\\n", NULL);
PyGILState_Release(gstate);
```""",
    """```c
#include <Python.h>

// Raising in C: use PyErr_SetString / PyErr_Format; return NULL or -1 as documented.
if (arg == NULL) {
    PyErr_SetString(PyExc_TypeError, "argument must not be NULL");
    return NULL;
}
```""",
    """```c
#include <Python.h>

// Memory layers: prefer PyMem_Raw*/PyMem_* as documented for the lifetime you own;
// never mix allocators on the same pointer.
void *buf = PyMem_Malloc(64);
if (buf == NULL) {
    return PyErr_NoMemory();
}
PyMem_Free(buf);
```""",
]


def pick_snippet(key: str) -> str:
    h = sum(ord(c) for c in key)
    return C_SNIPPETS[h % len(C_SNIPPETS)]


def esc_md(s: str) -> str:
    return s.replace("\n", " ").strip()


def render_chapter_parent(ch: dict, manual: Path) -> str:
    title = ch["chapter_title"]
    url = ch["chapter_url"]
    lines: list[str] = [
        f"# [{title}]({url})",
        "",
        f"Local notes aligned with [**{title}**]({url}) in the "
        f"[Python/C API reference](https://docs.python.org/3/c-api/index.html). "
        "For full signatures, ownership rules, and thread-safety text, follow the official links below.",
        "",
    ]
    ch_dir = manual / ch["chapter_slug"]
    for sub in ch["subsections"]:
        can = sub["canonical"]
        st = sub["title"]
        lines.append(f"### [{st}]({can})")
        lines.append("")
        lines.append(
            f"- Official docs: [{esc_md(st)}]({can}) — behaviors, return values, and error conventions."
        )
        lines.append(
            "- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics."
        )
        lines.append(
            "- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section)."
        )
        lines.append("")
        lines.append(pick_snippet(ch["chapter_slug"] + "/" + sub["slug"]))
        lines.append("")

    lines.append("## Sections in this repo")
    lines.append("")
    subs_on_disk = {p.name for p in ch_dir.iterdir() if p.is_dir() and (p / "index.md").exists()}
    ordered = [(s["slug"], s["title"]) for s in ch["subsections"] if s["slug"] in subs_on_disk]
    extra_dirs = sorted(subs_on_disk - {s["slug"] for s in ch["subsections"]})
    for slug, t in ordered:
        lines.append(f"- [{t}]({slug}/index.md)")
    for slug in extra_dirs:
        lines.append(f"- [{slug.replace('-', ' ').title()}]({slug}/index.md)")
    lines.append("")
    return "\n".join(lines)


def render_chapter_standalone(ch: dict) -> str:
    title = ch["chapter_title"]
    url = ch["chapter_url"]
    lines = [
        f"# [{title}]({url})",
        "",
        f"Single-page chapter in [**{title}**]({url}); no subdivisions below in this mirror.",
        "Skim overview bullets here, follow the canonical link for the full narrative and API listings.",
        "",
        f"- Canonical: [{esc_md(title)}]({url})",
        "- Treat return codes and refcount contracts exactly as documented; many helpers set the error indicator instead of asserting.",
        "- Threading nuances (where applicable) belong to this chapter and may depend on `_Py` internals for debug builds.",
        "",
        pick_snippet(ch["chapter_slug"]),
        "",
    ]
    return "\n".join(lines)


def render_leaf(ch: dict, sub: dict) -> str:
    can = sub["canonical"]
    st = sub["title"]
    ch_title = ch["chapter_title"]
    ch_entry_plain = C_API_BASE_URL + ch["chapter_page"]

    lines = [
        f"# [{st}]({can})",
        "",
        f"Local notes on **{esc_md(st)}**, part of "
        f"[*{esc_md(ch_title)}*]({ch_entry_plain}). This page summarizes patterns; authoritative text stays upstream.",
        "",
        "- Follow the **[official section](%s)** for exact signatures, deprecation notes, and edge cases." % can,
        "- Most helpers advertise failures via `NULL` / `-1` and the **error indicator**; treat success paths carefully when references are borrowed vs new.",
        "- Threading semantics are easy to violate in C extensions; skim the threading chapter alongside this section.",
        "",
        pick_snippet(sub["slug"]),
        "",
        f"Parent: [{ch_title}](../index.md)",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    manual = REPO_MANUAL
    toc_path = manual / "_c_api_toc.json"
    if not toc_path.exists():
        raise SystemExit(f"Missing {toc_path}; run scrape_c_api_toc.py --json … first")

    chapters: list[dict] = json.loads(toc_path.read_text(encoding="utf-8"))

    for ch in chapters:
        cdir = manual / ch["chapter_slug"]
        if not cdir.is_dir():
            continue
        if ch["subsections"]:
            (cdir / "index.md").write_text(render_chapter_parent(ch, manual), encoding="utf-8")
        else:
            (cdir / "index.md").write_text(render_chapter_standalone(ch), encoding="utf-8")

        for sub in ch["subsections"]:
            leaf_dir = cdir / sub["slug"]
            leaf = leaf_dir / "index.md"
            if not leaf_dir.is_dir():
                continue
            leaf.write_text(render_leaf(ch, sub), encoding="utf-8")

    root_index = manual / "index.md"
    if root_index.exists():
        raw = root_index.read_text(encoding="utf-8")
        hdr = raw.split("\n## Table of Contents", 1)
        h1_and_intro = hdr[0].strip()
        toc_block = "\n## Table of Contents" + hdr[1] if len(hdr) == 2 else ""

        lines = h1_and_intro.split("\n")
        h1 = lines[0] if lines else "# [Python C API Reference Manual]"
        blurb = (
            f"{h1}\n\n"
            "Structured mirror of the "
            "**[Python/C API Reference Manual]"
            "(https://docs.python.org/3/c-api/index.html)**. "
            "Subpages scrape canonical Sphinx anchors (`_c_api_toc.json`). "
            "Tutorial-style layering lives in **[Extending and Embedding]"
            "(https://docs.python.org/3/extending/index.html)**.\n"
        )
        root_index.write_text(blurb + toc_block, encoding="utf-8")


if __name__ == "__main__":
    main()
