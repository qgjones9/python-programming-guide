# [curses.ascii — Utilities for ASCII characters](https://docs.python.org/3/library/curses.ascii.html)

The [`curses.ascii`](https://docs.python.org/3/library/curses.ascii.html) submodule supplies **ASCII classification functions** and **control-character constants** independent of locale. Unlike most of [`curses`](../curses-terminal-handling-for-character-cell-displays/index.md), it works **without a terminal** — useful in parsers, log formatters, and TUI code that must classify bytes. Full reference remains on [docs.python.org](https://docs.python.org/3/library/curses.ascii.html).

---

## Control character constants

Named constants (`NUL`, `SOH`, … `DEL`) mirror C/POSIX mnemonics for teletype-era control codes. Many are rarely used in modern UIs but appear in wire protocols and escape sequences.

| Constant | Typical meaning |
|----------|-----------------|
| `TAB` / `HT`, `LF` / `NL`, `CR` | Whitespace / line breaks |
| `ESC` | Start of escape sequences |
| `SP` | Space |
| `DEL` | Delete (0x7f) |

```python
# Goal: named constants match expected code points
import curses.ascii as a

assert a.TAB == 9
assert a.LF == 10
assert a.CR == 13
assert a.ESC == 27
assert a.SP == 32
assert a.DEL == 127
```

---

## Classification functions

Each `is*` function accepts an **int** or **single-character str** (converted via `ord()`). They test **ordinal bit patterns**, not locale-aware Unicode categories.

| Function | True when |
|----------|-----------|
| `isalnum(c)` | Alphabetic or digit |
| `isalpha(c)` | Alphabetic |
| `isdigit(c)` | `'0'`–`'9'` |
| `islower(c)` / `isupper(c)` | Case letters |
| `isspace(c)` | Space, tab, LF, CR, FF, VT |
| `iscntrl(c)` / `isctrl(c)` | Control (0x00–0x1f or 0x7f) |
| `isprint(c)` | Printable including space |
| `isgraph(c)` | Printable excluding space |
| `ispunct(c)` | Printable, not space/alnum |
| `isascii(c)` | Fits in 7-bit ASCII |
| `ismeta(c)` | Ordinal ≥ 0x80 |
| `isblank(c)` | Space or horizontal tab |
| `isxdigit(c)` | Hex digit |

```python
# Goal: classify ASCII characters
import curses.ascii as a

assert a.isalpha("Z") and a.islower("z") and not a.isdigit("A")
assert a.isdigit("7") and a.isxdigit("f")
assert a.isspace("\n") and a.isblank(" ")
assert a.isctrl("\x01") and a.iscntrl("\x1f")
assert a.isascii("~") and not a.ismeta("~")
assert a.ismeta("\x80")
```

---

## Transform helpers

| Function | Effect |
|----------|--------|
| `ascii(c)` | Low 7 bits of `c` |
| `ctrl(c)` | Control character (`c & 0x1f`) |
| `alt(c)` | Set high bit (`c \| 0x80`) |
| `unctrl(c)` | Printable char, or `^X` / `^?` form |

```python
# Goal: ctrl and unctrl for control characters
import curses.ascii as a

assert a.ctrl("G") == "\x07"  # BEL / ^G
assert a.unctrl(7) == "^G"
assert a.unctrl(127) == "^?"
assert a.unctrl(65) == "A"
assert a.unctrl(a.ESC) == "^["
```

---

## controlnames

`controlnames` is a 33-element tuple: mnemonics for control codes 0–31 plus `SP` for space.

```python
# Goal: index controlnames by control code value
import curses.ascii as a

assert a.controlnames[0] == "NUL"
assert a.controlnames[a.TAB] == "HT" or a.controlnames[9] == "HT"
assert a.controlnames[-1] == "SP"
```

---

## Related modules

| Module | Relationship |
|--------|--------------|
| [`curses`](../curses-terminal-handling-for-character-cell-displays/index.md) | Full-screen TUI; import `curses.ascii` for byte-safe checks |
| [`string`](../../text-processing-services/string-common-string-operations/index.md) | `string.digits`, `hexdigits` overlap with `isdigit` / `isxdigit` |
| [`bytes`](../../built-in-types/binary-sequence-types-bytes-bytearray-memoryview/index.md) | Often paired when parsing terminal protocols |
