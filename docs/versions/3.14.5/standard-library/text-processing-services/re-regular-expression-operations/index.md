# [re — Regular expression operations](https://docs.python.org/3/library/re.html)

The [`re`](https://docs.python.org/3/library/re.html) module implements Perl-style regular expressions for **`str`** and **`bytes`** patterns. Module-level functions (`match`, `search`, `findall`, `sub`, …) are shortcuts; [`re.compile()`](https://docs.python.org/3/library/re.html#re.compile) returns a reusable pattern object with the same methods. Full syntax and flag reference remain on [docs.python.org](https://docs.python.org/3/library/re.html); see also the [Regular expression HOWTO](https://docs.python.org/3/howto/regex.html).

---

## Pattern and string types

| Rule | Detail |
|------|--------|
| Same-type pairing | Unicode `str` patterns match `str` text; `bytes` patterns match `bytes` |
| Raw strings | Prefer `r'\d+'` so backslashes are not Python-escaped |
| Compiled patterns | Cache and tune flags once; call `.search`, `.sub`, etc. on the object |

```python
# Goal: compile once, search many times
import re

email_local = re.compile(r"^[A-Za-z0-9._%+-]+$")
assert email_local.search("user.name+tag")
assert not email_local.search("bad name")
```

---

## Core functions — [Module Contents](https://docs.python.org/3/library/re.html#module-contents)

| Function / method | Anchoring | Returns |
|-------------------|-----------|---------|
| `re.match(pattern, string)` | Start of string only | `Match` or `None` |
| `re.search(pattern, string)` | Anywhere in string | `Match` or `None` |
| `re.fullmatch(pattern, string)` | Entire string must match | `Match` or `None` |
| `re.findall(pattern, string)` | All non-overlapping matches | `list[str]` or list of tuples |
| `re.finditer(pattern, string)` | Iterator of matches | `Iterator[Match]` |
| `re.sub(pattern, repl, string, count=0)` | Replace matches | New string |
| `re.split(pattern, string, maxsplit=0)` | Split on matches | `list[str]` |

```python
# Goal: extract, replace, and split with regex
import re

text = "Order 42: 3 items, total $12.50"
nums = re.findall(r"\d+", text)
assert nums == ["42", "3", "12", "50"]

masked = re.sub(r"\$\d+\.\d+", "$*.**", text)
assert "$*.**" in masked

parts = re.split(r"[:,]\s*", "a: b, c", maxsplit=1)
assert parts[0] == "a" and parts[1].startswith("b")
```

---

## Match objects

| Attribute / method | Role |
|--------------------|------|
| `group()` / `group(0)` | Whole match |
| `group(n)` / `group('name')` | Capturing group by index or name |
| `groups()` | Tuple of all groups except group 0 |
| `groupdict()` | Named groups as a dict |
| `start()` / `end()` / `span()` | Slice positions in source string |

```python
# Goal: named groups and spans
import re

pat = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
m = pat.search("born 1999-07-06 in NYC")
assert m.group("year") == "1999"
assert m.span("month") == (10, 12)
assert m.groupdict()["day"] == "06"
```

---

## Flags — [Module Contents](https://docs.python.org/3/library/re.html#re.A)

| Flag | Effect |
|------|--------|
| `re.I` / `IGNORECASE` | Case-insensitive matching |
| `re.M` / `MULTILINE` | `^` / `$` match line boundaries |
| `re.S` / `DOTALL` | `.` matches newline |
| `re.X` / `VERBOSE` | Insignificant whitespace and `#` comments in pattern |
| `re.A` / `ASCII` | `\w`, `\d`, `\s` ASCII-only (str patterns) |
| `re.U` / `UNICODE` | Unicode categories for `\w`, `\d`, `\s` (default on str) |

```python
# Goal: multiline ^ anchor and verbose pattern
import re

log = "ERROR line one\nINFO line two\nERROR line three"
errors = re.findall(r"^ERROR.*$", log, flags=re.MULTILINE)
assert len(errors) == 2

verbose = re.compile(r"""
    \d{3}   # area
    -?\d{3} # exchange
    -?\d{4} # subscriber
""", re.VERBOSE)
assert verbose.fullmatch("555-123-4567")
```

---

## Best practices and pitfalls

| Practice | Why |
|----------|-----|
| Prefer **`search`** over **`match`** unless you truly need start anchoring | `match` misses valid mid-string hits |
| Use **non-capturing** `(?:...)` when you do not need groups | Fewer tuple returns from `findall` |
| Watch **greedy** quantifiers | Add `?` for non-greedy (`*?`, `+?`) when needed |
| Escape user input | `re.escape(user_text)` before embedding in a pattern |
| Consider **`str` methods** first | `removeprefix`, `split`, `partition` are simpler for fixed delimiters |

**Pitfalls:**

- Mixing `str` and `bytes` raises `TypeError`.
- Invalid escape sequences in ordinary string literals trigger `SyntaxWarning` (future `SyntaxError`)—use raw strings.
- `re.sub` with a callable receives a `Match` object; return the replacement string from the callback.

```python
# Goal: callback replacement with Match groups
import re

def bump(m):
    return m.group(0).replace(m.group(1), str(int(m.group(1)) + 1))

assert re.sub(r"version=(\d+)", bump, "version=3") == "version=4"
```

For advanced needs (recursive patterns, fuzzy Unicode classes), evaluate the third-party [`regex`](https://pypi.org/project/regex/) package, which mirrors much of the `re` API.
