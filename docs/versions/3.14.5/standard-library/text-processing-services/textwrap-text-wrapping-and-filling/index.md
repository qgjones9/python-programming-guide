# [textwrap — Text wrapping and filling](https://docs.python.org/3/library/textwrap.html)

The [`textwrap`](https://docs.python.org/3/library/textwrap.html) module wraps paragraphs to a column width, dedents indented triple-quoted blocks, adds line prefixes, and truncates with an ellipsis placeholder. Convenience functions delegate to [`TextWrapper`](https://docs.python.org/3/library/textwrap.html#textwrap.TextWrapper); reuse one wrapper instance when processing many strings. Full option reference remains on [docs.python.org](https://docs.python.org/3/library/textwrap.html).

---

## Module-level functions

| Function | Returns | Typical use |
|----------|---------|-------------|
| `wrap(text, width=70, ...)` | `list[str]` lines without trailing `\n` | Build custom output |
| `fill(text, width=70, ...)` | Single `str` with `\n` between lines | Help text, log messages |
| `shorten(text, width, ...)` | Collapsed + truncated string | UI snippets, summaries |
| `dedent(text)` | String with common leading whitespace removed | Docstrings, embedded YAML |
| `indent(text, prefix, predicate=None)` | Lines with selective prefix | Block quoting, nesting |

```python
# Goal: wrap and fill a paragraph
import textwrap

text = "Python textwrap breaks on spaces and hyphens when possible."
lines = textwrap.wrap(text, width=20)
assert all(len(line) <= 20 for line in lines)
filled = textwrap.fill(text, width=20)
assert filled.count("\n") == len(lines) - 1
```

```python
# Goal: shorten with a custom placeholder
import textwrap

long = "Hello  world! This keeps going."
assert textwrap.shorten(long, width=12) == "Hello [...]"
assert textwrap.shorten(long, width=11) == "Hello [...]"
assert textwrap.shorten(long, width=10, placeholder="...") == "Hello..."
assert textwrap.shorten("Hello  world!", width=12) == "Hello world!"
```

---

## dedent and indent

`dedent` removes **common leading whitespace** per line; tabs and spaces are not treated as equal when measuring the shared prefix. Since 3.14, blank lines that contain only whitespace normalize to a single newline in the output.

`indent` adds `prefix` to lines selected by `predicate` (default: non-whitespace-only lines).

```python
# Goal: dedent an indented triple-quoted block
import textwrap

block = """\
    alpha
      beta
    """
dedented = textwrap.dedent(block)
assert dedented.startswith("alpha")
assert "  beta" in dedented  # relative indent preserved
```

```python
# Goal: prefix every non-empty line
import textwrap

sample = "hello\n\n \nworld"
indented = textwrap.indent(sample, "> ")
assert indented.splitlines()[0] == "> hello"
assert indented.splitlines()[-1] == "> world"
```

---

## TextWrapper options

| Attribute | Default | Effect |
|-----------|---------|--------|
| `width` | `70` | Maximum line length |
| `expand_tabs` | `True` | Expand tabs before wrapping |
| `tabsize` | `8` | Tab stop width when expanding |
| `replace_whitespace` | `True` | Collapse whitespace runs to single spaces |
| `drop_whitespace` | `True` | Strip leading/trailing space on wrapped lines |
| `initial_indent` | `''` | Prefix for first line only |
| `subsequent_indent` | `''` | Prefix for following lines |
| `break_long_words` | `True` | Split words longer than `width` |
| `break_on_hyphens` | `True` | Prefer breaks after hyphens |
| `max_lines` | `None` | Cap output lines; append `placeholder` |
| `placeholder` | `' [...]'` | Suffix when truncated |
| `fix_sentence_endings` | `False` | English-centric double-space after `.?!` |

```python
# Goal: reuse TextWrapper for batch processing
import textwrap

wrapper = textwrap.TextWrapper(
    width=30,
    initial_indent="  ",
    subsequent_indent="    ",
)
a = wrapper.fill("First sentence. Second sentence here.")
b = wrapper.fill("Another paragraph entirely.")
assert a.startswith("  ")
assert "    " in a
assert len(b) > 0
```

---

## Best practices and pitfalls

| Practice | Why |
|----------|-----|
| Split multi-paragraph input | `wrap`/`fill` operate on **one paragraph**; use `splitlines()` or blank-line splits |
| Reuse `TextWrapper` in loops | Module functions construct a new wrapper each call |
| Set `replace_whitespace=False` carefully | Newlines can appear mid-line and produce odd output |
| Use `shorten` for UI caps | Whitespace is collapsed before measuring width |
| Avoid `fix_sentence_endings` for i18n | Heuristic is English-specific and imperfect |

**Pitfall:** `shorten` ignores `tabsize`, `expand_tabs`, and related flags—whitespace is collapsed before wrapping logic runs.
