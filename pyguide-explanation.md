# About the opening comment in `pyguide.md`

The first lines of `pyguide.md` are an HTML comment (`<!-- ... -->`). In Markdown (including on GitHub), that block is **hidden when the document is rendered**, but it remains in the source for authors and tooling.

## What each line means

- **`AUTHORS:`** — A short metadata label for maintainers: who cares for the doc or who should read this note first.

- **`Prefer only GitHub-flavored Markdown in external text.`** — Contributors should stick to **GitHub Flavored Markdown (GFM)**—syntax GitHub’s renderer supports (tables, task lists, strikethrough, autolinks, fenced code blocks, and so on)—and avoid flavors or extensions that other tools accept but GitHub does not. *External text* means anything published or shared where GitHub-style rendering is the norm (for example the repo on GitHub or docs that target the same rules).

- **`See README.md for details.`** — Points to a README in the repo for the full policy. If there is no `README.md` next to this style guide, that reference may be stale or the README may live higher in the repository tree.

**In one sentence:** the comment is an author-only reminder to write the guide in portable GFM and to follow the README when it exists.

## The comment before the table of contents (`markdown="1"`)

Right after the main title, `pyguide.md` has this line:

```html
<!-- markdown="1" is required for GitHub Pages to render the TOC properly. -->
```

That line is **only documentation for authors**. It does not change rendering by itself.

The behavior it describes applies to the **next** element, `<details markdown="1">`, which wraps the “Table of Contents” list. The attribute **`markdown="1"`** is a [**kramdown**](https://kramdown.gettalong.org/syntax.html#html-blocks) extension (not part of the core GFM spec): it tells the Markdown processor used by many **Jekyll / GitHub Pages** sites to **parse Markdown inside that HTML block**. Without it, the list inside `<details>` might be emitted as literal text instead of a real list when the site is built with kramdown.

On **github.com**’s own preview, `<details>` / `<summary>` work, and list handling inside them follows GitHub’s current CommonMark/cmark-gfm rules; that can differ slightly from a Jekyll+kramdown build. The comment is there so people editing for **GitHub Pages** do not remove `markdown="1"` and break the published TOC.

## Does GFM have other “variable-like” things in comments?

**No.** In GitHub Flavored Markdown, an HTML comment is just a comment: the spec does not define `<!-- name=value -->` or other magic inside `<!-- ... -->` for variables, includes, or toggles. Anything that looks like a “directive” in a comment (for example `<!-- markdown="1" ... -->` on line 9) is **plain text for humans** unless a separate tool (not GFM) scans for it.

Other systems **outside** strict GFM do add special markup—examples include **Hugo** shortcodes, **MDX** in JSX, **MkDocs** plugins, or **Jekyll** front matter in `---` at the top of the file. Those are not GFM features.

What *is* related to the TOC note—but not a comment—is **`markdown="1"` as an HTML attribute** on an element (here `<details>`). kramdown also supports values like **`markdown="span"`** and **`markdown="block"`** for finer control over how inner Markdown is parsed. Those are processor options, not GFM comment options.

