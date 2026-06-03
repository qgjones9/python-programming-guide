# [token — Constants used with Python parse trees](https://docs.python.org/3/library/token.html)

**Source code:** [`Lib/token.py`](https://github.com/python/cpython/blob/main/Lib/token.py)

When Python reads your source code, the first step is **tokenization**: the text is split into small labeled pieces called **tokens** (identifiers, numbers, operators, newlines, and so on). The parser then builds a parse tree from that token stream.

The `token` module gives you the **numeric codes and names** for those leaf-node tokens. If you inspect parse trees, use [`tokenize`](https://docs.python.org/3/library/tokenize.html), or work with [`ast`](https://docs.python.org/3/library/ast.html), you will see these constants everywhere. The names are defined in the interpreter’s grammar ([`Grammar/Tokens`](https://github.com/python/cpython/blob/main/Grammar/Tokens)); the **integer values** can change between Python versions, so compare by name rather than by number when writing portable code.

The module also maps codes back to names and provides a few helper functions (mirroring the C header definitions).

!!! note "Same text, different token type"
    Which constant you get can depend on tokenizer options. For example, `"+"` may appear as `token.PLUS` or the generic `token.OP`, and `match` may be `token.NAME` or `token.SOFT_KEYWORD` depending on context and flags.

## Helper functions and lookups

These utilities help you interpret raw token values when walking parse trees or debugging the tokenizer.

| Name | What it does |
|------|----------------|
| [`token.tok_name`](https://docs.python.org/3/library/token.html#token.tok_name) | Dictionary from numeric code → string name (for example, turning `59` into `"PLUS"`). Useful when printing parse trees in a readable form. |
| [`token.ISTERMINAL(x)`](https://docs.python.org/3/library/token.html#token.ISTERMINAL) | Returns `True` if `x` is a **terminal** token (a leaf in the parse tree—actual input, not a grammar rule name). |
| [`token.ISNONTERMINAL(x)`](https://docs.python.org/3/library/token.html#token.ISNONTERMINAL) | Returns `True` if `x` is a **non-terminal** (an internal grammar symbol, not a piece of source text). |
| [`token.ISEOF(x)`](https://docs.python.org/3/library/token.html#token.ISEOF) | Returns `True` if `x` marks **end of input**. |

## Core tokens: names, literals, and generic operators

These are the main “content” tokens—the words, numbers, strings, and punctuation that make up a program.

| Constant | Meaning |
|----------|---------|
| `token.NAME` | An **identifier** or **keyword** (`x`, `print`, `if`, …). |
| `token.NUMBER` | A **numeric literal** (`42`, `3.14`, `0x10`, …). |
| `token.STRING` | A **string or bytes literal**, but not an f-string or t-string. The token text is **raw**: quotes, prefix (`r`, `b`, …), and backslashes appear literally—escape sequences are not processed at token time. |
| `token.OP` | A **generic** operator or delimiter. The [`tokenize`](https://docs.python.org/3/library/tokenize.html) module often reports `OP` instead of a specific type like `PLUS`; internally CPython’s tokenizer uses the exact types listed below. |

## Line structure tokens

These tokens describe **how source lines are arranged**, not the meaning of expressions. They connect directly to [Line structure](../../../language-reference/lexical-analysis/line-structure/index.md): logical lines, indentation, and line continuation.

| Constant | Meaning |
|----------|---------|
| `token.NEWLINE` | End of a **logical line**. The parser treats this as a statement boundary in most contexts. |
| `token.NL` | A **non-terminating** newline inside a continued logical line (for example, inside parentheses). The **parser ignores** `NL` tokens. |
| `token.INDENT` | Start of an **indented block** at the beginning of a logical line. |
| `token.DEDENT` | End of an **indented block** at the beginning of a logical line. |
| `token.COMMENT` | A `# …` comment. The **parser ignores** comments. |

## F-string and t-string tokens

Formatted string literals are tokenized in **multiple pieces** so the parser can handle `{…}` expressions inside the quotes.

### F-strings

| Constant | Meaning |
|----------|---------|
| `token.FSTRING_START` | Opening of an f-string (prefix + opening quotes). Does not include the literal body. |
| `token.FSTRING_MIDDLE` | Literal text **inside** an f-string, including format specs like `:.2f`. Expression parts use normal expression tokens delimited by `{`, `}`, `!`, and `:`. |
| `token.FSTRING_END` | Closing quotes of an f-string. |

### T-strings *(added in 3.14)*

Template string literals (`t"…"`) follow the same split pattern as f-strings:

| Constant | Meaning |
|----------|---------|
| `token.TSTRING_START` | Opening of a t-string (prefix + opening quotes). |
| `token.TSTRING_MIDDLE` | Literal text inside a t-string. Replacement fields use the same delimiter tokens as f-strings. |
| `token.TSTRING_END` | Closing quotes of a t-string. |

## End of file and source encoding

| Constant | Meaning |
|----------|---------|
| `token.ENDMARKER` | **No more input.** Appears in top-level grammar rules when parsing is complete. |
| `token.ENCODING` | Declares which **encoding** was used to decode bytes to text. [`tokenize.tokenize()`](https://docs.python.org/3/library/tokenize.html#tokenize.tokenize) always emits this as its **first** token. Not used by the C tokenizer directly, but required by the pure-Python `tokenize` module. |

## Special tokens (tokenizer / parser internals)

These constants exist for **specialized tooling**. The standard [`tokenize`](https://docs.python.org/3/library/tokenize.html) module does **not** normally emit them.

| Constant | Meaning |
|----------|---------|
| `token.TYPE_IGNORE` | A `# type: ignore` comment, when `PyCF_TYPE_COMMENTS` is enabled. Replaces a normal `COMMENT` token. |
| `token.TYPE_COMMENT` | A `# type: …` comment for static typing, with the same flag. |
| `token.SOFT_KEYWORD` | Marks a **soft keyword** in the grammar. The tokenizer never emits this directly—check a `NAME` token’s text with [`keyword.issoftkeyword()`](https://docs.python.org/3/library/keyword.html#keyword.issoftkeyword). |
| `token.ERRORTOKEN` | Marks **invalid** input. `tokenize` usually raises an exception instead; the parser may also reject valid-looking `OP` or `NAME` tokens later. |

## Operators and delimiters (exact types)

The constants below map each **specific** operator or delimiter to its source text. In [`tokenize`](https://docs.python.org/3/library/tokenize.html) output you often see generic `OP` instead; use `TokenInfo.exact_type` (see the tokenize docs) to recover the precise constant.

### Grouping and separators

| Constant | Value |
|----------|-------|
| `token.LPAR` / `token.RPAR` | `(` / `)` |
| `token.LSQB` / `token.RSQB` | `[` / `]` |
| `token.LBRACE` / `token.RBRACE` | `{` / `}` |
| `token.COLON` | `:` |
| `token.COMMA` | `,` |
| `token.SEMI` | `;` |
| `token.DOT` | `.` |

### Arithmetic and bitwise operators

| Constant | Value |
|----------|-------|
| `token.PLUS` / `token.MINUS` | `+` / `-` |
| `token.STAR` / `token.SLASH` | `*` / `/` |
| `token.DOUBLESTAR` / `token.DOUBLESLASH` | `**` / `//` |
| `token.PERCENT` | `%` |
| `token.AMPER` / `token.VBAR` | `&` / `\|` |
| `token.CIRCUMFLEX` / `token.TILDE` | `^` / `~` |
| `token.LEFTSHIFT` / `token.RIGHTSHIFT` | `<<` / `>>` |
| `token.AT` | `@` |

### Comparisons and other punctuation

| Constant | Value |
|----------|-------|
| `token.LESS` / `token.GREATER` | `<` / `>` |
| `token.EQUAL` | `=` |
| `token.EQEQUAL` / `token.NOTEQUAL` | `==` / `!=` |
| `token.LESSEQUAL` / `token.GREATEREQUAL` | `<=` / `>=` |
| `token.RARROW` | `->` |
| `token.ELLIPSIS` | `...` |
| `token.COLONEQUAL` | `:=` |
| `token.EXCLAMATION` | `!` |

### Augmented assignment

| Constant | Value |
|----------|-------|
| `token.PLUSEQUAL` / `token.MINEQUAL` | `+=` / `-=` |
| `token.STAREQUAL` / `token.SLASHEQUAL` | `*=` / `/=` |
| `token.PERCENTEQUAL` | `%=` |
| `token.AMPEREQUAL` / `token.VBAREQUAL` | `&=` / `\|=` |
| `token.CIRCUMFLEXEQUAL` | `^=` |
| `token.LEFTSHIFTEQUAL` / `token.RIGHTSHIFTEQUAL` | `<<=` / `>>=` |
| `token.DOUBLESTAREQUAL` / `token.DOUBLESLASHEQUAL` | `**=` / `//=` |
| `token.ATEQUAL` | `@=` |

## Other module-level constants

| Constant | Meaning |
|----------|---------|
| `token.N_TOKENS` | Total count of token types defined in this module. |
| `token.EXACT_TOKEN_TYPES` | Dict mapping **string form** of a token (for example `"+"`) to its numeric code. Added in 3.8. |

You can inspect the mapping at runtime:

```python
import token

print(token.EXACT_TOKEN_TYPES)
```

The table below lists every entry in `token.EXACT_TOKEN_TYPES` for Python 3.14 (numeric codes may differ in other versions):

| Name | Acronym | Source | Token constant | Numeric |
|------|---------|--------|----------------|---------|
| Left parenthesis | LPAR | `(` | `token.LPAR` | 7 |
| Right parenthesis | RPAR | `)` | `token.RPAR` | 8 |
| Left square bracket | LSQB | `[` | `token.LSQB` | 9 |
| Right square bracket | RSQB | `]` | `token.RSQB` | 10 |
| Colon | COLON | `:` | `token.COLON` | 11 |
| Comma | COMMA | `,` | `token.COMMA` | 12 |
| Semicolon | SEMI | `;` | `token.SEMI` | 13 |
| Plus | PLUS | `+` | `token.PLUS` | 14 |
| Minus | MINUS | `-` | `token.MINUS` | 15 |
| Asterisk | STAR | `*` | `token.STAR` | 16 |
| Slash | SLASH | `/` | `token.SLASH` | 17 |
| Vertical bar | VBAR | `\|` | `token.VBAR` | 18 |
| Ampersand | AMPER | `&` | `token.AMPER` | 19 |
| Less than | LESS | `<` | `token.LESS` | 20 |
| Greater than | GREATER | `>` | `token.GREATER` | 21 |
| Equal | EQUAL | `=` | `token.EQUAL` | 22 |
| Dot | DOT | `.` | `token.DOT` | 23 |
| Percent | PERCENT | `%` | `token.PERCENT` | 24 |
| Left brace | LBRACE | `{` | `token.LBRACE` | 25 |
| Right brace | RBRACE | `}` | `token.RBRACE` | 26 |
| Equal equal | EQEQUAL | `==` | `token.EQEQUAL` | 27 |
| Not equal | NOTEQUAL | `!=` | `token.NOTEQUAL` | 28 |
| Less than or equal | LESSEQUAL | `<=` | `token.LESSEQUAL` | 29 |
| Greater than or equal | GREATEREQUAL | `>=` | `token.GREATEREQUAL` | 30 |
| Tilde | TILDE | `~` | `token.TILDE` | 31 |
| Circumflex | CIRCUMFLEX | `^` | `token.CIRCUMFLEX` | 32 |
| Left shift | LEFTSHIFT | `<<` | `token.LEFTSHIFT` | 33 |
| Right shift | RIGHTSHIFT | `>>` | `token.RIGHTSHIFT` | 34 |
| Double asterisk | DOUBLESTAR | `**` | `token.DOUBLESTAR` | 35 |
| Plus equal | PLUSEQUAL | `+=` | `token.PLUSEQUAL` | 36 |
| Minus equal | MINEQUAL | `-=` | `token.MINEQUAL` | 37 |
| Asterisk equal | STAREQUAL | `*=` | `token.STAREQUAL` | 38 |
| Slash equal | SLASHEQUAL | `/=` | `token.SLASHEQUAL` | 39 |
| Percent equal | PERCENTEQUAL | `%=` | `token.PERCENTEQUAL` | 40 |
| Ampersand equal | AMPEREQUAL | `&=` | `token.AMPEREQUAL` | 41 |
| Vertical bar equal | VBAREQUAL | `\|=` | `token.VBAREQUAL` | 42 |
| Circumflex equal | CIRCUMFLEXEQUAL | `^=` | `token.CIRCUMFLEXEQUAL` | 43 |
| Left shift equal | LEFTSHIFTEQUAL | `<<=` | `token.LEFTSHIFTEQUAL` | 44 |
| Right shift equal | RIGHTSHIFTEQUAL | `>>=` | `token.RIGHTSHIFTEQUAL` | 45 |
| Double asterisk equal | DOUBLESTAREQUAL | `**=` | `token.DOUBLESTAREQUAL` | 46 |
| Double slash | DOUBLESLASH | `//` | `token.DOUBLESLASH` | 47 |
| Double slash equal | DOUBLESLASHEQUAL | `//=` | `token.DOUBLESLASHEQUAL` | 48 |
| At sign | AT | `@` | `token.AT` | 49 |
| At sign equal | ATEQUAL | `@=` | `token.ATEQUAL` | 50 |
| Right arrow | RARROW | `->` | `token.RARROW` | 51 |
| Ellipsis | ELLIPSIS | `...` | `token.ELLIPSIS` | 52 |
| Colon equal | COLONEQUAL | `:=` | `token.COLONEQUAL` | 53 |
| Exclamation mark | EXCLAMATION | `!` | `token.EXCLAMATION` | 54 |

## Version history

| Version | Change |
|---------|--------|
| 3.5 | Added `AWAIT` and `ASYNC` tokens. |
| 3.7 | Added `COMMENT`, `NL`, and `ENCODING`. Removed `AWAIT` and `ASYNC` (`async` / `await` tokenized as `NAME`). |
| 3.8 | Added `TYPE_COMMENT`, `TYPE_IGNORE`, `COLONEQUAL`, and `EXACT_TOKEN_TYPES`. Restored `AWAIT` / `ASYNC` for parsing older grammar via `ast.parse(..., feature_version=6)`. |
| 3.12 | Added `EXCLAMATION`. |
| 3.13 | Removed `AWAIT` and `ASYNC` again. |
| 3.14 | Added `TSTRING_START`, `TSTRING_MIDDLE`, and `TSTRING_END`. |