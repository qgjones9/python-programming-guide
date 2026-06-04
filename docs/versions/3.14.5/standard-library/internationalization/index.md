# [Internationalization](https://docs.python.org/3/library/i18n.html)

The **Internationalization** chapter of the Python standard library helps programs stay **language-independent** while still presenting messages and formatted output that match a user’s locale. [`gettext`](gettext-multilingual-internationalization-services/index.md) handles **translated message catalogs** (GNU `.mo` files); [`locale`](locale-internationalization-services/index.md) exposes the **POSIX locale database** for collation, numeric formatting, and time conventions. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/i18n.html); this hub orients you to each module and when to combine them.

Related material: environment variables such as `LANG` and `LANGUAGE` (also used by gettext’s catalog search), [`time`](../generic-operating-system-services/time-access-and-conversions/index.md) for `strftime` with `LC_TIME`, and third-party tooling such as [Babel](https://babel.pocoo.org/) for extracting translatable strings from Python sources.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`gettext`](gettext-multilingual-internationalization-services/index.md) | Mark strings for translation, load `.mo` catalogs, plural forms, context-aware lookups |
| [`locale`](locale-internationalization-services/index.md) | `setlocale`, `localeconv`, locale-aware number/currency formatting and collation |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| User-visible strings in another natural language | [`gettext`](gettext-multilingual-internationalization-services/index.md) — mark with `_()`, ship `.po`/`.mo` catalogs |
| Decimal separator, thousands grouping, currency layout | [`locale`](locale-internationalization-services/index.md) — `format_string`, `currency`, `localeconv` |
| Sort filenames or words per local alphabet | [`locale`](locale-internationalization-services/index.md) — `strcoll` / `strxfrm` under `LC_COLLATE` |
| Switch UI language at runtime without restarting | [`gettext`](gettext-multilingual-internationalization-services/index.md) — multiple `translation()` instances, `install()` per language |
| REPL/library module that must not touch builtins | [`gettext`](gettext-multilingual-internationalization-services/index.md) — module-local `_ = t.gettext`, not `gettext.install()` |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Use **gettext for messages**, **locale for formats** | Mixing concerns makes testing harder; gettext catalogs do not replace `LC_NUMERIC` |
| Call `locale.setlocale(locale.LC_ALL, '')` once at app startup if needed | Frequent `setlocale` is expensive and not thread-safe on many platforms |
| Never call `gettext.install()` inside **reusable libraries** | It patches builtins globally and affects importers |
| Extract strings with **xgettext/pybabel** (`-k` for custom markers like `N_`) | Deferred translation and dynamic `_()` args are invisible to extractors |
| Prefer **class-based gettext API** when languages change on the fly | GNU module-level API is global and monolingual per process |
| Treat **`getdefaultlocale()` as legacy** | Deprecated since 3.11; use `getlocale()` / `getencoding()` instead |

```python
# Goal: gettext for messages, locale left at C for predictable numeric parsing in libraries
import gettext

t = gettext.NullTranslations()
_ = t.gettext
assert _("Hello") == "Hello"
```

```python
# Goal: read grouping rules without changing process locale (localeconv needs a real locale)
import locale

saved = locale.setlocale(locale.LC_ALL)
try:
    locale.setlocale(locale.LC_ALL, "C")
    conv = locale.localeconv()
    assert conv["decimal_point"] == "."
finally:
    locale.setlocale(locale.LC_ALL, saved)
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `gettext.install()` in a library | Every importer gets a global `_()` | Bind `_ = translation(...).gettext` in the module namespace |
| `locale.currency()` under `'C'` locale | Raises or misformats | `setlocale(LC_ALL, '')` or a known locale first |
| Deferred `_('literal')` inside loops | Extractor never sees dynamic keys | Use `N_()` marker + `pybabel extract -k N_` |
| Assuming `DAY_1` is Monday | US convention: Sunday is day 1 in `nl_langinfo` | Document calendar semantics for your UI |
| Calling `setlocale` from extension code | Embeds C gettext; affects whole interpreter | Use Python `gettext` module in app code |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [gettext — Multilingual internationalization services](gettext-multilingual-internationalization-services/index.md) | GNU and class-based APIs, `.mo` search, plural/context lookups, I18N workflow |
| [locale — Internationalization services](locale-internationalization-services/index.md) | POSIX categories, `localeconv`, formatting, collation, C gettext bridge |
