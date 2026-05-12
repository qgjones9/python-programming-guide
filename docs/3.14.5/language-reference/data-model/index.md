# [3. Data model](https://docs.python.org/3/reference/datamodel.html)

Local notes for [**3. Data model**](https://docs.python.org/3/reference/datamodel.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. This mirror is shorthand; wording and grammar are authoritative only on docs.python.org.

### [3.1. Objects, values and types](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types)

- Canonical: **[3.1. Objects, values and types](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

### [3.2. The standard type hierarchy](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy)

- Canonical: **[3.2. The standard type hierarchy](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Names bind to objects; multiple names may reference the same value (aliases).
nums = []
alias = nums
alias.append(1)
assert nums == [1]
```

### [3.3. Special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names)

- Canonical: **[3.3. Special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names)** — definitions, judgments, and edge cases.
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

### [3.4. Coroutines](https://docs.python.org/3/reference/datamodel.html#coroutines)

- Canonical: **[3.4. Coroutines](https://docs.python.org/3/reference/datamodel.html#coroutines)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

## Sections in this repo

- [3.1. Objects, values and types](objects-values-and-types/index.md)
- [3.2. The standard type hierarchy](the-standard-type-hierarchy/index.md)
- [3.3. Special method names](special-method-names/index.md)
- [3.4. Coroutines](coroutines/index.md)
