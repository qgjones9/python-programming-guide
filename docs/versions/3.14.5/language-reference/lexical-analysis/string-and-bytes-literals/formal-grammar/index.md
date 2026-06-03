# [Formal grammar](https://docs.python.org/3/reference/lexical_analysis.html#formal-grammar)

Let's walk through the formal grammar that describes Python string literals (excluding “f-strings” and “t-strings”). This grammar uses a notation called EBNF (Extended Backus-Naur Form), which is a standard way to precisely express how different language elements are structured.

In these rules, negative lookahead (`!`) means that the sequence checks ahead to be sure a certain pattern (like a closing quote) does *not* occur before allowing a specific item within the string. This is how Python knows when the literal should end.

Here's how the grammar breaks down:

```ebnf
STRING             ::= stringprefix? stringcontent

stringprefix       ::= "r" | "u" | "b" | "br" | "rb"
                        # The prefix is optional and case-insensitive (e.g., "RB" is valid).

stringcontent      ::= 
     "'''"  ( !"'''"  longstringitem )* "'''"
   | '"""'  ( !'"""'  longstringitem )* '"""'
   | "'"    ( !"'"    stringitem )*    "'"
   | '"'    ( !'"'    stringitem )*    '"'

stringitem        ::= stringchar | stringescapeseq

stringchar        ::= any source character except backslash (`\`) and newline
                        # This means most normal characters are allowed, but not backslashes or line breaks.

longstringitem    ::= stringitem | newline
                        # For triple-quoted strings, newlines are allowed inside.

stringescapeseq   ::= "\" any source character
                        # A backslash followed by any character is interpreted as an escape sequence.
```

### Key Points

- **Whitespace matters.** The placement of spaces is significant in the grammar, so be careful interpreting each rule.
- **Prefix placement:** If you use a prefix (like `r`, `b`, or combinations such as `rb`), it must be attached directly before the opening quote—no spaces between the prefix and the quotes.
- **Negative lookahead** prevents the contents from accidentally closing the string early if they contain quotes.

This grammar covers all string literal forms except the modern formatted strings (`f"..."`) and template strings (`t"..."`), which have more complex rules due to interpolation.

If you're unsure about how string literals are constructed, use this grammar as a reference to understand exactly what is and isn’t allowed by the Python interpreter.
