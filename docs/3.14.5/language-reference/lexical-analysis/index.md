# [2. Lexical analysis](https://docs.python.org/3/reference/lexical_analysis.html)

Local notes for [**2. Lexical analysis**](https://docs.python.org/3/reference/lexical_analysis.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. This mirror is shorthand; wording and grammar are authoritative only on docs.python.org.

### [2.1. Line structure](https://docs.python.org/3/reference/lexical_analysis.html#line-structure)

- Canonical: **[2.1. Line structure](https://docs.python.org/3/reference/lexical_analysis.html#line-structure)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

### [2.2. Other tokens](https://docs.python.org/3/reference/lexical_analysis.html#other-tokens)

- Canonical: **[2.2. Other tokens](https://docs.python.org/3/reference/lexical_analysis.html#other-tokens)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

### [2.3. Names (identifiers and keywords)](https://docs.python.org/3/reference/lexical_analysis.html#names-identifiers-and-keywords)

- Canonical: **[2.3. Names (identifiers and keywords)](https://docs.python.org/3/reference/lexical_analysis.html#names-identifiers-and-keywords)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

### [2.4. Literals](https://docs.python.org/3/reference/lexical_analysis.html#literals)

- Canonical: **[2.4. Literals](https://docs.python.org/3/reference/lexical_analysis.html#literals)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

### [2.5. String and Bytes literals](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals)

- Canonical: **[2.5. String and Bytes literals](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

### [2.6. Numeric literals](https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals)

- Canonical: **[2.6. Numeric literals](https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

### [2.7. Operators and delimiters](https://docs.python.org/3/reference/lexical_analysis.html#operators-and-delimiters)

- Canonical: **[2.7. Operators and delimiters](https://docs.python.org/3/reference/lexical_analysis.html#operators-and-delimiters)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

## Sections in this repo

- [2.1. Line structure](line-structure/index.md)
- [2.2. Other tokens](other-tokens/index.md)
- [2.3. Names (identifiers and keywords)](names-identifiers-and-keywords/index.md)
- [2.4. Literals](literals/index.md)
- [2.5. String and Bytes literals](string-and-bytes-literals/index.md)
- [2.6. Numeric literals](numeric-literals/index.md)
- [2.7. Operators and delimiters](operators-and-delimiters/index.md)
