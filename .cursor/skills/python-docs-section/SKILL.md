---
name: python-docs-section
description: >-
  Scaffold and enrich nested Markdown mirrors of docs.python.org Sphinx books
  (tutorial, library, c-api, reference, extending, …): Phase 0 scrape of
  index.html toctree, Phase 1 stubs with canonical chapter.html#anchor H1s,
  Phase 2 enrichment with python or c fences and teaching comments. Supports
  strict tutorial mode (exec-validated python) and reference/C-API modes.
  Includes version-bump workflow for local docs/X.Y.Z trees and
  python-programming-guide script map (tutorial, standard-library, c-api,
  language-reference, extending).
---

# Python documentation section (unified)

**Canonical project skill:** `.cursor/skills/python-docs-section/SKILL.md`

Use this skill whenever you mirror or refresh **any** official Python manual under a versioned `docs/<python-release>/...` tree—especially when **CPython bumps** and you want local notes, TOC sync, and a clear place to record **what changed** (new sections, renames, link fixes).

---

## Inputs (contract)

| Input | Meaning |
|-------|---------|
| **`SECTION`** | Path segment after the version root, e.g. `tutorial`, `library`, `c-api`, `reference`, `extending`. |
| **`BASE`** | Book root URL, e.g. **`https://docs.python.org/3/{SECTION}/`** or **`https://docs.python.org/3.14/{SECTION}/`** for a **minor-pinned** doc set. |
| **`INDEX`** | **`{BASE}index.html`** — always scrape this for the global toctree; do not guess chapter filenames from titles. |
| **`LOCAL_ROOT`** | Directory in your repo holding this book’s mirror, e.g. `docs/3.14.5/tutorial/`. |

Relative `href` values in Sphinx HTML join against **`BASE`**, not bare `/3/`.

**Version choice:** `…/3/…` tracks the **current** 3.x branch on python.org; `…/3.N/…` pins to a **specific minor** (closer to a frozen release). Match that choice to the folder name you use locally (`3.14.5` vs `3.15.0`).

---

## python-programming-guide — manual map

These local trees follow this skill; **automated scrapers** exist where listed.

| Local directory (under `docs/<ver>/`) | `SECTION` | Upstream index | Scrape + enrich scripts |
|--------------------------------------|-----------|----------------|-------------------------|
| `tutorial/` | `tutorial` | [tutorial index](https://docs.python.org/3/tutorial/index.html) | Manual / agent (no dedicated script yet); use **tutorial-strict** enrichment for chapter `index.md`. |
| `standard-library/` | `library` | [library index](https://docs.python.org/3/library/index.html) | Manual / agent or future script; huge tree—usually chapter-by-chapter. |
| `python-c-api-reference-manual/` | `c-api` | [c-api index](https://docs.python.org/3/c-api/index.html) | `scripts/scrape_c_api_toc.py` → `_c_api_toc.json`; `scripts/enrich_c_api_markdown.py`. |
| `language-reference/` | `reference` | [reference index](https://docs.python.org/3/reference/index.html) | `scripts/scrape_reference_toc.py` → `_reference_toc.json`; `scripts/enrich_reference_markdown.py`. |
| `extending-and-embedding-python-interpreter/` | `extending` | [extending index](https://docs.python.org/3/extending/index.html) | `scripts/scrape_extending_toc.py` → `_extending_toc.json`; `scripts/enrich_extending_markdown.py`. |

---

## When to use

- **New stubs or TOC refresh** after upstream edits or a **new Python release**.
- **Enriched chapter pages**: bullets + fenced examples + **`## Sections in this repo`**.
- **Changelog-style maintenance**: diff old vs new scraped JSON or grep for changed `canonical` URLs; update prose in a repo changelog or chapter notes—not in this skill file.

---

## Phase 0 — Resolve section + chapter map

1. Fetch **`INDEX`** HTML.
2. Find **`toctree-wrapper compound`** blocks. Some indices have **multiple** wrappers (e.g. `extending/index.html`) or synthetic sections anchored on **`INDEX#fragment`** only—merge those into your JSON model explicitly (see extending scraper pattern).
3. Parse **`toctree-l1` / `toctree-l2`** (and deeper if present): `<a class="reference internal" href="…">` → join to **`BASE`**.

**Hard rule:** Never infer chapter filenames (e.g. `exceptions.html` vs `exceptions`) from slugified titles—**href is truth**.

---

## Phase 1 — Scaffold `slug/…/index.md`

### Directory layout

Each logical § gets `{LOCAL_ROOT}/{segment}/…/index.md`; **H1**:

`# [Title](https://…/{chapter}.html#fragment)`

Use **fragments from `href`** when present (`#py-getargcargv`), not slugify drift.

### Hierarchy

- **Indented GFM TOC** ↔ path depth (two spaces per level), **or**
- **Numeral outline** `N.M.§ Title` ↔ stack-of-slugs (see original tutorial convention).

### Slugify

Lowercase; normalize dashes; strip characters unsafe in paths; collapse `-`. Strip leading **`N.`** numbering from titles when deriving **directory** slugs if your tree omits numeric prefixes—**keep numbers in markdown link titles** when the upstream outline uses them.

### Parent TOC in `index.md`

Headings **`#` × (2 + depth)**; every internal target ends with **`…/index.md`**.

Markdown links must be **`[text](url)`** — never `](url]` by mistake.

---

## Phase 2 — Enrich chapter `index.md`

1. **`# [Chapter title](canonical chapter URL)`** (fragment only when that chapter truly lives at `index.html#§`).
2. One short scope paragraph pointing at upstream for full prose.
3. Per subsection: **`### … — [Title](chapter.html#anchor)`**, bullets (teaching distilled, not a copy-paste of docs.python.org), then fenced examples.
4. **`## Sections in this repo`** with `[Title](relative/index.md)` children.

---

## Enrichment modes (pick one per book/chapter)

| Mode | Fences | Comments | Validation |
|------|--------|----------|------------|
| **tutorial-strict** | **` ```python `** | **`#`** line comments, optional end-of-line; one-line **goal** at top of bigger blocks | **Required:** each ` ```python ` block **`exec`** clean. Use **`ns = {}; exec(code, ns, ns)`** if the block defines nested functions that close over globals—**not** distinct empty `{}` for globals vs locals. Prefer `assert`; use `io.StringIO` for `print` checks. |
| **reference-manual** (language ref) | **` ```python `** mostly | Teach edge cases (“`\n` in `s` vs `repr(s)`”) | Prefer **same exec policy** when blocks are pedagogical snippets. |
| **c-api / extending** | **` ```c `** | **`//`** for ownership, GIL, errors | Illustrative only—**no mandatory compile.** |
| **mixed** | `python` + `c` | As appropriate | Gate **exec** only on `python`. |

### Tutorial-strict specifics (carry-over from legacy tutorial skill)

- No **`input()`**, no **`while True`**, no “press Ctrl+C” in executable fences.
- **REPL `_`**: mention in comments; don’t **`assert`** on `_` in a `.py` exec unless you simulate REPL semantics.
- **REPL vs file:** state when behavior differs.

### Forbidden everywhere

Infinite loops in any executable fence; `input()`; misleading `repr` vs string content checks (`"\n"` in `repr(s)` vs `"\n"` in `s`)—prefer the pairing explained in prose/comments.

---

## Python release bump (changelog-minded workflow)

1. **Choose doc URL lineage:** stay on **`/3/`** or pin **`/3.N/`** and record that in `_*.json` commit messages or project notes.
2. **Clone or copy** the prior `docs/X.Y.Z/` tree to **`docs/X.Y.Z′/`** (or work on a branch) so history is comparable.
3. **Re-fetch `INDEX`** and regenerate **`_*_toc.json`** for each scripted manual (**c-api**, **reference**, **`extending`**).
4. **Diff JSON** (`git diff`, `jq`) for added/removed **`chapter_slug`** / **`subsection.slug`** / changed **`canonical`** strings—those deltas are your **TOC changelog**.
5. **Re-run enrichers** to refresh boilerplate headers/snippets; resolve merge conflicts where you hand-edited bullets.
6. **Tutorial / library:** re-scrape TOC from `tutorial/index.html` / `library/index.html` via agent pass or future scripts; bump **tutorial-strict** `exec()` after edits.
7. **Optional:** add a short **`docs/<ver>/changelog.md`** (or repo **CHANGELOG**) section: synced to docs.python.org 3.K with a dated note listing new sections and notable link changes — user-maintained.

---

## Repo tooling (python-programming-guide)

| `SECTION` | Commands |
|-----------|----------|
| `reference` | `python3 scripts/scrape_reference_toc.py --json docs/<ver>/language-reference/_reference_toc.json` then `python3 scripts/enrich_reference_markdown.py` |
| `c-api` | `python3 scripts/scrape_c_api_toc.py --json docs/<ver>/python-c-api-reference-manual/_c_api_toc.json` then `python3 scripts/enrich_c_api_markdown.py` |
| `extending` | `python3 scripts/scrape_extending_toc.py --json docs/<ver>/extending-and-embedding-python-interpreter/_extending_toc.json` then `python3 scripts/enrich_extending_markdown.py` |

**Paths:** Replace `<ver>` with your folder (e.g. `3.14.5`).  
**tutorial** / **library:** follow Phase 0–2 manually until dedicated scripts land.

---

## Conventions aligned with existing docs

- **Canonical HTTPS** in H1s and subsection links; **`[text](url)`** balanced parentheses.
- **Internal links:** explicit `subdir/index.md` paths.
- **Commit messages:** one line, ≤120 characters if workspace rule requires; no Conventional Commit prefix where project rules disallow it.

---

## Quick checklist

- [ ] `BASE`/`INDEX` match the Python version strategy you document locally (`/3/` vs `/3.N/`).
- [ ] TOC parsed from real **`href`** values; fragments from Sphinx, not guesses.
- [ ] Fence language matches mode (**tutorial-strict python** vs **c-api c**).
- [ ] Tutorial-strict chapters: all ` ```python ` blocks **`exec`** clean (correct namespace for nested defs).
- [ ] **`## Sections in this repo`** uses **`…/index.md`**.
- [ ] Scope limited to requested `docs/` paths unless asked to expand.
