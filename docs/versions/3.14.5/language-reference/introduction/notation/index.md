# [Notation](https://docs.python.org/3/reference/introduction.html#notation)

Local notes on **Notation** within [*Introduction*](../index.md). Lexical and syntactic rules throughout the Language Reference use a grammar notation that mixes [EBNF](ebnf/index.md) with [PEG](peg/index.md) ordered choice. Full symbol definitions are on [docs.python.org](https://docs.python.org/3/reference/introduction.html#notation).

The descriptions of lexical analysis and syntax use a grammar notation that is a mixture of [EBNF](ebnf/index.md) and [PEG](peg/index.md). For example:

| Notation | Description |
|----------|-------------|
| [EBNF](ebnf/index.md) | Extended Backus-Naur Form notation used to define grammar rules with sequences, repetition, and grouping. |
| [PEG](peg/index.md)   | Parsing Expression Grammar notation, including ordered choice semantics used in Python’s grammar definitions. |

## Python's grammar notation

The [Python Language Reference](../../index.md) describes lexical analysis and syntax with a notation that is **mostly EBNF**, mixed with a few **PEG** ideas (see [PEG](peg/index.md)). Once you know classic EBNF, you mainly need to learn Python’s symbols and formatting conventions.

### Rule shape

Each rule starts with a **name**, a **colon**, and a definition:

```ebnf
name:   letter (letter | digit | "_")*
letter: "a"..."z" | "A"..."Z"
digit:  "0"..."9"
```

Python uses `:` where many EBNF textbooks use `=`. The example above says:

- A **name** is one **letter** followed by zero or more letters, digits, or underscores.
- A **letter** is any character from `a`–`z` or `A`–`Z`.
- A **digit** is any character from `0`–`9`.

### Symbols and literals

| Notation | Meaning |
|----------|---------|
| `name` | Refers to another grammar rule (a non-terminal). |
| `TOKEN` | An uppercase name refers to a token (for grammar purposes, treated like a rule). |
| `'if'` | Single-quoted text: a **keyword**. |
| `"case"` | Double-quoted text: a **soft keyword**. |
| `'@'` | Single-quoted non-letter: an **operator or delimiter** (OP token). |
| `"text"` / `'text'` | Must match that text literally (without the quotes). |

The choice of single vs double quotes tells you *what kind* of token the literal represents, not just the characters on the page.

### Combining pieces

| Notation | Meaning | Classic EBNF analogue |
|----------|---------|------------------------|
| `e1 e2` | **Sequence** — `e1` then `e2` (whitespace between items). | `e1, e2` with commas |
| `e1 \| e2` | **Alternative** — one of the options. In Python this is PEG *ordered choice*: if `e1` matches, `e2` is not tried. | `\|` (but with different parsing semantics) |
| `e*` | Zero or more repetitions of `e`. | `{ e }` |
| `e+` | One or more repetitions of `e`. | `e, { e }` |
| `[e]` or `e?` | Optional — `e` may appear once or not at all. | `[ e ]` |
| `(e)` | Grouping — treat `e` as one unit. | `( e )` |

**Operator binding:** `*`, `+`, and `?` bind tightly to the item on their left. The bar `|` binds most loosely. Use parentheses when the grouping is not obvious.

**Whitespace** in a rule separates tokens; it is not “match a space character” unless a space appears inside quotes.

### Lexical-only notation

These appear in **lexical** rules (how source text is split into tokens), not in ordinary syntax rules:

| Notation | Meaning |
|----------|---------|
| `"a"..."z"` | Any single character in the inclusive ASCII range from `a` to `z`. |
| `<...>` | Informal description of what may appear, or a shorthand defined nearby. |

### Lookaheads

Some rules peek at the next input without consuming it:

| Notation | Meaning |
|----------|---------|
| `&e` | **Positive lookahead** — `e` must match here, but no characters are consumed. |
| `!e` | **Negative lookahead** — `e` must *not* match here. |

Lookaheads disambiguate cases where a simple sequence or alternative would be unclear.

### Long rules and line breaks

Rules usually fit on one line. When a rule is long, Python’s docs wrap it in either of these styles:

```ebnf
literal: stringliteral | bytesliteral
         | integer | floatnumber | imagnumber
```

```ebnf
literal:
   | stringliteral
   | bytesliteral
   | integer
   | floatnumber
   | imagnumber
```

Each line after the first continues the same rule. A leading `|` on a continuation line is just formatting—it does **not** mean “empty first alternative.”

## Lexical vs syntactic rules

Python splits grammar into two layers:

1. **Lexical analysis** — reads characters and produces **tokens** (names, numbers, keywords, punctuation). Rules in [Lexical analysis](../../lexical-analysis/index.md) are *lexical* definitions. In those rules, whitespace is significant unless it becomes a token such as `INDENT` or `NEWLINE`.
2. **Syntactic analysis** — reads the token stream and checks program structure. Rules in later chapters are *syntactic* definitions. They refer to tokens (like `NAME`, `NUMBER`), not individual characters.

The same BNF-style notation is used for both, but the *input* differs: characters vs tokens. When you read a grammar rule, notice which chapter it lives in—that tells you which layer you are in.

## Quick reference: reading any Python grammar rule

1. Find the rule **name** on the left of the colon.
2. Expand **non-terminals** and **TOKEN** names by looking up their definitions.
3. Match **quoted literals** exactly (respecting keyword vs soft-keyword vs OP quoting).
4. Apply **sequence**, then **repetition** (`*`, `+`, `?`, `[ ]`), then **alternatives** (`|`)—or use parentheses when the rule groups them differently.
5. Stop on **terminals** and **token** symbols; for lexical rules, also use **character ranges** and **lookaheads** where shown.

With these pieces, you can read the grammar for the full Python language as documented in the [Language Reference](../../index.md)—from identifiers and literals through statements, expressions, and the [full grammar specification](../../full-grammar-specification/index.md).

## Best practices

| Practice | Why |
|----------|-----|
| Learn [EBNF](ebnf/index.md) first, then [PEG ordered choice](peg/index.md). | Most rule shape is EBNF-like; `\|` semantics are the main PEG addition. |
| Check which chapter a rule lives in before interpreting whitespace. | Lexical rules treat whitespace differently from syntactic rules. |
| Follow links from rule names to their definitions. | Non-terminals expand recursively until you reach tokens or literals. |
| Use `ast.parse` to test whether source matches the grammar on your version. | The running parser is the practical test of syntax rules. |
| Prefer canonical grammar anchors over paraphrases when filing bugs. | Wording in this mirror is distilled; docs.python.org is normative. |

```python
import ast

# The reference grammar is what CPython's PEG parser implements (since 3.9).
tree = ast.parse("name = letter + '_suffix'")  # illustrative identifier-style assign
assert isinstance(tree.body[0], ast.Assign)
```

## Sections in this repo

| Section | Path |
|---------|------|
| [EBNF](ebnf/index.md) | `ebnf/index.md` |
| [PEG](peg/index.md) | `peg/index.md` |

Parent: [Introduction](../index.md)
