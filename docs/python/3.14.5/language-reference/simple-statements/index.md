# [7. Simple statements](https://docs.python.org/3/reference/simple_stmts.html)

Local notes for [**7. Simple statements**](https://docs.python.org/3/reference/simple_stmts.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. This mirror is shorthand; wording and grammar are authoritative only on docs.python.org.

### [7.1. Expression statements](https://docs.python.org/3/reference/simple_stmts.html#expression-statements)

- Canonical: **[7.1. Expression statements](https://docs.python.org/3/reference/simple_stmts.html#expression-statements)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [7.2. Assignment statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements)

- Canonical: **[7.2. Assignment statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```

### [7.3. The assert statement](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)

- Canonical: **[7.3. The assert statement](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

### [7.4. The pass statement](https://docs.python.org/3/reference/simple_stmts.html#the-pass-statement)

- Canonical: **[7.4. The pass statement](https://docs.python.org/3/reference/simple_stmts.html#the-pass-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

### [7.5. The del statement](https://docs.python.org/3/reference/simple_stmts.html#the-del-statement)

- Canonical: **[7.5. The del statement](https://docs.python.org/3/reference/simple_stmts.html#the-del-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [7.6. The return statement](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement)

- Canonical: **[7.6. The return statement](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

### [7.7. The yield statement](https://docs.python.org/3/reference/simple_stmts.html#the-yield-statement)

- Canonical: **[7.7. The yield statement](https://docs.python.org/3/reference/simple_stmts.html#the-yield-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

### [7.8. The raise statement](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement)

- Canonical: **[7.8. The raise statement](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

### [7.9. The break statement](https://docs.python.org/3/reference/simple_stmts.html#the-break-statement)

- Canonical: **[7.9. The break statement](https://docs.python.org/3/reference/simple_stmts.html#the-break-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [7.10. The continue statement](https://docs.python.org/3/reference/simple_stmts.html#the-continue-statement)

- Canonical: **[7.10. The continue statement](https://docs.python.org/3/reference/simple_stmts.html#the-continue-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [7.11. The import statement](https://docs.python.org/3/reference/simple_stmts.html#the-import-statement)

- Canonical: **[7.11. The import statement](https://docs.python.org/3/reference/simple_stmts.html#the-import-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Names bind to objects; multiple names may reference the same value (aliases).
nums = []
alias = nums
alias.append(1)
assert nums == [1]
```

### [7.12. The global statement](https://docs.python.org/3/reference/simple_stmts.html#the-global-statement)

- Canonical: **[7.12. The global statement](https://docs.python.org/3/reference/simple_stmts.html#the-global-statement)** — definitions, judgments, and edge cases.
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

### [7.13. The nonlocal statement](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement)

- Canonical: **[7.13. The nonlocal statement](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```

### [7.14. The type statement](https://docs.python.org/3/reference/simple_stmts.html#the-type-statement)

- Canonical: **[7.14. The type statement](https://docs.python.org/3/reference/simple_stmts.html#the-type-statement)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

## Sections in this repo

- [7.1. Expression statements](expression-statements/index.md)
- [7.2. Assignment statements](assignment-statements/index.md)
- [7.3. The assert statement](the-assert-statement/index.md)
- [7.4. The pass statement](the-pass-statement/index.md)
- [7.5. The del statement](the-del-statement/index.md)
- [7.6. The return statement](the-return-statement/index.md)
- [7.7. The yield statement](the-yield-statement/index.md)
- [7.8. The raise statement](the-raise-statement/index.md)
- [7.9. The break statement](the-break-statement/index.md)
- [7.10. The continue statement](the-continue-statement/index.md)
- [7.11. The import statement](the-import-statement/index.md)
- [7.12. The global statement](the-global-statement/index.md)
- [7.13. The nonlocal statement](the-nonlocal-statement/index.md)
- [7.14. The type statement](the-type-statement/index.md)
