# [1. Introduction](https://docs.python.org/3/reference/introduction.html)

Local notes for [**1. Introduction**](https://docs.python.org/3/reference/introduction.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. This mirror is shorthand; wording and grammar are authoritative only on docs.python.org.

### [1.1. Alternate Implementations](https://docs.python.org/3/reference/introduction.html#alternate-implementations)

- Canonical: **[1.1. Alternate Implementations](https://docs.python.org/3/reference/introduction.html#alternate-implementations)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Statements execute for effect; expressions inside them still follow semantics.
seen = []

def record():
    seen.append(True)
    return "done"


record()
assert seen == [True]
```

### [1.2. Notation](https://docs.python.org/3/reference/introduction.html#notation)

- Canonical: **[1.2. Notation](https://docs.python.org/3/reference/introduction.html#notation)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

## Sections in this repo

- [1.1. Alternate Implementations](alternate-implementations/index.md)
- [1.2. Notation](notation/index.md)
