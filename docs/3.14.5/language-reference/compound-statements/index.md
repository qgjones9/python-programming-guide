# [8. Compound statements](https://docs.python.org/3/reference/compound_stmts.html)

Local notes for [**8. Compound statements**](https://docs.python.org/3/reference/compound_stmts.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. This mirror is shorthand; wording and grammar are authoritative only on docs.python.org.

### [8.1. The if statement](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement)

- Canonical: **[8.1. The if statement](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

### [8.2. The while statement](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)

- Canonical: **[8.2. The while statement](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

### [8.3. The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)

- Canonical: **[8.3. The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

### [8.4. The try statement](https://docs.python.org/3/reference/compound_stmts.html#the-try-statement)

- Canonical: **[8.4. The try statement](https://docs.python.org/3/reference/compound_stmts.html#the-try-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

### [8.5. The with statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)

- Canonical: **[8.5. The with statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

### [8.6. The match statement](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)

- Canonical: **[8.6. The match statement](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

### [8.7. Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)

- Canonical: **[8.7. Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

### [8.8. Class definitions](https://docs.python.org/3/reference/compound_stmts.html#class-definitions)

- Canonical: **[8.8. Class definitions](https://docs.python.org/3/reference/compound_stmts.html#class-definitions)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

### [8.9. Coroutines](https://docs.python.org/3/reference/compound_stmts.html#coroutines)

- Canonical: **[8.9. Coroutines](https://docs.python.org/3/reference/compound_stmts.html#coroutines)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```

### [8.10. Type parameter lists](https://docs.python.org/3/reference/compound_stmts.html#type-parameter-lists)

- Canonical: **[8.10. Type parameter lists](https://docs.python.org/3/reference/compound_stmts.html#type-parameter-lists)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

### [8.11. Annotations](https://docs.python.org/3/reference/compound_stmts.html#annotations)

- Canonical: **[8.11. Annotations](https://docs.python.org/3/reference/compound_stmts.html#annotations)** — definitions, judgments, and edge cases.
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

## Sections in this repo

- [8.1. The if statement](the-if-statement/index.md)
- [8.2. The while statement](the-while-statement/index.md)
- [8.3. The for statement](the-for-statement/index.md)
- [8.4. The try statement](the-try-statement/index.md)
- [8.5. The with statement](the-with-statement/index.md)
- [8.6. The match statement](the-match-statement/index.md)
- [8.7. Function definitions](function-definitions/index.md)
- [8.8. Class definitions](class-definitions/index.md)
- [8.9. Coroutines](coroutines/index.md)
- [8.10. Type parameter lists](type-parameter-lists/index.md)
- [8.11. Annotations](annotations/index.md)
