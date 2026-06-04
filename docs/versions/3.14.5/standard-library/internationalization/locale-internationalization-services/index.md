# [locale — Internationalization services](https://docs.python.org/3/library/locale.html)

The [`locale`](https://docs.python.org/3/library/locale.html) module exposes the **POSIX locale database**: collation order, numeric and monetary formatting, time formats, and message-catalog locale categories—without hard-coding country rules in application logic. It is built on the **`_locale`** C extension when available. Canonical reference: [locale.html](https://docs.python.org/3/library/locale.html).

---

## Purpose

| Concern | Role of `locale` |
|---------|------------------|
| Cultural formatting | Decimal point, thousands separators, currency symbols |
| Collation | Locale-aware string ordering via `strcoll` / `strxfrm` |
| Discovery | `getlocale`, `getencoding`, `normalize` for locale names |
| C interoperability | Thin wrappers around C library `gettext` where needed |

Python’s own string operations use **Unicode semantics**; `LC_CTYPE` does not switch `str.lower()` to locale rules. Numeric helpers (`atof`, `format_string`, …) are the supported way to parse/format numbers per locale.

---

## Core API

### `locale.Error`

Raised when `setlocale()` receives an unrecognized locale name.

### `setlocale(category, locale=None)` — [setlocale](https://docs.python.org/3/library/locale.html#locale.setlocale)

| `locale` argument | Effect |
|-------------------|--------|
| String (e.g. `'de_DE.UTF-8'`) | Set category; return new setting |
| `('',)` or `''` | User’s default from environment (`LANG`, …) |
| `'C'` | Portable C locale |
| `(lang, encoding)` tuple | Normalized via aliasing engine |
| `None` / omitted | Return current setting for `category` |

**Not thread-safe** on most systems. Typical app startup:

```python
import locale

locale.setlocale(locale.LC_ALL, "")
```

```python
# Goal: save/restore locale around a C-locale numeric block
import locale

saved = locale.setlocale(locale.LC_ALL)
try:
    locale.setlocale(locale.LC_ALL, "C")
    assert locale.setlocale(locale.LC_NUMERIC) in ("C", "POSIX", saved)
finally:
    locale.setlocale(locale.LC_ALL, saved)
```

---

### `localeconv()` — [localeconv](https://docs.python.org/3/library/locale.html#locale.localeconv)

Returns a dict of **local conventions** (`decimal_point`, `thousands_sep`, `grouping`, currency fields, sign position codes, …). Values may be `locale.CHAR_MAX` when unspecified.

`currency()` requires a **non-C** monetary locale. Since 3.7, the function may temporarily adjust `LC_CTYPE` when numeric strings are non-ASCII—affects other threads.

```python
import locale

locale.setlocale(locale.LC_ALL, "C")
conv = locale.localeconv()
assert conv["decimal_point"] == "."
assert isinstance(conv["grouping"], (str, list))
```

---

### `nl_langinfo(option)` — [nl_langinfo](https://docs.python.org/3/library/locale.html#locale.nl_langinfo)

Platform-dependent locale strings: `CODESET`, `D_T_FMT`, day/month names (`DAY_1`…`MON_12`), `RADIXCHAR`, `YESEXPR` / `NOEXPR`, era formats, etc.

**Note:** `DAY_1` is **Sunday** (US convention), not ISO 8601 Monday-first.

Since 3.14, may temporarily set `LC_CTYPE` when the result is non-ASCII.

```python
import locale

locale.setlocale(locale.LC_ALL, "C")
# CODESET may be empty under C on some platforms
codeset = locale.nl_langinfo(locale.CODESET)
assert codeset is None or isinstance(codeset, str)
```

---

### Locale discovery and encoding

| Function | Behavior |
|----------|----------|
| `getdefaultlocale(envvars)` | **Deprecated** 3.11, removed 3.15 — use `getlocale` / `getencoding` |
| `getlocale(category=LC_CTYPE)` | `(language, encoding)` tuple; `C` → `(None, None)` |
| `getpreferredencoding(do_setlocale=True)` | Guess for text; `'utf-8'` on Android / UTF-8 mode |
| `getencoding()` | **3.11+** — current `LC_CTYPE` encoding; ignores UTF-8 mode |
| `normalize(localename)` | Name suitable for `setlocale()` |

```python
import locale

locale.setlocale(locale.LC_ALL, "C")
lang, enc = locale.getlocale()
assert lang is None and enc is None
```

```python
import locale

normalized = locale.normalize("en_US.UTF-8")
assert "en" in normalized.lower() or normalized == "en_US.UTF-8"
```

---

### String collation and transforms

| Function | Use |
|----------|-----|
| `strcoll(s1, s2)` | Compare per `LC_COLLATE` (-1, 0, 1) |
| `strxfrm(s)` | Transform for repeated comparisons |

```python
import locale

locale.setlocale(locale.LC_ALL, "C")
assert locale.strcoll("abc", "abd") < 0
assert locale.strxfrm("abc") <= locale.strxfrm("abd")
```

---

### Numeric and monetary formatting

| Function | Use |
|----------|-----|
| `format_string(format, val, grouping=False, monetary=False)` | `%`-style format with locale separators |
| `currency(val, symbol=True, grouping=False, international=False)` | Monetary string per `LC_MONETARY` |
| `str(float)` | Like built-in `str(float)` but locale decimal point |
| `delocalize(string)` | Strip locale formatting → normalized number string (**3.5+**) |
| `localize(string, grouping=False, monetary=False)` | Opposite of `delocalize` (**3.10+**) |
| `atof(string, func=float)` | Parse float per `LC_NUMERIC` |
| `atoi(string)` | Parse int per `LC_NUMERIC` |

```python
import locale

locale.setlocale(locale.LC_ALL, "C")
assert locale.format_string("%.2f", 1234.5) == "1234.50"
assert locale.delocalize("1234.50") == "1234.50"
assert locale.atof("3.14") == 3.14
assert locale.atoi("42") == 42
```

```python
# Goal: localize/delocalize round-trip under C locale
import locale

locale.setlocale(locale.LC_ALL, "C")
raw = locale.localize("1234.5")
assert locale.delocalize(raw) == "1234.5"
```

---

## Locale categories — [Locale categories](https://docs.python.org/3/library/locale.html#locale-categories)

| Constant | Affects |
|----------|---------|
| `LC_CTYPE` | Character classification / **text encoding** (PEP 538/540 interactions) |
| `LC_COLLATE` | `strcoll`, `strxfrm` |
| `LC_TIME` | `time.strftime` conventions |
| `LC_MONETARY` | `localeconv` currency fields, `currency()` |
| `LC_NUMERIC` | `format_string`, `atof`, `atoi`, locale `str()` |
| `LC_MESSAGES` | OS messages (`os.strerror`); **not on Windows** |
| `LC_ALL` | All categories atomically |
| `CHAR_MAX` | Sentinel in `localeconv()` values |

```python
import locale

assert locale.LC_ALL != locale.LC_NUMERIC
assert locale.CHAR_MAX >= 0
```

---

## Background, details, hints, tips and caveats — [Background](https://docs.python.org/3/library/locale.html#background-details-hints-tips-and-caveats)

| Topic | Guidance |
|-------|----------|
| Startup locale | Process starts in **`C`** except `LC_CTYPE` encoding may follow user preference |
| `setlocale` in libraries | Avoid—side effect on entire program and other threads |
| Thread safety | Save/restore is costly; prefer leaving locale alone after initial setup |
| Unicode text | Case fold and classes use Unicode/code point rules, not locale `ctype` |
| Numeric ops | Use `locale.atof` / `format_string` when locale matters—not bare `float()` on localized strings |

---

## Locale names — [Locale names](https://docs.python.org/3/library/locale.html#locale-names)

Platform-specific strings. POSIX form:

```text
language ["_" territory] ["." charset] ["@" modifier]
```

Windows supports **BCP 47** tags (`en-US`, script subtags) and legacy display names (`English_United States.1252`). The **`C`** locale is always available.

```python
import locale

# normalize accepts many spellings; result is platform-specific
name = locale.normalize("C")
assert name  # non-empty string
```

---

## For extension writers and programs that embed Python — [For extension writers](https://docs.python.org/3/library/locale.html#for-extension-writers-and-programs-that-embed-python)

Extension modules should **not** call `setlocale()` except to read state. Embedding apps that must isolate locale can omit the `_locale` built-in module from their build.

---

## Access to message catalogs — [Access to message catalogs](https://docs.python.org/3/library/locale.html#access-to-message-catalogs)

`locale.gettext`, `locale.dgettext`, `locale.dcgettext`, `locale.textdomain`, `locale.bindtextdomain`, and `locale.bind_textdomain_codeset` wrap the **C library gettext** (binary catalog format). Python applications should normally use the **[`gettext` module](../gettext-multilingual-internationalization-services/index.md)** instead—except when linking C libraries that call C `gettext` internally.

---

## Best practices

| Practice | Why |
|----------|-----|
| Set locale **once** at application entry | Repeated changes break threads and third-party code |
| Use **`getencoding()`** (3.11+) for explicit encoding | Clearer than deprecated `getdefaultlocale` |
| Format numbers for display with **`format_string` / `currency`** | Built-in `format()` ignores `LC_NUMERIC` |
| Keep business logic in **`C` or UTF-8 locale** in libraries | Predictable parsing in tests and CI |
| Pair with **`gettext`** for translated prose | `locale` does not translate arbitrary application strings |

---

## See also

- [Internationalization hub](../index.md)
- [`gettext` module](../gettext-multilingual-internationalization-services/index.md)
- [PEP 538](https://peps.python.org/pep-0538/) — legacy locale coercion
- [PEP 540](https://peps.python.org/pep-0540/) — UTF-8 mode
