# [2.1. Line structure](https://docs.python.org/3/reference/lexical_analysis.html#line-structure)

A Python program is divided into a number of logical lines.

| Section | Description |
|---------|-------------|
| [Logical lines](logical-lines/index.md) | How logical lines end with `NEWLINE` and how statements respect line boundaries. |
| [Physical lines](physical-lines/index.md) | End-of-line conventions on Unix, Windows, and classic Mac OS. |
| [Comments](comments/index.md) | `#` comments and how the parser treats them. |
| [Encoding declarations](encoding-declarations/index.md) | Source file encoding comments on the first or second line. |
| [Explicit line joining](explicit-line-joining/index.md) | Joining physical lines with a trailing backslash (`\`). |
| [Implicit line joining](implicit-line-joining/index.md) | Splitting expressions across lines inside `()`, `[]`, or `{}`. |
| [Blank lines](blank-lines/index.md) | Lines with only whitespace or comments, and when they are ignored. |
| [Indentation](indentation/index.md) | Leading whitespace, `INDENT`/`DEDENT` tokens, and block structure. |
| [Whitespace between tokens](whitespace-between-tokens/index.md) | Spaces and tabs that separate tokens but are not significant otherwise. |
| [End marker](end-marker/index.md) | The token that signals end of input after the final line. |
