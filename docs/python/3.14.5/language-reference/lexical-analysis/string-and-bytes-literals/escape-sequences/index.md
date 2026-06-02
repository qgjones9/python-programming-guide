# [Escape sequences](https://docs.python.org/3/reference/lexical_analysis.html#escape-sequences)

Unless an `r` or `R` prefix is present, escape sequences in Python string and bytes literals are processed. Escape sequences let you insert special characters in strings using a backslash (`\`). The following are the standard escape sequences recognized by Python:

| Escape Sequence    | Meaning                              |
|--------------------|--------------------------------------|
| `\<newline>`       | Ignored end of line (line continuation) |
| `\\`               | Backslash (`\`)                      |
| `\'`               | Single quote (`'`)                   |
| `\"`               | Double quote (`"`)                   |
| `\a`               | ASCII Bell (BEL)                     |
| `\b`               | ASCII Backspace (BS)                 |
| `\f`               | ASCII Formfeed (FF)                  |
| `\n`               | ASCII Linefeed (LF), newline         |
| `\r`               | ASCII Carriage Return (CR)           |
| `\t`               | ASCII Horizontal Tab (TAB)           |
| `\v`               | ASCII Vertical Tab (VT)              |
| `\ooo`             | Character with octal value `ooo`     |
| `\xhh`             | Character with hex value `hh`        |
| `\N{name}`         | Unicode character named `name`       |
| `\uxxxx`           | Unicode character with hex value `xxxx`  |
| `\Uxxxxxxxx`       | Unicode character with hex value `xxxxxxxx` |

For more details on each type of escape sequence, see the subsections below.




| Section | Description |
|---------|-------------|
| [Ignored end of line](ignored-end-of-line/index.md) | How a backslash at the end of a line continues a string without inserting a newline. |
| [Escaped characters](escaped-characters/index.md) | Standard backslash escapes such as `\n`, `\t`, and `\\`. |
| [Octal character](octal-character/index.md) | `\ooo` escapes for characters from their octal code point. |
| [Hexadecimal character](hexadecimal-character/index.md) | `\xhh` escapes for bytes and limited hex values. |
| [Named Unicode character](named-unicode-character/index.md) | `\N{name}` escapes using Unicode character names. |
| [Hexadecimal Unicode characters](hexadecimal-unicode-characters/index.md) | `\u` and `\U` escapes for Unicode code points. |
| [Unrecognized escape sequences](unrecognized-escape-sequences/index.md) | What happens when a backslash is not followed by a valid escape. |
