# [4. Execution model](https://docs.python.org/3/reference/executionmodel.html)

Local notes for [**4. Execution model**](https://docs.python.org/3/reference/executionmodel.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. This mirror is shorthand; wording and grammar are authoritative only on docs.python.org.

### [4.1. Structure of a program](https://docs.python.org/3/reference/executionmodel.html#structure-of-a-program)

- Canonical: **[4.1. Structure of a program](https://docs.python.org/3/reference/executionmodel.html#structure-of-a-program)** — definitions, judgments, and edge cases.
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

### [4.2. Naming and binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)

- Canonical: **[4.2. Naming and binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [4.3. Exceptions](https://docs.python.org/3/reference/executionmodel.html#exceptions)

- Canonical: **[4.3. Exceptions](https://docs.python.org/3/reference/executionmodel.html#exceptions)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [4.4. Runtime Components](https://docs.python.org/3/reference/executionmodel.html#runtime-components)

- Canonical: **[4.4. Runtime Components](https://docs.python.org/3/reference/executionmodel.html#runtime-components)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

## Sections in this repo

- [4.1. Structure of a program](structure-of-a-program/index.md)
- [4.2. Naming and binding](naming-and-binding/index.md)
- [4.3. Exceptions](exceptions/index.md)
- [4.4. Runtime Components](runtime-components/index.md)
