# [7. Simple statements](https://docs.python.org/3/reference/simple_stmts.html)

Local notes for [**7. Simple statements**](https://docs.python.org/3/reference/simple_stmts.html) in *[The Python Language Reference](https://docs.python.org/3/reference/index.html)*. A *simple statement* fits on one logical line (several may share a line, separated by semicolons). Full grammar and edge cases remain authoritative on docs.python.org.

### [7.1. Expression statements](https://docs.python.org/3/reference/simple_stmts.html#expression-statements)

- An expression statement evaluates a *starred_expression* (often a single call or literal).
- Procedures are functions that return `None`; their calls are valid expression statements with no useful value.
- In the interactive interpreter, non-`None` results are printed via `repr()`; scripts do not auto-print expression results.

```python
# Expression statements run for side effects; the value is usually discarded.
log = []

def record(msg):
    log.append(msg)
    return None  # procedure-style call


record("ready")
assert log == ["ready"]

# Non-None values have a string form like the REPL would show.
assert repr(2 + 2) == "4"
```

### [7.2. Assignment statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements)

- `(target_list "=")+ expression` binds names or mutates attributes, subscriptions, and slices.
- Sequence unpacking requires matching arity; `*target` collects surplus items (PEP 3132).
- Overlapping targets in one statement are applied **left to right** — e.g. `i, x[i] = 1, 2` can surprise readers.
- See also [7.2.1 Augmented assignment](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) and [7.2.2 Annotated assignment](https://docs.python.org/3/reference/simple_stmts.html#annotated-assignment-statements) on the same page.

```python
# Basic binding and tuple unpacking.
a, b = 1, 2
assert (a, b) == (1, 2)

first, *middle, last = range(5)
assert first == 0 and middle == [1, 2, 3] and last == 4

# Left-to-right overlap within one target list (reference example).
x = [0, 1]
i = 0
i, x[i] = 1, 2
assert i == 1 and x == [0, 2]

# Augmented assignment evaluates the target once before the RHS.
nums = [1, 2, 3]
idx = 1
nums[idx] += 10
assert nums == [1, 12, 3]
```

### [7.3. The assert statement](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)

- `assert expr` is equivalent to `if __debug__: if not expr: raise AssertionError`.
- The two-expression form `assert expr1, expr2` supplies `AssertionError(expr2)` when the check fails.
- With `python -O`, assert statements are not emitted — do not rely on them for production invariants.

```python
# Passing checks do nothing; failures raise AssertionError (when __debug__ is True).
flag = True
assert flag
assert 1 + 1 == 2, "expected two"

errors = []
try:
    assert False, "boom"
except AssertionError as exc:
    errors.append(str(exc))
assert errors == ["boom"]
```

### [7.4. The pass statement](https://docs.python.org/3/reference/simple_stmts.html#the-pass-statement)

- `pass` is a null operation — syntactic filler where a statement is required.
- Common in empty function or class bodies until implementation arrives.

```python
# pass satisfies syntax without executing meaningful work.
def stub():
    pass


class Placeholder:
    pass


assert stub() is None
assert Placeholder.__name__ == "Placeholder"
```

### [7.5. The del statement](https://docs.python.org/3/reference/simple_stmts.html#the-del-statement)

- `del target_list` removes bindings or asks objects to delete attributes/items (like assignment, recursively).
- Deleting a name removes it from the local or global namespace; unbound names raise `NameError`.
- Since 3.2, deleting a name that is a free variable in a nested block is allowed when rules are met.

```python
# Delete keys and slice elements; delete a local name binding.
data = {"keep": 1, "drop": 2}
del data["drop"]
assert data == {"keep": 1}

row = [10, 20, 30]
del row[1]
assert row == [10, 30]

temp = object()
del temp
# temp is now unbound in this scope
```

### [7.6. The return statement](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement)

- `return` may appear only inside a function definition (not nested class bodies at module level rules).
- Bare `return` or `return` with no expression list yields `None`.
- In generators, `return value` finishes the iterator; `StopIteration.value` carries the value (3.3+).

```python
def add(a, b):
    return a + b


assert add(2, 3) == 5
def implicit_none():
    return


assert implicit_none() is None
```

### [7.7. The yield statement](https://docs.python.org/3/reference/simple_stmts.html#the-yield-statement)

- `yield_stmt` is semantically the same as a parenthesized yield *expression* statement.
- Using `yield` (or `yield from`) in a `def` makes that function a generator function.
- See [Yield expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions) for full semantics.

```python
def countdown(n):
    while n:
        yield n
        n -= 1


def flatten(nested):
    for part in nested:
        yield from part


assert list(countdown(3)) == [3, 2, 1]
assert list(flatten([[1, 2], [3]])) == [1, 2, 3]
```

### [7.8. The raise statement](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement)

- `raise` with no expression re-raises the active exception inside an `except` block.
- `raise exc from cause` sets explicit exception chaining (`__cause__`); `from None` suppresses context display.
- The first expression must be a `BaseException` subclass or instance.

```python
# Raise and catch a fresh exception.
try:
    raise ValueError("bad input")
except ValueError as exc:
    assert str(exc) == "bad input"

# Re-raise preserves the active exception after handling.
seen = []
try:
    try:
        raise KeyError("missing")
    except KeyError:
        seen.append("handled")
        raise
except KeyError:
    seen.append("propagated")
assert seen == ["handled", "propagated"]
```

### [7.9. The break statement](https://docs.python.org/3/reference/simple_stmts.html#the-break-statement)

- `break` exits the nearest enclosing `for` or `while` loop, skipping an optional `else` suite.
- If the loop target variable was bound by `for`, it keeps its value at the break point.
- A `finally` clause on an enclosing `try` runs before the loop is actually left.

```python
# break exits early; for-target keeps its last value.
total = 0
for n in range(10):
    if n == 5:
        last = n
        break
    total += n
assert total == 10 and last == 5
```

### [7.10. The continue statement](https://docs.python.org/3/reference/simple_stmts.html#the-continue-statement)

- `continue` skips the rest of the current loop body and starts the next iteration.
- Like `break`, it may appear only directly inside `for`/`while` (not inside nested defs in the loop).
- Enclosing `try`/`finally` still runs the `finally` suite before the next cycle begins.

```python
# continue skips to the next iteration without finishing the body.
evens = []
for n in range(6):
    if n % 2:
        continue
    evens.append(n)
assert evens == [0, 2, 4]
```

### [7.11. The import statement](https://docs.python.org/3/reference/simple_stmts.html#the-import-statement)

- `import mod [as name]` finds/loads a module, then binds name(s) in the current namespace (like assignment).
- `from pkg import attr` loads `pkg`, resolves `attr` (possibly via submodule import), then binds locally.
- `from __future__ import …` is a compile-time *future statement* (see §7.11.1 on the canonical page).

```python
# import and from-import bind names in the current namespace.
import json as j

assert j.dumps([1]) == "[1]"

from collections import deque

d = deque([1, 2])
d.append(3)
assert list(d) == [1, 2, 3]
```

### [7.12. The global statement](https://docs.python.org/3/reference/simple_stmts.html#the-global-statement)

- `global name` declares that assignments to `name` refer to the module-global binding in this scope.
- The declaration applies to the whole function/class body; use-before-declare raises `SyntaxError`.
- `global` is a parser directive — it does not affect code compiled via `exec()` from another scope.

```python
# global allows rebinding a module-level name from inside a function.
counter = 0


def bump(steps=1):
    global counter
    counter += steps


bump(2)
assert counter == 2
```

### [7.13. The nonlocal statement](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement)

- `nonlocal name` binds assignments to the nearest enclosing function scope (not globals).
- If no enclosing binding exists, `SyntaxError` is raised at compile time.
- Like `global`, it applies to the entire function body and is a parser directive.

```python
def make_counter(start=0):
    count = start

    def inc():
        nonlocal count
        count += 1
        return count

    return inc


step = make_counter(10)
assert step() == 11 and step() == 12
```

### [7.14. The type statement](https://docs.python.org/3/reference/simple_stmts.html#the-type-statement)

- `type Name = expression` declares a type alias (`typing.TypeAliasType`), added in Python 3.12 (PEP 695).
- The RHS is evaluated lazily when `Name.__value__` is accessed (annotation scope).
- `type` is a soft keyword; generic aliases add a type parameter list after the name.

```python
# type aliases are TypeAliasType instances with lazy __value__.
type Point = tuple[float, float]

assert Point.__name__ == "Point"
assert Point.__value__ == tuple[float, float]

type IntMap = dict[str, int]
assert IntMap.__value__ == dict[str, int]
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
