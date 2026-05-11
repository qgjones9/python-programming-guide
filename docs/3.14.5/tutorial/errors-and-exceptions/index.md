# [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)

Condensed notes for [chapter 8 — Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html): parse-time **syntax errors**, runtime **exceptions**, **`try` / `except` / `else` / `finally`**, **`raise`**, explicit chaining (**`from`**), defining your own types, and **`with`** for cleanup. For **`input()`**-driven examples from the official text, open the linked sections.

### 8.1 — [Syntax Errors](https://docs.python.org/3/tutorial/errors.html#syntax-errors)

- The parser reports the **filename**, **line**, and a caret region; the caret is not always where you should edit if the real issue is a missing **`:`** or parenthesis earlier.

```python
import ast

# `compile`/`ast.parse` turn source into bytecode/AST — invalid syntax raises SyntaxError.
bad = "while True print('nope')"
try:
    ast.parse(bad)
except SyntaxError as e:
    assert e.lineno == 1
```

### 8.2 — [Exceptions](https://docs.python.org/3/tutorial/errors.html#exceptions)

- Even valid syntax can fail at runtime (**`TypeError`**, **`ValueError`**, **`ZeroDivisionError`**, …). The last line of a traceback names the **exception type** and message.

```python
try:
    _ = 1 / 0
except ZeroDivisionError as err:
    # str(err) is the human-readable detail after the colon in tracebacks
    assert "division by zero" in str(err).lower()
```

### 8.3 — [Handling Exceptions](https://docs.python.org/3/tutorial/errors.html#handling-exceptions)

- **`except E`** matches **`E`** and **any subclass** of **`E`**; put **`except Exception`** **after** specific types, never before them.
- **`try` … `else`** runs when the **`try`** suite finishes **without** raising—use it so normal post-success work does not live inside **`try`** (avoid catching bugs you did not intend to handle).

```python
def parse_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        # Re-raise to let callers decide policy (log, prompt, substitute default, …).
        raise


assert parse_int("7") == 7
try:
    parse_int("x")
except ValueError:
    pass
```

### 8.4 — [Raising Exceptions](https://docs.python.org/3/tutorial/errors.html#raising-exceptions)

- **`raise`** targets an **instance** or a **class** (implicitly called with no args). Inside **`except`**, bare **`raise`** propagates the caught exception unchanged.

```python
def must_positive(x: int) -> None:
    if x <= 0:
        raise ValueError  # same class object as `raise ValueError()` here


try:
    must_positive(0)
except ValueError:
    pass
```

### 8.5 — [Exception Chaining](https://docs.python.org/3/tutorial/errors.html#exception-chaining)

- **`raise New from old`** sets **`__cause__`** for “direct cause” tracebacks. **`raise New from None`** hides the original context when you intentionally replace errors at a boundary.

```python
def boundary() -> None:
    try:
        raise OSError("low-level")
    except OSError:
        raise RuntimeError("high-level") from None


try:
    boundary()
except RuntimeError as e:
    assert e.__cause__ is None  # `from None` suppresses chaining metadata
```

### 8.6 — [User-defined Exceptions](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions)

- Subclass **`Exception`** (not **`BaseException`**) for recoverable application errors; store details on **`self`** or rely on **`BaseException.args`**.

```python
class DomainError(Exception):
    """Tiny example of a typed error for one API surface."""


try:
    raise DomainError("bad state")
except DomainError as e:
    assert e.args == ("bad state",)
```

### 8.7 — [Defining Clean-up Actions](https://docs.python.org/3/tutorial/errors.html#defining-clean-up-actions)

- **`finally`** always runs when leaving the **`try`** construct (after **`try`**, **`except`**, or **`else`**), and is the right place for **must-run** teardown—**but** prefer **`with`** for objects that already implement context managers.

```python
state = {"ran": False}

try:
    try:
        raise ValueError  # exception still propagates after `finally` runs
    finally:
        state["ran"] = True
except ValueError:
    pass

assert state["ran"] is True
```

### 8.8 — [Predefined Clean-up Actions](https://docs.python.org/3/tutorial/errors.html#predefined-clean-up-actions)

- Objects with **`__enter__` / `__exit__`** (or **`contextlib.contextmanager`**) support **`with`**, guaranteeing **`__exit__`** is called even when the suite raises.

```python
from contextlib import contextmanager


@contextmanager
def demo():
    yield 1


with demo() as x:
    assert x == 1
```

### Raising and handling multiple unrelated exceptions

- **`ExceptionGroup`** / **`BaseExceptionGroup`** (3.11+) bundle several errors raised together; **`except*`** matches contained exceptions. See the official subsection and [PEP 654](https://peps.python.org/pep-0654/).

```python
# ExceptionGroup bundles several errors; iterate `.exceptions` or use `except*` (3.11+).
eg = ExceptionGroup("many", [ValueError("a"), TypeError("b")])
assert len(eg.exceptions) == 2
assert isinstance(eg.exceptions[0], ValueError)
```

### Enriching exceptions with notes

- **`Exception.add_note()`** attaches free-form text shown at the end of tracebacks (useful when re-raising after adding context).

```python
err = RuntimeError("root")
err.add_note("happened during step 2")
assert "step 2" in str(err.__notes__[0])
```

## Sections in this repo

- [Syntax Errors](syntax-errors/index.md)
- [Exceptions](exceptions/index.md)
- [Handling Exceptions](handling-exceptions/index.md)
- [Raising Exceptions](raising-exceptions/index.md)
- [Exception Chaining](exception-chaining/index.md)
- [User-defined Exceptions](user-defined-exceptions/index.md)
- [Defining Clean-up Actions](defining-clean-up-actions/index.md)
- [Predefined Clean-up Actions](predefined-clean-up-actions/index.md)
- [Raising and Handling Multiple Unrelated Exceptions](raising-and-handling-multiple-unrelated-exceptions/index.md)
- [Enriching exceptions with notes](enriching-exceptions-with-notes/index.md)

Next: [Classes](../classes/index.md)
