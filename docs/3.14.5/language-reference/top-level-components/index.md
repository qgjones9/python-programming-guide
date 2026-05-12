# [9. Top-level components](https://docs.python.org/3/reference/toplevel_components.html)

Local notes for [**9. Top-level components**](https://docs.python.org/3/reference/toplevel_components.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. This mirror is shorthand; wording and grammar are authoritative only on docs.python.org.

### [9.1. Complete Python programs](https://docs.python.org/3/reference/toplevel_components.html#complete-python-programs)

- Canonical: **[9.1. Complete Python programs](https://docs.python.org/3/reference/toplevel_components.html#complete-python-programs)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

### [9.2. File input](https://docs.python.org/3/reference/toplevel_components.html#file-input)

- Canonical: **[9.2. File input](https://docs.python.org/3/reference/toplevel_components.html#file-input)** — definitions, judgments, and edge cases.
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

### [9.3. Interactive input](https://docs.python.org/3/reference/toplevel_components.html#interactive-input)

- Canonical: **[9.3. Interactive input](https://docs.python.org/3/reference/toplevel_components.html#interactive-input)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

### [9.4. Expression input](https://docs.python.org/3/reference/toplevel_components.html#expression-input)

- Canonical: **[9.4. Expression input](https://docs.python.org/3/reference/toplevel_components.html#expression-input)** — definitions, judgments, and edge cases.
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

- [9.1. Complete Python programs](complete-python-programs/index.md)
- [9.2. File input](file-input/index.md)
- [9.3. Interactive input](interactive-input/index.md)
- [9.4. Expression input](expression-input/index.md)
