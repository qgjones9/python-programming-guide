# [locale encoding](https://docs.python.org/3.14/glossary.html#term-locale-encoding)

On Unix, it is the encoding of the LC_CTYPE locale. It can be set with
[locale.setlocale(locale.LC_CTYPE,new_locale)](https://docs.python.org/3.14/library/locale.html#locale.setlocale).

On Windows, it is the ANSI code page (ex: `"cp1252"`).

On Android and VxWorks, Python uses `"utf-8"` as the locale encoding.

[locale.getencoding()](https://docs.python.org/3.14/library/locale.html#locale.getencoding) can be used to get the locale encoding.

See also the [filesystem encoding and error handler](../filesystem-encoding-and-error-handler/index.md).
