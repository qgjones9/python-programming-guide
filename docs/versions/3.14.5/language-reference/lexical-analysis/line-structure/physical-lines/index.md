# [Physical lines](https://docs.python.org/3/reference/lexical_analysis.html#physical-lines)

A physical line in Python refers to a continuous sequence of characters that ends with a specific end-of-line marker. Several conventions exist for marking the end of a line, depending on the operating system:

- On Unix systems, lines end with an ASCII linefeed character (`\n`).
- On Windows, lines use a combination of carriage return and linefeed (`\r\n`).
- On classic Mac OS, the end-of-line marker is an ASCII carriage return (`\r`).

Regardless of which convention is present in your source file, Python's parser automatically converts all end-of-line sequences (`\n`, `\r\n`, or `\r`) to a single ASCII linefeed (`\n`). This means that line endings are normalized everywhere, including inside [string literals](../../string-and-bytes-literals/index.md), and files can even mix multiple line ending styles without affecting how Python interprets them.

If the source file does not end with a standard line ending, reaching the end of input is still treated as ending the last line—so the final physical line is considered complete even without a trailing newline character.

```ebnf
newline: <ASCII LF> | <ASCII CR> <ASCII LF> | <ASCII CR>
```
