# [Whitespace between tokens](https://docs.python.org/3/reference/lexical_analysis.html#whitespace-between-tokens)

Except at the start of a logical line or inside string literals, whitespace characters—space, tab, or formfeed—can be used interchangeably to separate tokens.

```ebnf
whitespace ::= ' ' | tab | formfeed
```

Whitespace is only required between two tokens if, without it, the combined sequence could be misinterpreted as a different token. For example:

- `ab` is read as a single token, but `a b` is two tokens.
- Both `+a` and `+ a` are parsed as two tokens (`+` and `a`) because `+a` itself isn't a valid token.

In short, whitespace helps the parser distinguish between tokens only when necessary.