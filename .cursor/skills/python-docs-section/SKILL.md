---
name: python-docs-section
description: >-
  Scaffold and enrich nested Markdown mirrors of any docs.python.org Sphinx
  section from its section index HTML: parses the toctree for chapter URLs,
  scrapes each chapter page for subsection fragments, emits stubs and parent
  index.md trees with bullets and fenced examples in the appropriate language.
  Typical sections: tutorial, library, c-api, reference, extending, howto, using,
  distributing. Use when mirroring Official Python Documentation into a docs/
  tree alongside versioned stubs (e.g. docs/3.14.5/).
---

# Python documentation section (stubs + enriched index)

**Project skill:** `.cursor/skills/python-docs-section/SKILL.md`

End-to-end workflow for **any** [docs.python.org](https://docs.python.org/3/) Sphinx section (same structure across manuals): **(1)** resolve the section root and chapter map from `{BASE}index.html`, **(2)** scaffold or refresh nested `slug/…/index.md` with `H1` links to **`chapter.html#fragment`**, **(3)** optionally enrich chapter parents with bullets + fenced examples plus **Sections in this repo**.

---

## Inputs (contract)

- **`SECTION`** — URL path segment after `/3/` (no slashes), e.g. `tutorial`, `library`, `c-api`, `reference`, `extending`, `faq`, `howto`, `using`, `install`, `distributing`.
- **`BASE`** — section root URL: **`https://docs.python.org/3/{SECTION}/`**
- **`INDEX`** — book index page: **`{BASE}index.html`**

All relative `href` values from Sphinx (e.g. `intro.html`, `exceptions.html#raising-exceptions`) are joined against **`BASE`**, not `/3/`.

---

## When to use

- Mirroring **C API**, **Standard Library**, **Tutorial**, **Language Reference**, etc. under a local `docs/<version>/<manual>/` tree.
- User provides a TOC region or an existing scaffold and wants canonical **`https://`** links with correct **`#anchors`** scraped from Sphinx (do not invent chapter filenames — `exceptions.html` is not guessable from the slug alone).
- User wants enrichment with **comments inside fences** (`#` in Python, `//` in C).

---

## Phase 0 — Resolve section + chapter map

1. Fetch **`INDEX`** HTML.
2. Locate the Sphinx toctree wrapper (typically a `compound`/`toctree`-class block containing `<a class="reference internal" href="…">` links).
3. Build **chapter title → absolute chapter URL** (strip only in-page `#fragment` for the chapter file mapping). Nested bullets in the TOC imply subsections belong to **that chapter’s HTML page**, not separate files unless the TOC links to another `*.html`.

**Important:** Manuals like **`c-api`** use opaque filenames (**`intro.html`**, **`init.html`**, **`abstract.html`**). Parsing **`c-api/index.html`** is mandatory; slugifying titles is not sufficient.

---

## Phase 1 — Scaffold directories and stub `index.md`

Same as for the Tutorial workflow:

### Parent directory

Sections live under the directory that contains the source `index.md` (e.g. `docs/3.14.5/python-c-api-reference-manual/` mirroring **`c-api`**).

### Chapter page scrape — markdown links with anchors

When subsections appear **inside** one chapter page:

1. Fetch `https://docs.python.org/3/{SECTION}/{chapter}.html` (no `#` initially).
2. Collect `<a class="reference internal" href="#fragment">` from the sidebar/local TOC where present.
3. Canonical subsection URL: **`{chapter_abs_url}#{fragment}`**.
4. Stub `index.md` H1: **`# [Title](canonical_url_with_fragment)`**.

### Hierarchy rules | Slugify | Parent TOC headings

Follow the Tutorial skill: indented bullets ↔ directory depth, **or** numeral outlines; **`#` × (2 + depth)** heading levels on the parent TOC; targets end with **`…/index.md`**.

---

## Phase 2 — Enrich chapter `index.md`

1. Keep H1 as `# [Chapter](https://docs.python.org/3/{SECTION}/{chapter}.html)` (canonical chapter URL, usually no `#`).
2. Add a short scope paragraph pointing to the official chapter.
3. For each subsection: heading with **`[Title](chapter.html#fragment)`**, bullets distilled from docs (names, contracts, pitfalls), fenced examples as below.
4. End with **`## Sections in this repo`** listing child **`[Title](subdir/index.md)`** links.

### Code fence language (pick per manual / chapter)

| Context | Typical fence | Comments |
|---------|---------------|----------|
| `c-api/` | **` ```c `** | Ownership, refcounts, errors, **GIL** notes with `//` |
| `tutorial/`, much of `library/` | **` ```python `** | Prefer small **`assert`**-style snippets with `#` when self-contained |

**Mixed manuals** may include both **`python`** and **`c`** on the same page when appropriate.

### Validation policy

- **` ```python ` fences:** If examples are **self-contained**, prefer snippets that **`exec`** cleanly in isolation (recommended for Tutorial-style chapters). Not a hard gate for every repo.
- **` ```c ` fences:** Illustrative only; **no mandatory compile/exec** step. Keep snippets short, compilable-shaped, avoid infinite loops.

### Forbidden in fences

- No **`input()`**, no **`while True`**, no **`while (1)`** demos, no “press Ctrl+C” patterns.

---

## Conventions aligned with existing docs

- **Canonical:** `https://docs.python.org/3/...` H1 and subsection URLs.
- **Internal:** `subdir/index.md` relative to the file.
- **Commit messages:** one line ≤120 chars if committing; respect project rules.

---

## Quick checklist

- [ ] `SECTION`/`BASE` correct; chapter URLs parsed from **`{BASE}index.html`**, not guessed.
- [ ] Subsection **`#fragment`** from chapter HTML TOC when available.
- [ ] Fence language matches the manual (`c-api` vs `tutorial`).
- [ ] **`[text](url)`** markdown balanced — **no** stray `]` after URLs.
- [ ] Parent TOC uses **`…/index.md`**.
- [ ] No drive-by edits outside the requested docs tree unless asked.
