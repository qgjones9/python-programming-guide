# [5. The import system](https://docs.python.org/3/reference/import.html)

Local notes for [**5. The import system**](https://docs.python.org/3/reference/import.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. This mirror is shorthand; wording and grammar are authoritative only on docs.python.org.

### [5.1. importlib](https://docs.python.org/3/reference/import.html#importlib)

- Canonical: **[5.1. importlib](https://docs.python.org/3/reference/import.html#importlib)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```

### [5.2. Packages](https://docs.python.org/3/reference/import.html#packages)

- Canonical: **[5.2. Packages](https://docs.python.org/3/reference/import.html#packages)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Names bind to objects; multiple names may reference the same value (aliases).
nums = []
alias = nums
alias.append(1)
assert nums == [1]
```

### [5.3. Searching](https://docs.python.org/3/reference/import.html#searching)

- Canonical: **[5.3. Searching](https://docs.python.org/3/reference/import.html#searching)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

### [5.4. Loading](https://docs.python.org/3/reference/import.html#loading)

- Canonical: **[5.4. Loading](https://docs.python.org/3/reference/import.html#loading)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

### [5.5. The Path Based Finder](https://docs.python.org/3/reference/import.html#the-path-based-finder)

- Canonical: **[5.5. The Path Based Finder](https://docs.python.org/3/reference/import.html#the-path-based-finder)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

### [5.6. Replacing the standard import system](https://docs.python.org/3/reference/import.html#replacing-the-standard-import-system)

- Canonical: **[5.6. Replacing the standard import system](https://docs.python.org/3/reference/import.html#replacing-the-standard-import-system)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

### [5.7. Package Relative Imports](https://docs.python.org/3/reference/import.html#package-relative-imports)

- Canonical: **[5.7. Package Relative Imports](https://docs.python.org/3/reference/import.html#package-relative-imports)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

### [5.8. Special considerations for __main__](https://docs.python.org/3/reference/import.html#special-considerations-for-main)

- Canonical: **[5.8. Special considerations for __main__](https://docs.python.org/3/reference/import.html#special-considerations-for-main)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [5.9. References](https://docs.python.org/3/reference/import.html#references)

- Canonical: **[5.9. References](https://docs.python.org/3/reference/import.html#references)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```

## Sections in this repo

- [5.1. importlib](importlib/index.md)
- [5.2. Packages](packages/index.md)
- [5.3. Searching](searching/index.md)
- [5.4. Loading](loading/index.md)
- [5.5. The Path Based Finder](the-path-based-finder/index.md)
- [5.6. Replacing the standard import system](replacing-the-standard-import-system/index.md)
- [5.7. Package Relative Imports](package-relative-imports/index.md)
- [5.8. Special considerations for __main__](special-considerations-for-main/index.md)
- [5.9. References](references/index.md)
