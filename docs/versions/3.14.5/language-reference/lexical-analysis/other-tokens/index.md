# [2.2. Other tokens](https://docs.python.org/3/reference/lexical_analysis.html#other-tokens)

After [line structure](../line-structure/index.md) tokens (`NEWLINE`, `INDENT`, `DEDENT`), the remaining lexical categories are **names**, **literals**, and **operators/delimiters**. Whitespace is not a token—it only separates tokens. The lexer always takes the **longest** legal token when reading left to right.

Besides the [line structure tokens](../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#line-structure-tokens) [`NEWLINE`](../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#line-structure-tokens), [`INDENT`](../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#line-structure-tokens), and [`DEDENT`](../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#line-structure-tokens) (discussed in [Line structure](../line-structure/index.md)), the following categories of tokens exist:

| Category | Typical `tokenize` types | Section in this repo |
|----------|--------------------------|----------------------|
| Identifiers and keywords | `NAME` | [Names (identifiers and keywords)](../names-identifiers-and-keywords/index.md) |
| Literals | `NUMBER`, `STRING` | [Literals](../literals/index.md) |
| Operators and delimiters | `OP` | [Operators and delimiters](../operators-and-delimiters/index.md) |

[Whitespace](../line-structure/whitespace-between-tokens/index.md) characters (other than [logical line terminators](../line-structure/logical-lines/index.md), discussed earlier) are not tokens, but serve to delimit tokens. Where ambiguity exists, a token comprises the longest possible string that forms a legal token, when read from left to right.

## Longest-match disambiguation

The lexer greedily forms the longest valid token. That matters for names, operators, and multi-character punctuators:

```python
import io
import tokenize

def token_strings(src):
    keep = {tokenize.NAME, tokenize.OP, tokenize.NUMBER, tokenize.STRING}
    return [
        tok.string
        for tok in tokenize.generate_tokens(io.StringIO(src).readline)
        if tok.type in keep
    ]

# One NAME, not two letters
assert token_strings("ab") == ["ab"]

# Whitespace splits identifiers
assert token_strings("a b") == ["a", "b"]

# '<=' is one OP, not '<' followed by '='
assert token_strings("a<=b") == ["a", "<=", "b"]

# Ellipsis is one OP token (type ...), not three '.' operators
assert token_strings("...") == ["..."]
assert ... is Ellipsis
```

## When whitespace is optional

Some adjacent spellings tokenize the same way with or without spaces, because no single longer token can absorb the characters:

```python
import io
import tokenize

def ops_and_names(src):
    pairs = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type in (tokenize.OP, tokenize.NAME, tokenize.NUMBER):
            pairs.append(tok.string)
    return pairs

assert ops_and_names("+a") == ["+", "a"]
assert ops_and_names("+ a") == ["+", "a"]
# '+a' is not one token; unary '+' and name 'a' are always separate
```

Other pairs **do** require separation: `ab` is one identifier, but `a b` must be two. If concatenation would spell a different legal token, spaces matter—follow the official rule and, when in doubt, inspect with `tokenize`.

## Whitespace never appears in the token stream

Only comments and encoding cookies use `#` at the lexical level; ordinary spaces, tabs, and formfeeds between tokens are skipped entirely:

```python
import io
import tokenize

meaningful = [
    tok
    for tok in tokenize.generate_tokens(io.StringIO("a   +   b").readline)
    if tok.type in (tokenize.NAME, tokenize.OP)
]
assert [t.string for t in meaningful] == ["a", "+", "b"]
# No token's string is only whitespace—spaces are skipped, not tokenized
```

## Sections in this repo

| Section | Description |
|---------|-------------|
| [Line structure](../line-structure/index.md) | `NEWLINE`, `INDENT`, `DEDENT`, and how lines are formed |
| [Names (identifiers and keywords)](../names-identifiers-and-keywords/index.md) | `NAME` tokens, keywords, soft keywords |
| [Literals](../literals/index.md) | `STRING`, `NUMBER`, and related literal forms |
| [Operators and delimiters](../operators-and-delimiters/index.md) | `OP` tokens and the formal grammar of symbols |
