---
name: python-docs-section
description: >-
  Mirror and enrich official docs.python.org manuals (tutorial, standard library,
  C API, language reference, extending) under docs/<release>/: scrape the book
  index for the real table of contents, scaffold index.md stubs with canonical
  chapter links, then add teaching bullets and code examples. Tutorial chapters
  require runnable Python; C API/extending use illustrative C. Includes
  version-bump steps and python-programming-guide scraper commands.
---

# Python documentation mirror (unified workflow)

**Project copy:** `.cursor/skills/python-docs-section/SKILL.md`

Use this skill when you **mirror or refresh** an official Python manual in a versioned tree such as `docs/3.14.5/tutorial/`. Typical triggers: a **new CPython release**, upstream TOC edits, or filling in teaching notes next to the official text.

---

## Key terms

These names appear throughout the workflow. **Prefer the plain-language label** in prose; use the **shorthand** only in tables, scripts, or when it matches a real URL path.

| Plain language | Shorthand (when needed) | Meaning |
|----------------|-------------------------|---------|
| **Manual slug** | `SECTION` | The path segment on docs.python.org after the version, e.g. `tutorial`, `library`, `c-api`, `reference`, `extending`. |
| **Upstream book root** | `BASE` | Root URL for that manual, e.g. `https://docs.python.org/3/tutorial/` or `https://docs.python.org/3.14/tutorial/` when pinned to a minor version. |
| **Book index page** | `INDEX` | Always `{BASE}index.html` — scrape this for the **full** table of contents; never guess chapter filenames from titles. |
| **Local mirror folder** | `LOCAL_ROOT` | Repo directory for this book, e.g. `docs/versions/3.14.5/tutorial/`. |

Relative links in Sphinx HTML resolve against **`BASE`**, not bare `/3/`.

**Which upstream version to follow:** `…/3/…` tracks the **current** 3.x docs; `…/3.N/…` pins to a **specific minor** (closer to a frozen release). Use the same choice as your local folder name (`3.14.5` vs `3.15.0`).

---

## python-programming-guide — where each manual lives

| Local folder (under `docs/<ver>/`) | Manual slug on python.org | Official index | Automation in this repo |
|------------------------------------|---------------------------|----------------|-------------------------|
| `tutorial/` | `tutorial` | [tutorial index](https://docs.python.org/3/tutorial/index.html) | By hand or agent; use **runnable-tutorial** rules on chapter `index.md`. |
| `standard-library/` | `library` | [library index](https://docs.python.org/3/library/index.html) | By hand or agent; large tree — usually one chapter at a time. |
| `python-c-api-reference-manual/` | `c-api` | [c-api index](https://docs.python.org/3/c-api/index.html) | `scrape_c_api_toc.py` → `_c_api_toc.json`; `enrich_c_api_markdown.py`. |
| `language-reference/` | `reference` | [reference index](https://docs.python.org/3/reference/index.html) | `scrape_reference_toc.py` → `_reference_toc.json`; `enrich_reference_markdown.py`. |
| `extending-and-embedding-python-interpreter/` | `extending` | [extending index](https://docs.python.org/3/extending/index.html) | `scrape_extending_toc.py` → `_extending_toc.json`; `enrich_extending_markdown.py`. |

---

## When to use this skill

- **New stub pages or TOC sync** after upstream changes or a new Python release.
- **Enriched chapters**: distilled bullets, fenced examples, and **`## Sections in this repo`** linking child folders.
- **Release maintenance**: diff old vs new scraped JSON or search for changed canonical URLs; record deltas in project changelog or chapter notes — not in this skill file.

---

## Step 1 — Discover the outline from the official index

1. Fetch the **book index page** (`INDEX`) HTML.
2. Locate Sphinx **`toctree-wrapper compound`** blocks. Some books have **several** wrappers (e.g. extending) or sections that exist only as **`index.html#fragment`** — merge those into one outline model (see `scrape_extending_toc.py`).
3. Walk **`toctree-l1`**, **`toctree-l2`**, and deeper levels: each `<a class="reference internal" href="…">` becomes a full URL by joining **`href`** to **`BASE`**.

**Hard rule:** Chapter filenames come from **`href`**, not from slugified titles (`exceptions.html` vs `exceptions` are not interchangeable).

---

## Step 2 — Scaffold local folders and stub `index.md`

### Folder layout

Each outline entry gets `{LOCAL_ROOT}/{slug}/…/index.md` with an H1 that links upstream:

`# [Title](https://…/{chapter}.html#fragment)`

Use **URL fragments from `href`** when present (e.g. `#py-getargcargv`), not guesses from directory names.

### Nesting

- **Indented GitHub-flavored TOC** ↔ directory depth (two spaces per level), **or**
- **Numbered outline** `N.M. Title` ↔ nested slug paths (tutorial convention).

### Slug rules

Lowercase; normalize dashes; remove characters unsafe in paths; collapse repeated `-`. You may strip leading **`N.`** from titles for **directory** names while **keeping numbers in link text** when the official outline uses them.

### Parent page table of contents

Use heading level **`#` × (2 + depth)**; internal links always end with **`…/index.md`**.

Markdown links must be **`[text](url)`** — balanced parentheses (avoid `](url]` typos).

---

## Step 3 — Enrich each chapter `index.md`

1. **`# [Chapter title](canonical chapter URL)`** — add a `#fragment` only when the section truly lives on `index.html#…`.
2. One short **scope** paragraph: what this chapter covers and that full prose stays on docs.python.org.
3. Per subsection: **`### … — [Title](chapter.html#anchor)`**, teaching bullets (distilled, not copied), then fenced examples.
4. **`## Sections in this repo`** listing `[Title](child-path/index.md)` for subfolders.

---

## Example styles (pick one per book or chapter)

| Style | Code fences | Comments | Validation |
|-------|-------------|----------|------------|
| **Runnable tutorial** | ` ```python ` | `#` line comments; optional one-line **goal** at top of longer blocks | **Required:** every ` ```python ` block runs with **`exec`** without error. Use **`ns = {}; exec(code, ns, ns)`** when nested functions need shared globals — not separate empty `{}` for globals and locals. Prefer `assert`; use `io.StringIO` to capture `print`. |
| **Language reference** | ` ```python ` mostly | Explain edge cases (e.g. newline in `s` vs in `repr(s)`) | Run **`exec`** on pedagogical snippets when practical. |
| **C API / extending** | ` ```c ` | `//` for ownership, GIL, errors | Illustrative only — no compile step required. |
| **Mixed** | `python` and `c` | As needed | **`exec`** only on `python` blocks. |

### Runnable tutorial — extra rules

- No **`input()`**, no **`while True`**, no “press Ctrl+C” in executable blocks.
- **REPL `_`**: mention in comments; do not **`assert`** on `_` in a `.py` exec unless you simulate REPL behavior.
- Say when **interactive session** behavior differs from **script file** behavior.

### Avoid in all executable examples

Infinite loops; `input()`; checks that confuse `repr` with string content (`"\n"` in `repr(s)` vs `"\n"` in `s`) — explain the distinction in prose or comments instead.

---

## Bumping to a new Python release

1. **Pick upstream URL style:** rolling `…/3/…` or pinned `…/3.N/…`; note the choice in scraped JSON commits or project notes.
2. **Copy** the prior `docs/X.Y.Z/` tree to `docs/X.Y.Z′/` (or use a branch) so you can compare.
3. **Re-fetch the book index** and regenerate `_*_toc.json` for scripted manuals (C API, language reference, extending).
4. **Diff JSON** (`git diff`, `jq`) for new/removed chapters, subsection slugs, or changed canonical URLs — that diff is your **outline changelog**.
5. **Re-run enrich scripts** for boilerplate; resolve conflicts where you edited bullets by hand.
6. **Tutorial and standard library:** re-scrape TOC from the official index (agent or future scripts); re-**`exec`** runnable-tutorial blocks after edits.
7. **Optional:** add `docs/<ver>/changelog.md` (or repo CHANGELOG) noting sync date, new sections, and notable link changes.

---

## Repo commands (python-programming-guide)

Replace `<ver>` with your release folder (e.g. `3.14.5`).

| Manual slug | Commands |
|-------------|----------|
| `reference` | `python3 scripts/scrape_reference_toc.py --json docs/<ver>/language-reference/_reference_toc.json` then `python3 scripts/enrich_reference_markdown.py` |
| `c-api` | `python3 scripts/scrape_c_api_toc.py --json docs/<ver>/python-c-api-reference-manual/_c_api_toc.json` then `python3 scripts/enrich_c_api_markdown.py` |
| `extending` | `python3 scripts/scrape_extending_toc.py --json docs/<ver>/extending-and-embedding-python-interpreter/_extending_toc.json` then `python3 scripts/enrich_extending_markdown.py` |

**Tutorial** and **library:** follow Steps 1–3 manually until dedicated scripts exist.

---

## Conventions (match existing repo pages)

- **Canonical HTTPS** in H1s and subsection links; balanced **`[text](url)`**.
- **Internal links:** explicit paths such as `subdir/index.md`.
- **Commit messages:** one line, ≤120 characters when workspace rules require it; no Conventional Commit prefix if the project disallows it.

---

## Quick checklist

- [ ] **Upstream book root** and **index page** match your documented version strategy (`/3/` vs `/3.N/`).
- [ ] Outline built from real **`href`** values; fragments taken from Sphinx, not guessed.
- [ ] Example style matches the book (**runnable tutorial** vs **illustrative C**).
- [ ] Runnable tutorial: every ` ```python ` block **`exec`** clean (shared namespace for nested defs).
- [ ] **`## Sections in this repo`** links end with **`…/index.md`**.
- [ ] Work stays in requested `docs/` paths unless the user asks to expand.
