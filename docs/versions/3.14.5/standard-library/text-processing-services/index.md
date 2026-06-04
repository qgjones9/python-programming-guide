# [Text Processing Services](https://docs.python.org/3/library/text.html)

Python’s standard library groups string manipulation, pattern matching, Unicode normalization, and interactive line editing under **Text Processing Services**. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/text.html); this hub orients you to each module, when to reach for it, and how the pieces fit together.

Related material outside this section: built-in [`str`](../built-in-types/text-sequence-type-str/index.md) methods, the [`codecs`](../binary-data-services/codecs-codec-registry-and-base-classes/index.md) module for encodings, and third-party packages such as [regex](https://pypi.org/project/regex/) when you need richer Unicode or backtracking control than [`re`](re-regular-expression-operations/index.md) provides.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`string`](string-common-string-operations/index.md) | ASCII character sets, `str.format()` mini-language, custom `Formatter` subclasses |
| [`string.templatelib`](stringtemplatelib-support-for-template-string-literals/index.md) | **t-strings** (3.14+): decomposed template literals for custom rendering |
| [`re`](re-regular-expression-operations/index.md) | Regular expression search, split, sub, and compiled patterns |
| [`difflib`](difflib-helpers-for-computing-deltas/index.md) | Sequence diffs, fuzzy matching, HTML/unified/context diff output |
| [`textwrap`](textwrap-text-wrapping-and-filling/index.md) | Paragraph wrap, dedent, indent, truncate-with-ellipsis |
| [`unicodedata`](unicodedata-unicode-database/index.md) | Unicode character properties, names, normalization (NFC/NFKC/…) |
| [`stringprep`](stringprep-internet-string-preparation/index.md) | RFC 3454 preparation tables (IDNA / internationalized identifiers) |
| [`readline`](readline-gnu-readline-interface/index.md) | GNU readline / libedit: history, completion hooks, line buffer |
| [`rlcompleter`](rlcompleter-completion-function-for-gnu-readline/index.md) | Tab completion for Python identifiers in the interactive REPL |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Simple literal formatting | f-strings or `str.format()`; see [`string`](string-common-string-operations/index.md) for the format mini-language |
| Custom template engine (SQL, HTML, CLI) | [`string.templatelib`](stringtemplatelib-support-for-template-string-literals/index.md) t-strings + your renderer |
| Extract or validate text structure | [`re`](re-regular-expression-operations/index.md); prefer `re.compile()` in hot loops |
| Compare files or suggest typos | [`difflib`](difflib-helpers-for-computing-deltas/index.md) |
| CLI help text, docstring blocks | [`textwrap`](textwrap-text-wrapping-and-filling/index.md) |
| Case-fold, compose, or inspect code points | [`unicodedata`](unicodedata-unicode-database/index.md) |
| Domain names, protocol identifiers | [`stringprep`](stringprep-internet-string-preparation/index.md) + application profile (e.g. nameprep) |
| Persistent REPL history / custom completion | [`readline`](readline-gnu-readline-interface/index.md) + [`rlcompleter`](rlcompleter-completion-function-for-gnu-readline/index.md) |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Normalize Unicode **before** comparing or hashing user text | `unicodedata.normalize('NFKC', s)` avoids visually identical but unequal strings |
| Use **raw strings** for regex patterns | Avoid doubling backslashes (`r'\d+'` not `'\\d+'`) |
| Prefer **`str` methods** when they suffice | `str.removeprefix`, `split`, `partition` are clearer and often faster than regex |
| Compile regexes used many times | `pat = re.compile(...)` amortizes parsing cost |
| Treat `readline` as **optional** | Not available on WASI, iOS, or Android; guard imports in portable tools |
| Keep diffs at **line granularity** | Pass lists of lines (often from `splitlines(keepends=True)`) to `difflib` |

```python
# Goal: pick normalization before case-insensitive identifier comparison
import unicodedata

def canonical_id(text):
    return unicodedata.normalize("NFKC", text).casefold()

assert canonical_id("Straße") == canonical_id("STRASSE")
```

```python
# Goal: wrap user-facing prose for an 80-column terminal
import textwrap

paragraph = "Python's text modules compose: normalize, match, diff, and wrap."
wrapped = textwrap.fill(paragraph, width=40)
assert all(len(line) <= 40 for line in wrapped.splitlines())
```

---

## Sections in this repo

| Module | Notes |
|--------|-------|
| [string — Common string operations](string-common-string-operations/index.md) | Constants, `Formatter`, format mini-language |
| [string.templatelib — Support for template string literals](stringtemplatelib-support-for-template-string-literals/index.md) | `Template`, `Interpolation`, t-string literals |
| [re — Regular expression operations](re-regular-expression-operations/index.md) | Patterns, flags, `Match` objects |
| [difflib — Helpers for computing deltas](difflib-helpers-for-computing-deltas/index.md) | `SequenceMatcher`, diff formats, fuzzy match |
| [textwrap — Text wrapping and filling](textwrap-text-wrapping-and-filling/index.md) | `wrap`, `fill`, `dedent`, `TextWrapper` |
| [unicodedata — Unicode Database](unicodedata-unicode-database/index.md) | UCD lookups and normalization forms |
| [stringprep — Internet String Preparation](stringprep-internet-string-preparation/index.md) | RFC 3454 table predicates and maps |
| [readline — GNU readline interface](readline-gnu-readline-interface/index.md) | History, completion, init files |
| [rlcompleter — Completion function for GNU readline](rlcompleter-completion-function-for-gnu-readline/index.md) | `Completer` for the interactive prompt |
