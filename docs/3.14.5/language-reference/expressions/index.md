# [6. Expressions](https://docs.python.org/3/reference/expressions.html)

Local notes for [**6. Expressions**](https://docs.python.org/3/reference/expressions.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. This mirror is shorthand; wording and grammar are authoritative only on docs.python.org.

### [6.1. Arithmetic conversions](https://docs.python.org/3/reference/expressions.html#arithmetic-conversions)

- Canonical: **[6.1. Arithmetic conversions](https://docs.python.org/3/reference/expressions.html#arithmetic-conversions)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Indentation defines blocks; only the reference is normative for edge cases.
def ok():
    return True


assert ok() is True
```

### [6.2. Atoms](https://docs.python.org/3/reference/expressions.html#atoms)

- Canonical: **[6.2. Atoms](https://docs.python.org/3/reference/expressions.html#atoms)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

### [6.3. Primaries](https://docs.python.org/3/reference/expressions.html#primaries)

- Canonical: **[6.3. Primaries](https://docs.python.org/3/reference/expressions.html#primaries)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

### [6.4. Await expression](https://docs.python.org/3/reference/expressions.html#await-expression)

- Canonical: **[6.4. Await expression](https://docs.python.org/3/reference/expressions.html#await-expression)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

### [6.5. The power operator](https://docs.python.org/3/reference/expressions.html#the-power-operator)

- Canonical: **[6.5. The power operator](https://docs.python.org/3/reference/expressions.html#the-power-operator)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

### [6.6. Unary arithmetic and bitwise operations](https://docs.python.org/3/reference/expressions.html#unary-arithmetic-and-bitwise-operations)

- Canonical: **[6.6. Unary arithmetic and bitwise operations](https://docs.python.org/3/reference/expressions.html#unary-arithmetic-and-bitwise-operations)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Expressions may nest; parentheses override default precedence safely.
base, exp = 2, 8
assert (base ** exp) == 256
```

### [6.7. Binary arithmetic operations](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)

- Canonical: **[6.7. Binary arithmetic operations](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)** — definitions, judgments, and edge cases.
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

### [6.8. Shifting operations](https://docs.python.org/3/reference/expressions.html#shifting-operations)

- Canonical: **[6.8. Shifting operations](https://docs.python.org/3/reference/expressions.html#shifting-operations)** — definitions, judgments, and edge cases.
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

### [6.9. Binary bitwise operations](https://docs.python.org/3/reference/expressions.html#binary-bitwise-operations)

- Canonical: **[6.9. Binary bitwise operations](https://docs.python.org/3/reference/expressions.html#binary-bitwise-operations)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Data model: double-underscore methods intercept builtins when defined.
class C:
    def __len__(self):
        return 0


assert len(C()) == 0
```

### [6.10. Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)

- Canonical: **[6.10. Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Parentheses alter evaluation order versus default precedence.
assert (1 + 2) * 3 == 9  # grouped addition first
assert 1 + 2 * 3 == 7  # multiplication binds tighter without parens
```

### [6.11. Boolean operations](https://docs.python.org/3/reference/expressions.html#boolean-operations)

- Canonical: **[6.11. Boolean operations](https://docs.python.org/3/reference/expressions.html#boolean-operations)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [6.12. Assignment expressions](https://docs.python.org/3/reference/expressions.html#assignment-expressions)

- Canonical: **[6.12. Assignment expressions](https://docs.python.org/3/reference/expressions.html#assignment-expressions)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [6.13. Conditional expressions](https://docs.python.org/3/reference/expressions.html#conditional-expressions)

- Canonical: **[6.13. Conditional expressions](https://docs.python.org/3/reference/expressions.html#conditional-expressions)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

### [6.14. Lambdas](https://docs.python.org/3/reference/expressions.html#lambda)

- Canonical: **[6.14. Lambdas](https://docs.python.org/3/reference/expressions.html#lambda)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [6.15. Expression lists](https://docs.python.org/3/reference/expressions.html#expression-lists)

- Canonical: **[6.15. Expression lists](https://docs.python.org/3/reference/expressions.html#expression-lists)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Containers compare element-wise per reference rules once types align.
assert (1, 2) < (1, 3)
```

### [6.16. Evaluation order](https://docs.python.org/3/reference/expressions.html#evaluation-order)

- Canonical: **[6.16. Evaluation order](https://docs.python.org/3/reference/expressions.html#evaluation-order)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# import forms create module bindings (see import system chapter for loaders).
import json as j
assert j.dumps([0]) == "[0]"
```

### [6.17. Operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)

- Canonical: **[6.17. Operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)** — definitions, judgments, and edge cases.
- Other Python implementations may differ unless they claim compliance; settle disputes against CPython docs.
- Prefer the linked anchors when bisecting language changes across minor versions.

```python
# Names bind to objects; multiple names may reference the same value (aliases).
nums = []
alias = nums
alias.append(1)
assert nums == [1]
```

## Sections in this repo

- [6.1. Arithmetic conversions](arithmetic-conversions/index.md)
- [6.2. Atoms](atoms/index.md)
- [6.3. Primaries](primaries/index.md)
- [6.4. Await expression](await-expression/index.md)
- [6.5. The power operator](the-power-operator/index.md)
- [6.6. Unary arithmetic and bitwise operations](unary-arithmetic-and-bitwise-operations/index.md)
- [6.7. Binary arithmetic operations](binary-arithmetic-operations/index.md)
- [6.8. Shifting operations](shifting-operations/index.md)
- [6.9. Binary bitwise operations](binary-bitwise-operations/index.md)
- [6.10. Comparisons](comparisons/index.md)
- [6.11. Boolean operations](boolean-operations/index.md)
- [6.12. Assignment expressions](assignment-expressions/index.md)
- [6.13. Conditional expressions](conditional-expressions/index.md)
- [6.14. Lambdas](lambda/index.md)
- [6.15. Expression lists](expression-lists/index.md)
- [6.16. Evaluation order](evaluation-order/index.md)
- [6.17. Operator precedence](operator-precedence/index.md)
