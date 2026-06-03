# [string — Common string operations](https://docs.python.org/3/library/string.html)

The [`string`](https://docs.python.org/3/library/string.html) module supplies **ASCII character-set constants** and the **`Formatter` machinery** behind `str.format()`. Everyday text work usually lives on built-in [`str`](../built-in-types/text-sequence-type-str/index.md) methods and f-strings; reach for this module when you need portable character classes or a customizable formatting pipeline. Full specification remains on [docs.python.org](https://docs.python.org/3/library/string.html).

---

## String constants — [String constants](https://docs.python.org/3/library/string.html#string-constants)

These values are **not locale-dependent** (except where noted in upstream docs for `Formatter` locale features):

| Constant | Contents |
|----------|----------|
| `ascii_letters` | `ascii_lowercase` + `ascii_uppercase` |
| `ascii_lowercase` | `'abcdefghijklmnopqrstuvwxyz'` |
| `ascii_uppercase` | `'ABCDEFGHIJKLMNOPQRSTUVWXYZ'` |
| `digits` | `'0123456789'` |
| `hexdigits` | `'0123456789abcdefABCDEF'` |
| `octdigits` | `'01234567'` |
| `punctuation` | ASCII punctuation in the C locale |
| `printable` | digits + letters + punctuation + whitespace |
| `whitespace` | space, tab, LF, CR, FF, VT |

```python
# Goal: validate an ASCII identifier fragment
import string

allowed = string.ascii_letters + string.digits + "_"
token = "user_42"
assert all(ch in allowed for ch in token)
assert set(" \t\n") <= set(string.whitespace)
```

**Pitfall:** `string.printable.isprintable()` returns `False` because the constant includes whitespace—upstream notes this differs from POSIX “printable” semantics.

---

## Custom formatting — [Custom string formatting](https://docs.python.org/3/library/string.html#custom-string-formatting)

`string.Formatter` mirrors the engine used by `str.format()` and f-strings. Subclass it to change how fields are resolved, validated, or rendered—useful for template languages, debug formatters, or strict “no unused kwargs” policies.

| Method | Role |
|--------|------|
| `format(format_string, /, *args, **kwargs)` | Public entry; forwards to `vformat` |
| `vformat(format_string, args, kwargs)` | Parses fields and assembles output |
| `parse(format_string)` | Yields `(literal, field_name, format_spec, conversion)` tuples |
| `get_field(field_name, args, kwargs)` | Resolves a field to `(obj, used_key)` |
| `get_value(key, args, kwargs)` | Fetches positional or keyword argument |
| `format_field(value, format_spec)` | Calls built-in `format()` |
| `convert_field(value, conversion)` | Applies `!s`, `!r`, or `!a` |
| `check_unused_args(used_args, args, kwargs)` | Hook for unused-argument checks |

```python
# Goal: Formatter with strict keyword usage
import string

class StrictFormatter(string.Formatter):
    def check_unused_args(self, used_args, args, kwargs):
        unused = set(kwargs) - used_args
        if unused:
            raise ValueError(f"unused kwargs: {unused}")

fmt = StrictFormatter()
assert fmt.format("{name}: {value:d}", name="count", value=7) == "count: 7"
try:
    fmt.format("{x}", x=1, y=2)
except ValueError as exc:
    assert "unused kwargs" in str(exc)
else:
    raise AssertionError("expected ValueError")
```

---

## Format mini-language — [Format specification mini-language](https://docs.python.org/3/library/string.html#format-specification-mini-language)

Replacement fields use `{field[!conversion][:format_spec]}`. The **format_spec** grammar (alignment, fill, sign, width, grouping, type) is shared by `str.format()`, f-strings, `format()`, and t-string processing via [`string.templatelib`](../stringtemplatelib-support-for-template-string-literals/index.md).

| Align | Meaning |
|-------|---------|
| `<` | Left (default for most types) |
| `>` | Right (default for numbers) |
| `^` | Centered |
| `=` | Pad after sign, before digits (numbers only) |

| Type | Typical use |
|------|-------------|
| `s` | String (default for str) |
| `d` | Decimal integer |
| `f` / `F` | Fixed-point float |
| `g` / `G` | General float (drops trailing zeros) |
| `x` / `X` | Hex integer |
| `n` | Locale-aware number (needs `locale` setup) |
| `%` | Multiply by 100 and show `%` |

```python
# Goal: alignment, grouping, and conversions without an f-string
assert "{:<10}".format("left") == "left      "
assert "{:>10}".format("right") == "     right"
assert "{:*^10}".format("mid") == "***mid****"
assert "{:,}".format(1234567) == "1,234,567"
assert "{0!r}".format("hi") == "'hi'"
```

---

## Practical patterns and pitfalls

| Pattern | Guidance |
|---------|----------|
| Character class tests | `all(c in string.hexdigits for c in s)` for hex tokens |
| Safe user templates | Subclass `Formatter` and override `get_value` to whitelist keys |
| Prefer f-strings in app code | Use `string.Formatter` when you need **programmable** format parsing |
| Doubled braces | `{{` and `}}` emit literal braces in format strings |
| Dynamic width/precision | Nested fields `{width}` inside format_spec are substituted first |

```python
# Goal: parse a format string into literal and field spans
import string

parts = list(string.Formatter().parse("Hello {name}!"))
assert parts[0][0] == "Hello "
assert parts[0][1] == "name"
assert parts[1][0] == "!"
assert parts[1][1] is None  # trailing literal
```

For narrative examples of positional, named, and numeric formatting, see upstream [Format examples](https://docs.python.org/3/library/string.html#format-examples).
