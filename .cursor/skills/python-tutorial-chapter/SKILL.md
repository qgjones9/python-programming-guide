---
name: python-tutorial-chapter
description: >-
  Scaffolds nested Markdown tutorial sections from docs.python.org TOC (indent
  or numeral hierarchy), resolves canonical URLs from official Sphinx HTML
  (book index and per-chapter pages), emits markdown links with full
  base.html#anchor URLs for each section, and expands a chapter index.md with
  summaries, executable fenced Python examples, and inline comments inside
  those snippets explaining behavior. Use when mirroring Python
  Tutorial (or similar Sphinx) chapters into a docs tree, adding stub index.md
  files, or enriching docs/.../tutorial/.../index.md like standard-library or
  tutorial chapter pages in the styleguides Python docs.
---

# Python tutorial chapter (stubs + enriched index)

**Project skill:** `.cursor/skills/python-tutorial-chapter/SKILL.md` in this repo (also available globally as `~/.cursor/skills/python-tutorial-chapter/SKILL.md`).

End-to-end workflow used for [The Python Tutorial](https://docs.python.org/3/tutorial/index.html) chapters in a local `docs/` tree: **(1)** create nested `…/slug/…/index.md` stubs with H1 links to the official page, **(2)** replace or add a structured TOC on the parent chapter `index.md`, **(3)** optionally expand that chapter with bullets + runnable `python` fences (with **comments inside the fences** teaching each step), and a “Sections in this repo” link block.

---

## When to use

- User points at a chapter `index.md` plus a TOC region (GFM bullets, or a numbered outline like `2.1.1. Title`).
- User wants local stubs that mirror `docs.python.org/3/tutorial/...` (or another Sphinx chapter) with correct `# […](url)` targets.
- User asks to “do the same” as **An Informal Introduction** or **More Control Flow Tools**: summary + snippets + child links.
- User wants **explained snippets** (`#` comments inside fenced Python) alongside asserts.

---

## Phase 1 — Scaffold directories and stub `index.md`

### Parent directory

- New sections live under the directory that contains the source `index.md` being edited (e.g. `docs/3.14.5/tutorial/`).

### Resolve official URLs (recommended)

1. Fetch the chapter’s **index** HTML from Python docs (e.g. `https://docs.python.org/3/tutorial/index.html` for the full tutorial TOC).
2. Parse the **`toctree-wrapper compound`** block: `<a class="reference internal" href="…">` gives relative `*.html#anchor` links; join with `https://docs.python.org/3/tutorial/` (adjust path for other manuals).
3. Build a map from **TOC label text** → **absolute URL**. Normalize keys: collapse whitespace; normalize curly quotes to ASCII where the outline uses straight quotes.

### Chapter page scrape — markdown links with **anchors**

When mapping sections **inside one chapter** (e.g. [Data Structures](https://docs.python.org/3/tutorial/datastructures.html)), scrape **that chapter’s HTML**, not only the book index.

1. Fetch `https://docs.python.org/3/tutorial/<chapter>.html` (no `#` yet).
2. Parse the page’s local TOC: `<a class="reference internal" href="#fragment">…</a>`. The `href` is often **`#comparing-sequences-and-other-types`** (fragment only).
3. **Canonical URL** for each subsection: **`{chapter_url}#{fragment}`** — same origin as the page, e.g. `https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types`.
4. **Stub `index.md` H1** for that subsection must use the **full URL including `#fragment`** so the heading links straight to the official §.
5. **Enriched chapter `index.md`:** for each numbered §, add an **official deep link** beside or under the heading, using valid markdown:

   - Correct: `**5.8** — [Comparing Sequences and Other Types](https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types)`
   - Or fold into a heading: `### 5.8 — [Comparing Sequences and Other Types](https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types)`
   - **Invalid:** a closing `]` instead of `)` after the URL — markdown links are **`[text](url)`** only.

6. **Fragment source of truth:** prefer the `href` from the scraped `<a>`; if building from heading text, match Sphinx’s slug rules (lowercase, hyphens) and verify the link targets an existing id on the page when possible.

### Hierarchy rules (pick one source shape)

**A. Indented GFM bullets** (two spaces per child level, `- [Title](url)` optional):

- Each bullet → one slug segment; depth from leading spaces: `depth = len(indent.replace("\t", "    ")) // 2`.
- Maintain a **stack of slugs**; pop while `len(stack) > depth`, append slug for current line; path = `stack` joined with `/`.

**B. Numeral outline** (`1. Title`, `2.1. Subtitle`, …):

- Parse `^(\d+(?:\.\d+)*)\.\s+(.+)$` → integer parts list `parts`.
- **Stack update:** `while len(stack) >= len(parts): stack.pop()` then `stack.append(slugify(title))`. Sibling vs child follows subsection numbering (same pattern as legal-outline / Sphinx section numbers).

### Slugify (directory names)

- Lowercase; replace em/en dashes with `-`; strip punctuation unsuitable for paths (`.,;:()'\"«»`); collapse spaces to `-`; collapse repeated `-`.

### Stub file content

- Path: `{parent}/{slug[/slug…]}/index.md`.
- First line: `# [Display title](canonical_url)` — URL must match the official TOC entry for that section (including `#fragment` when present).
- Optional second line: one short sentence (e.g. local notes pointer). Keep minimal unless the user asks for more.

### Parent chapter TOC replacement (optional)

- Replace the raw TOC list with markdown headings whose depth matches nesting: top-level `##`, next `###`, then `####`, … formula **`#` × (2 + depth)** where `depth = len(parts)-1` for numerals, or bullet depth as above.
- Link text: include numbering in the link label if the outline uses it (e.g. `## [2.1.1. Argument Passing](…/index.md)`).
- Every link target must end with **`…/index.md`** (not a bare trailing `/`).

---

## Phase 2 — Enrich the chapter `index.md`

Apply when the user wants the “amazing” long-form chapter page.

1. **Keep** the H1 as `# [Chapter title](https://docs.python.org/3/tutorial/<chapter>.html)` (or the exact chapter URL).
2. Add a **one-paragraph** scope line pointing to the official chapter for prose and updates.
3. For each major **§** (e.g. `### 4.3 — The range() function`):
   - Optional but recommended: a **markdown link** to the official subsection using **`chapter.html#anchor`** (from the chapter-page scrape above), either in the heading or as a bullet line right under it.
   - Short **bullets** mirroring the tutorial’s teaching points (not a copy-paste of the whole site).
   - One or more **` ```python `** blocks that **demonstrate** those bullets.
4. **Snippet rules:**
   - Prefer **`assert`**-style checks or small return values over `print` noise; use **`io.StringIO`** + `print(..., file=buf)` when `print` behavior matters.
   - **Comments inside snippets (recommended):** add **`#` line comments** (and short **end-of-line comments** where helpful) so each block teaches *why* the code is written, not only *what* it outputs. Put a **one-line block goal** at the top of larger examples (e.g. what API or pitfall is illustrated). Comment **non-obvious** choices (e.g. `deque` for queues, `sorted` vs `.sort`, chained comparisons, mutable default traps). Avoid narrating every obvious line; do not restate the prose bullets verbatim.
   - **Do not** embed `input()`, infinite `while True`, or “press Ctrl+C” examples as executable blocks.
   - For **REPL-only** behavior (`_` last result), mention in a comment; do not assert on `_` inside a `.py` exec unless simulating.
   - Avoid false expectations: e.g. `"\n" in repr(s)` is wrong for newlines — use `"\n" in s` and `"\\n" in repr(s)` if both ideas matter.
5. **Validation (required):** extract every ` ```python ` fence from the chapter file and `exec` them in order in a fresh namespace (or one shared namespace if order matters); **fix failures** until all pass.
6. End with **`## Sections in this repo`** (or under the chapter TOC heading) listing **`[Title](relative/path/index.md)`** links to stubs created in Phase 1.

---

## Conventions aligned with existing docs

- **Canonical links:** `https://docs.python.org/3/...` in H1s and intro blurbs; subsection pointers use **`…/<chapter>.html#anchor`** when scraped from the chapter TOC.
- **Internal links:** explicit `subdir/index.md` paths relative to the chapter file.
- **Commit messages** (if committing): follow workspace one-line ≤120 chars rule; no Conventional Commits prefix if the repo rule says so.

---

## Quick checklist

- [ ] TOC labels align with parsed official links (normalize whitespace / quotes).
- [ ] Chapter-page scrape: each § has a correct **`[label](https://…/chapter.html#fragment)`** link (parenthesis close, not `]`).
- [ ] Every stub path exists and has `index.md` with correct `https://` H1 **including `#fragment`** when the official TOC uses a fragment.
- [ ] Parent TOC uses `…/index.md` links.
- [ ] Chapter enrichment: bullets + `python` blocks per section; snippets include **teaching comments** where non-obvious; all blocks `exec` clean.
- [ ] No drive-by edits outside the requested doc tree.
