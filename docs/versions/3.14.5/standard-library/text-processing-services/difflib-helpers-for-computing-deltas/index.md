# [difflib — Helpers for computing deltas](https://docs.python.org/3/library/difflib.html)

[`difflib`](https://docs.python.org/3/library/difflib.html) compares **sequences** (usually lines of text) and produces human-readable or machine-readable deltas. Use it for test failure output, merge tools, “did you mean?” suggestions, and HTML side-by-side diffs. For directory comparison see [`filecmp`](../../file-and-directory-access/filecmp-file-and-directory-comparisons/index.md). Full API reference remains on [docs.python.org](https://docs.python.org/3/library/difflib.html).

---

## SequenceMatcher — [SequenceMatcher](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher)

Flexible comparator for hashable sequence elements. The Ratcliff–Obershelp-style algorithm finds long contiguous matches, then recurses on left/right remainders—fast and visually pleasing, but **not guaranteed minimal edit distance**.

| Method | Role |
|--------|------|
| `ratio()` | Similarity in [0, 1] |
| `quick_ratio()` | Upper bound, cheaper |
| `real_quick_ratio()` | Cheapest upper bound |
| `get_matching_blocks()` | Non-overlapping `(i, j, n)` triples |
| `get_opcodes()` | Tag triples: `replace`, `delete`, `insert`, `equal` |

The **`autojunk`** heuristic (default `True`) treats very frequent lines as junk in long sequences (>200 items, >1% duplicates).

```python
# Goal: similarity ratio between token lists
import difflib

sm = difflib.SequenceMatcher(None, "abcd", "abxcd")
assert sm.ratio() > 0.7
blocks = sm.get_matching_blocks()
assert blocks[-1].size == 0  # sentinel block
```

---

## Differ line codes — [Differ](https://docs.python.org/3/library/difflib.html#difflib.Differ)

`Differ.compare(a, b)` yields lines prefixed with two-character codes:

| Code | Meaning |
|------|---------|
| `'  '` | Present in both sequences |
| `'- '` | Only in first sequence |
| `'+ '` | Only in second sequence |
| `'? '` | Intraline hint (not in either original) |

```python
# Goal: unified-style delta with ndiff
import difflib

a = "one\ntwo\nthree\n".splitlines(keepends=True)
b = "ore\ntree\nemu\n".splitlines(keepends=True)
delta = list(difflib.ndiff(a, b))
assert any(line.startswith("- one") for line in delta)
assert any(line.startswith("+ tree") for line in delta)
```

Use [`restore()`](https://docs.python.org/3/library/difflib.html#difflib.restore) to rebuild either side from an `ndiff` delta.

---

## Diff output formats

| Function | Format | Typical consumer |
|----------|--------|------------------|
| `unified_diff(a, b, ...)` | Unified patch (`---`, `+++`, `@@`) | `patch`, code review tools |
| `context_diff(a, b, ...)` | Context diff (`***`, `---`) | Legacy tools |
| `HtmlDiff().make_file(...)` | Full HTML page | Browser viewing |
| `HtmlDiff().make_table(...)` | HTML table fragment | Embedding in apps |

Pass **`splitlines(keepends=True)`** lists when you need newlines preserved for `writelines`.

```python
# Goal: unified diff generator
import difflib

before = ["alpha\n", "beta\n"]
after = ["alpha\n", "gamma\n"]
diff = list(difflib.unified_diff(
    before, after, fromfile="old.txt", tofile="new.txt", lineterm=""
))
text = "".join(diff)
assert "--- old.txt" in text or "---" in text
assert "beta" in text and "gamma" in text
```

---

## Fuzzy matching — [get_close_matches](https://docs.python.org/3/library/difflib.html#difflib.get_close_matches)

Returns up to **`n`** choices from **`possibilities`** with similarity ≥ **`cutoff`** (default `0.6`), best first.

```python
# Goal: typo-tolerant command lookup
import difflib

choices = ["apple", "apply", "ape", "apex"]
matches = difflib.get_close_matches("appel", choices, n=2, cutoff=0.6)
assert set(matches) <= set(choices)
assert "apple" in matches or "apply" in matches
assert len(matches) == 2
```

---

## Best practices and pitfalls

| Practice | Why |
|----------|-----|
| Compare **lines**, not whole files | `SequenceMatcher` on giant single strings is slow and noisy |
| Tune **`cutoff`** for suggestions | Lower values admit weak matches |
| Disable **`autojunk`** for repetitive logs | Repetition may be meaningful, not noise |
| Escape HTML in **`fromdesc` / `todesc`** | `HtmlDiff` treats descriptions as raw HTML |
| Materialize generators when re-reading | `unified_diff` returns a generator—consume once or `list()` it |

**Pitfall:** `'? '` intraline hint lines can mislead when whitespace differs—treat them as hints, not source text.

```python
# Goal: restore original sequences from ndiff output
import difflib

a = "one\ntwo\n".splitlines(keepends=True)
b = "ore\ntwo\n".splitlines(keepends=True)
delta = list(difflib.ndiff(a, b))
assert "".join(difflib.restore(delta, 1)) == "".join(a)
assert "".join(difflib.restore(delta, 2)) == "".join(b)
```
