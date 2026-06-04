# [gettext — Multilingual internationalization services](https://docs.python.org/3/library/gettext.html)

The [`gettext`](https://docs.python.org/3/library/gettext.html) module implements **internationalization (I18N)** and **localization (L10N)** for Python programs: mark user-facing strings once, ship translated **message catalogs**, and resolve the right language at runtime via GNU **`.mo`** files. It offers both the **GNU gettext C-style API** (process-wide) and a **class-based API** (recommended for modules and multi-language apps). Canonical reference: [gettext.html](https://docs.python.org/3/library/gettext.html).

---

## Purpose

| Concern | Role of `gettext` |
|---------|-------------------|
| I18N | Make the program translation-aware (mark strings, extract catalogs) |
| L10N | Load language-specific `.mo` files and return translated Unicode strings |
| Catalog format | Parse GNU gettext binary catalogs via `GNUTranslations` |
| Fallback | `NullTranslations` passes messages through when no catalog exists |

---

## GNU gettext API — [GNU gettext API](https://docs.python.org/3/library/gettext.html#gnu-gettext-api)

The module-level functions affect **global** domain and locale directory bindings—appropriate for a **single-language application** driven by the user’s environment (`LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, `LANG`).

| Function | Behavior |
|----------|----------|
| `bindtextdomain(domain, localedir=None)` | Bind domain to directory; search path `localedir/lang/LC_MESSAGES/domain.mo` |
| `textdomain(domain=None)` | Get/set current global domain |
| `gettext(message)` | Translate `message` in current domain (usually aliased as `_`) |
| `dgettext(domain, message)` | Translate in a specific domain |
| `ngettext(singular, plural, n)` | Plural-aware lookup using catalog plural formula |
| `dngettext(domain, singular, plural, n)` | Plural lookup in named domain |
| `pgettext` / `dpgettext` / `npgettext` / `dnpgettext` | Context-qualified variants (since 3.8) |

`dcgettext()` from GNU gettext is **not implemented** in Python.

```python
# Goal: global API with NullTranslations behavior when no .mo file is present
import gettext

gettext.textdomain("demo")
_ = gettext.gettext
assert _("This is a translatable string.") == "This is a translatable string."
```

---

## Class-based API — [Class-based API](https://docs.python.org/3/library/gettext.html#class-based-api)

Prefer this API for **libraries** and apps that **switch languages** without relying on process-wide state.

| Function / class | Behavior |
|------------------|----------|
| `find(domain, localedir=None, languages=None, all=False)` | Standard `.mo` search; honors `LANGUAGE` et al. when `languages` omitted |
| `translation(domain, localedir=None, languages=None, class_=None, fallback=False)` | Return cached `GNUTranslations` or `NullTranslations` if `fallback=True` |
| `install(domain, localedir=None, *, names=None)` | Install `_()` into `builtins` (keyword-only `names` since 3.11) |
| `Catalog(domain, localedir)` | Alias for `translation()` (GNOME compatibility) |

```python
# Goal: explicit translation object without touching builtins
import gettext

t = gettext.translation("mymodule", fallback=True)
_ = t.gettext
assert _("writing a log message") == "writing a log message"
```

```python
# Goal: find() returns None when no catalog exists on this machine
import gettext

path = gettext.find("nonexistent-domain-xyz", languages=["en"])
assert path is None or path.endswith(".mo")
```

---

### The NullTranslations class — [The NullTranslations class](https://docs.python.org/3/library/gettext.html#the-nulltranslations-class)

Base implementation: returns originals, supports **fallback chains** via `add_fallback()`.

| Method | Behavior |
|--------|----------|
| `gettext(message)` | Return `message` or delegate to fallback |
| `ngettext(singular, plural, n)` | `singular` if `n == 1` else `plural` |
| `pgettext` / `npgettext` | Context-aware pass-through |
| `install(names=None)` | Bind `_()` (and optional names) into builtins—avoid in libraries |

```python
import gettext

primary = gettext.NullTranslations()
fallback = gettext.NullTranslations()
primary.add_fallback(fallback)
assert primary.ngettext("one file", "%d files", 1) == "one file"
assert primary.ngettext("one file", "%d files", 3) == "%d files"
```

---

### The GNUTranslations class — [The GNUTranslations class](https://docs.python.org/3/library/gettext.html#the-gnutranslations-class)

Parses GNU **`.mo`** files (big- or little-endian). Metadata from the empty-string entry populates `info()`; `Content-Type` sets charset (messages are Unicode strings in Python 3). Invalid magic or version raises `OSError`.

Plural lookups use the **`Plural-Forms`** expression from the catalog header. Message ids and results are **Unicode**, not bytes.

```python
# Goal: ngettext without a real .mo file uses NullTranslations plural rules
import gettext

cat = gettext.NullTranslations()
n = 3
msg = cat.ngettext(
    "There is %(num)d file in this directory",
    "There are %(num)d files in this directory",
    n,
) % {"num": n}
assert "files" in msg and "3" in msg
```

---

### Solaris message catalog support — [Solaris message catalog support](https://docs.python.org/3/library/gettext.html#solaris-message-catalog-support)

Solaris `.mo` format is **unsupported** (undocumented binary layout).

---

### The Catalog constructor — [The Catalog constructor](https://docs.python.org/3/library/gettext.html#the-catalog-constructor)

`gettext.Catalog(domain, localedir)` is an alias for `translation()`. Mapping-style catalog access from older GNOME bindings is **not** supported.

---

## Internationalizing your programs and modules — [Internationalizing your programs and modules](https://docs.python.org/3/library/gettext.html#internationalizing-your-programs-and-modules)

Typical pipeline:

1. Mark translatable strings in source (`_('...')` or `N_('...')` for deferred).
2. Run **xgettext**, **pygettext**, or **pybabel extract** to build `.po` catalogs.
3. Translators fill `.po` files; **msgfmt** (or `pybabel compile`) produces `.mo` binaries.
4. At runtime, load catalogs with `translation()` or `install()`.

Tools: GNU **xgettext**, Python **pygettext.py** / **msgfmt.py**, [Babel](https://babel.pocoo.org/) **pybabel**.

---

### Localizing your module — [Localizing your module](https://docs.python.org/3/library/gettext.html#localizing-your-module)

Do **not** use the GNU global API or `install()` in importable modules—it mutates builtins for the whole process.

```python
# Goal: module-scoped _ without builtins side effects
import gettext

t = gettext.translation("spam", "/usr/share/locale", fallback=True)
_ = t.gettext
assert _("module message") == "module message"
```

---

### Localizing your application — [Localizing your application](https://docs.python.org/3/library/gettext.html#localizing-your-application)

In the main driver, `gettext.install('myapplication')` or `gettext.install('myapplication', '/usr/share/locale')` exposes `_()` everywhere.

```python
# Goal: simulate install by binding _ in a namespace (avoid builtins in tests)
import gettext

ns = {}
t = gettext.translation("myapplication", fallback=True)
ns["_"] = t.gettext
assert ns["_"]("This string will be translated.") == "This string will be translated."
```

---

### Changing languages on the fly — [Changing languages on the fly](https://docs.python.org/3/library/gettext.html#changing-languages-on-the-fly)

Create one `translation()` per language and call `install()` on the active instance when the user switches.

```python
import gettext

lang_en = gettext.translation("myapplication", languages=["en"], fallback=True)
lang_fr = gettext.translation("myapplication", languages=["fr"], fallback=True)
lang_en.install()
assert _("hello") == "hello"
lang_fr.install()
# Without .mo files both return the source string; pattern is the switching API
assert _("hello") == "hello"
```

---

### Deferred translations — [Deferred translations](https://docs.python.org/3/library/gettext.html#deferred-translations)

Mark strings at definition time, translate at use time:

| Pattern | Technique |
|---------|-----------|
| Dummy `_` then `del _` | Temporary override until catalogs load |
| `N_(msg)` marker | Extract with `xgettext -k N_`; translate with `_()` in the loop |

Extractors only see **string literals** inside `_()` / `N_()`—not variables.

```python
# Goal: deferred translation with a no-op marker then real _
def N_(message):
    return message

animals = [N_("mollusk"), N_("albatross"), N_("rat")]
_ = lambda s: s.upper()  # stand-in for catalog lookup
printed = [_(a) for a in animals]
assert printed == ["MOLLUSK", "ALBATROSS", "RAT"]
```

```python
# Goal: pgettext separates identical English words by context (API surface)
import gettext

t = gettext.NullTranslations()
assert t.pgettext("menu", "right") == "right"
assert t.pgettext("direction", "right") == "right"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Wrap only **user-visible** strings | File names, protocol tokens, and format codes stay out of catalogs |
| Keep `%(name)s` **Python formatting** in translated strings | Translators can reorder placeholders safely |
| Ship `.mo` under `share/locale/.../LC_MESSAGES/` | Matches `find()` / `bindtextdomain` layout |
| Test with `fallback=True` in CI without catalogs | Confirms code paths before translations land |
| Use **context** (`pgettext`) for ambiguous English | One msgid, multiple translations per context |

---

## See also

- [Internationalization hub](../index.md)
- [`locale` module](../locale-internationalization-services/index.md) — POSIX formatting and C gettext bridge
- [GNU gettext manual](https://www.gnu.org/software/gettext/manual/gettext.html)
