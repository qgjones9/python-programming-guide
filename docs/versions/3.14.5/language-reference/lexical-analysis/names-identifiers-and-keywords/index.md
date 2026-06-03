# [2.3. Names (identifiers and keywords)](https://docs.python.org/3/reference/lexical_analysis.html#names-identifiers-and-keywords)

In Python, a **NAME** token represents _identifiers_, _keywords_, or _soft keywords_. When you define variables, functions, classes, or reference keywords like `if` or `for`, you are using names.

**Identifiers** are the names you assign to objects (like variables, functions, classes).  
**Keywords** are reserved words in Python (like `def`, `class`, `while`, ...) that have special meanings and cannot be used as ordinary identifiers.

### Characters Allowed in Names

A valid Python name (identifier) can include:
- Uppercase letters (`A-Z`)
- Lowercase letters (`a-z`)
- The underscore (`_`)
- Digits (`0-9`), but **not** as the first character
- Non-ASCII Unicode letter-like and digit-like characters (e.g., letters from other languages)

**Note:** Names must contain at least one character and are case-sensitive (`variable` vs `Variable`). There is no upper limit on name length.

#### Examples

```python
# Valid identifiers
variable = 1
Variable = 2
π = 3.14           # Using a Greek letter (non-ASCII)
user_name = "Alice"
value123 = 456
_underscore = "valid"
员工 = "employee"     # Name in Chinese

# Invalid identifiers
1st_value = 10      # Invalid: can't start with a digit
some-var = 5        # Invalid: hyphens are not allowed
def = 5             # Invalid: 'def' is a keyword
```

### Formal Lexical Structure

Names must match these patterns:

- The first character must be a Unicode letter (A–Z, a–z, or non-ASCII letter) or an underscore (`_`).
- Remaining characters may be letters, underscores, or digits (0–9).

**In EBNF notation:**
```
NAME          ::= name_start name_continue*
name_start    ::= "a"–"z" | "A"–"Z" | "_" | <non-ASCII letter>
name_continue ::= name_start | "0"–"9"
identifier    ::= NAME, except keywords
```
> Not all names matched by this grammar are valid—see the section on [Non-ASCII characters in names](non-ascii-characters-in-names/index.md) for further details.

| Subject | Description |
|---------|-------------|
| [Keywords](keywords/index.md) | Reserved words that cannot be used as ordinary identifiers. |
| [Soft Keywords](soft-keywords/index.md) | Context-sensitive keywords that are identifiers in other contexts. |
| [Reserved classes of identifiers](reserved-classes-of-identifiers/index.md) | Identifier patterns with special meaning based on leading or trailing underscores. |
| [Non-ASCII characters in names](non-ascii-characters-in-names/index.md) | Which Unicode letter-like and digit-like characters are valid in names. |



## Best Practices

- Use ASCII-only names whenever possible.
- If you must use non-ASCII characters, use them consistently and avoid using them in names that are not related to the non-ASCII characters.
- Use the underscore `_` to separate words in names.