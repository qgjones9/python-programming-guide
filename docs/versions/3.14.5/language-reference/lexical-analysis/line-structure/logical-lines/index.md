# [Logical lines](https://docs.python.org/3/reference/lexical_analysis.html#logical-lines)

The lexer turns source text into tokens on **logical lines**: units bounded by a [`NEWLINE`](../../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#line-structure-tokens) token. Full rules for building logical lines from [physical lines](../physical-lines/index.md) live in [explicit](../explicit-line-joining/index.md) and [implicit](../implicit-line-joining/index.md) line joining; this page focuses on what a logical line means for statements and parsing.

The end of a logical line is represented by the token [`NEWLINE`](../../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#line-structure-tokens) (`token.NEWLINE`). Statements cannot cross logical line boundaries except where [`NEWLINE`](../../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#line-structure-tokens) is allowed by the syntax (e.g., between statements in compound statements). A logical line is constructed from one or more [physical lines](../physical-lines/index.md) by following the [explicit line joining](../explicit-line-joining/index.md) or [implicit line joining](../implicit-line-joining/index.md) rules.

## One physical line, one logical line

By default, each physical line that is not joined or inside an open bracket pair ends with one `NEWLINE`:

```python
x = 1
y = 2
# Two physical lines → two logical lines → two simple statements
```

## Joining collapses physical lines

[Explicit](../explicit-line-joining/index.md) and [implicit](../implicit-line-joining/index.md) joining produce **one** logical line (and thus one terminating `NEWLINE`) even when the source spans several physical lines:

```python
total = (1 + 2
         + 3)
# Parentheses keep the expression on one logical line; NEWLINE after the closing ')'

ok = 1900 < 2000 < 2100 and 1 <= 6 <= 12 \
    and 1 <= 15 <= 31
assert ok
# Backslash join: two physical lines, one logical line
```

## Statements usually cannot straddle logical lines

Without a joiner or bracketed expression, a line break starts a new logical line and therefore a new statement. The second line below is **not** continued addition—it is a separate statement (a unary `+` on `2`):

```python
x = 1
+ 2
# Logical line 1: x = 1
# Logical line 2: +2  (expression statement; not "x = 1 + 2")
```

To add on the next line, join explicitly or wrap in parentheses (see the examples above).

## `NEWLINE` inside compound statements

Compound statements (e.g. `if`, `for`, `def`) allow `NEWLINE` **between** the statements in a suite, but each simple statement still occupies whole logical lines within that block:

```python
if True:
    a = 1
    b = 2
# Three logical lines: header "if True:", then "a = 1", then "b = 2"
```

The header line ends with `:`; the indented body lines each end with their own `NEWLINE`. You cannot split a **single** simple statement across logical lines without the joining rules above.

## Blank lines and `NEWLINE`

A line that contains only whitespace and/or a comment is a [blank line](../blank-lines/index.md): it does **not** emit `NEWLINE` for parsing purposes. In the interactive interpreter, a completely empty line (no spaces, no `#`) can end a multi-line compound entry—that behavior is REPL-specific, not a change to how logical lines are tokenized in a `.py` file.
