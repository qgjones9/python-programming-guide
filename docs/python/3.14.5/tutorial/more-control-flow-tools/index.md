# [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html)

Condensed notes for [chapter 4 of the Python Tutorial](https://docs.python.org/3/tutorial/controlflow.html): `if`/`for`/`while`, `range`, loop control, `match`, functions (defaults, keywords, `*`/`**`, special parameter forms, lambdas, docstrings, annotations), and a pointer to style (PEP 8). For full explanations and examples, follow the heading link.

### 4.1 — `if` statements

- `if` / `elif` / `else`: zero or more `elif` branches; `else` is optional. `elif` avoids extra nesting compared to chained `if` / `else`.
- For many constant comparisons or structural tests, **`match`** is often clearer (see §4.7).

```python
def classify(x: int) -> str:
    if x < 0:
        return "negative"
    elif x == 0:
        return "zero"
    elif x == 1:
        return "one"
    else:
        return "many"


assert classify(-1) == "negative" and classify(0) == "zero" and classify(5) == "many"
```

### 4.2 — `for` statements

- `for` iterates over **items of a sequence** (list, string, etc.), not only numeric ranges.
- **Do not mutate a collection while iterating over it**; iterate over a **copy** or build a **new** collection.

```python
words = ["cat", "window", "defenestrate"]
lengths = [len(w) for w in words]
assert lengths == [3, 6, 12]

users = {"Hans": "active", "Éléonore": "inactive", "景太郎": "active"}
for user, status in users.copy().items():
    if status == "inactive":
        del users[user]
assert set(users) == {"Hans", "景太郎"}

active_users = {u: s for u, s in users.items() if s == "active"}
assert active_users == {"Hans": "active", "景太郎": "active"}
```

### 4.3 — The `range()` function

- `range(stop)`, `range(start, stop)`, `range(start, stop, step)`; the **end value is excluded**.
- `range` returns a **compact iterable**, not a pre-built list; pair with `list()` when you need materialization.
- Prefer **`enumerate()`** over `range(len(seq))` when you need both index and value.

```python
assert list(range(5)) == [0, 1, 2, 3, 4]
assert list(range(5, 10)) == [5, 6, 7, 8, 9]
assert list(range(0, 10, 3)) == [0, 3, 6, 9]
assert sum(range(4)) == 6

a = ["Mary", "had", "a", "little", "lamb"]
indexed = list(enumerate(a))
assert indexed[0] == (0, "Mary")
```

### 4.4 — `break` and `continue`

- **`break`** leaves the innermost enclosing `for` or `while`.
- **`continue`** skips to the **next iteration** of the innermost loop.

```python
# break: first factor found
out = []
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            out.append((n, x, n // x))
            break
assert (4, 2, 2) in out

# continue: skip to next iteration when even
lines = []
for num in range(2, 10):
    if num % 2 == 0:
        lines.append(f"even:{num}")
        continue
    lines.append(f"odd:{num}")
assert lines[0] == "even:2" and lines[1] == "odd:3"
```

### 4.5 — `else` clauses on loops

- On **`for` / `while`**, `else` runs when the loop **completes without `break`**. If `break` runs, the loop’s `else` is skipped (unlike `if`/`else` pairing visually with nearby `if`).

```python
def primes_up_to(limit: int) -> list[int]:
    found = []
    for n in range(2, limit):
        for x in range(2, n):
            if n % x == 0:
                break
        else:
            found.append(n)
    return found


assert primes_up_to(10) == [2, 3, 5, 7]
```

### 4.6 — `pass` statements

- **`pass`** is a no-op: holds syntactic place for empty bodies (loops, classes, stubs). **`...`** (Ellipsis) is a conventional placeholder but is just another expression value.

```python
class Empty:
    pass


def todo():
    ...  # or pass


assert Empty is not None and todo() is None
```

### 4.7 — `match` statements

- **`match` / `case`**: first matching pattern wins; **captures** bind parts of the subject; **`_`** is a wildcard. Supports guards (`if`), `|`, sequences, mappings, class patterns, and more (see **PEP 636**).

```python
def http_error(status: int) -> str:
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case _:
            return "other"


assert http_error(404) == "Not found"

point = (0, 5)
match point:
    case (0, 0):
        label = "origin"
    case (0, y):
        label = f"on_y_axis:{y}"
    case (x, 0):
        label = f"on_x_axis:{x}"
    case (x, y):
        label = f"point:{x},{y}"
    case _:
        label = "unknown"
assert label == "on_y_axis:5"
```

### 4.8 — Defining functions

- **`def`** introduces a name, parameters, and an indented body. Optional first-string literal is a **docstring**.
- Locals live in a **new scope** per call; arguments are **names bound to passed objects** (shared mutables are visible to caller).
- **`return`** sends a value back; omitting it (or bare `return`) yields **`None`**.

```python
def fib2(n: int) -> list[int]:
    """Return Fibonacci numbers strictly less than n."""
    result: list[int] = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result


assert fib2(100) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
alias = fib2
assert alias(10) == fib2(10)
```

### 4.9 — More on defining functions

#### Default argument values

- Defaults are evaluated **once** at **function definition** time (in the defining scope), not per call.
- **Never use a mutable literal** (`[]`, `{}`, …) as a default; use **`None`** and assign a fresh container in the body.

```python
i = 5


def f(arg=i):
    return arg


i = 6
assert f() == 5


def bad_accum(x, acc=[]):  # intentional anti-pattern for illustration
    acc.append(x)
    return list(acc)


first = bad_accum(1)
second = bad_accum(2)
assert first == [1] and second == [1, 2]  # same list reused


def good_accum(x, acc=None):
    if acc is None:
        acc = []
    acc.append(x)
    return list(acc)


assert good_accum(1) == [1] and good_accum(2) == [2]
```

#### Keyword arguments and `*` / `**`

- Callers may pass **`name=value`**; keywords must follow positional args and cannot duplicate a parameter.
- **`*args`** collects extra positional arguments; **`**kwargs`** collects extra keywords into a **`dict`**.

```python
def record(a, *args, **kwargs):
    return a, args, kwargs


assert record(1, 2, 3, x=4) == (1, (2, 3), {"x": 4})


def parrot(voltage, state="a stiff", action="voom"):
    return voltage, state, action


assert parrot(1000) == (1000, "a stiff", "voom")
assert parrot(voltage=1000) == (1000, "a stiff", "voom")
assert parrot("high", state="still") == ("high", "still", "voom")
```

#### Special parameters (`/`, `*`)

- **`/`** (before it): **positional-only** — cannot be passed by keyword.
- **`*`** alone before a parameter: everything after is **keyword-only**.

```python
def standard_arg(arg):
    return arg


assert standard_arg(2) == standard_arg(arg=2)


def pos_only(arg, /):
    return arg


assert pos_only(3) == 3


def kwd_only(*, arg):
    return arg


assert kwd_only(arg=4) == 4


def combined(pos_only, /, standard, *, kwd_only):
    return pos_only, standard, kwd_only


assert combined(1, 2, kwd_only=3) == (1, 2, 3)


def foo(name, /, **kwds):
    return "name" in kwds


assert foo(1, **{"name": 2}) is True
```

#### Arbitrary argument lists and unpacking

- **`*args`** in the definition “scoops” remaining positionals; parameters after `*args` are keyword-only.
- In a **call**, `*iterable` and `**dict` unpack into positionals and keywords.

```python
def concat(*args, sep="/"):
    return sep.join(args)


assert concat("earth", "mars", "venus") == "earth/mars/venus"
assert concat("earth", "mars", "venus", sep=".") == "earth.mars.venus"

args = [3, 6]
assert list(range(*args)) == [3, 4, 5]


def parrot2(voltage, state="x", action="y"):
    return voltage, state, action


d = {"voltage": "four million", "state": "gone", "action": "VOOM"}
assert parrot2(**d) == ("four million", "gone", "VOOM")
```

#### Lambda expressions

- **`lambda`**: small anonymous **single-expression** functions; often used as **`key=`** for `sort` / `sorted`.

```python
def make_incrementor(n):
    return lambda x: x + n


f = make_incrementor(42)
assert f(0) == 42 and f(1) == 43

pairs = [(1, "one"), (2, "two"), (3, "three")]
pairs.sort(key=lambda p: p[1])
assert pairs[0][1] == "one" and pairs[-1][1] == "two"
```

#### Documentation strings

- First line: short summary; if more lines follow, leave a **blank line** after the summary. The parser **strips common leading indentation** from docstrings.

```python
def documented():
    """Return None.

    Longer description after a blank line.
    """
    return None


assert documented.__doc__.startswith("Return None.")
```

#### Function annotations

- Annotations are **metadata** stored in **`__annotations__`**; they do not change runtime behavior unless you use a tool that reads them (e.g. type checkers).

```python
def annotated(ham: str, eggs: str = "eggs") -> str:
    return ham + " and " + eggs


assert annotated.__annotations__["ham"] is str
assert annotated("spam") == "spam and eggs"
```

### 4.10 — Intermezzo: coding style

- **[PEP 8](https://peps.python.org/pep-0008/)** is the usual style guide: **4 spaces**, no tabs for indentation; wrap near **79** characters for code (72 for flowing text in docstrings, per PEP 8); blank lines between top-level defs/classes; **`UpperCamelCase`** classes, **`lowercase_with_underscores`** functions; spaces around operators; prefer **UTF-8** / ASCII identifiers for wide collaboration.

```python
class StyleDemo:
    """Docstring uses UpperCamelCase for the class name in prose, not the code."""

    def example_method(self) -> None:
        a = max(1, 2) + 3  # spaces around `=` and binary ops
        assert a == 5
```

## Sections in this repo

- [if Statements](if-statements/index.md)
- [for Statements](for-statements/index.md)
- [The range() Function](the-range-function/index.md)
- [break and continue Statements](break-and-continue-statements/index.md)
- [else Clauses on Loops](else-clauses-on-loops/index.md)
- [pass Statements](pass-statements/index.md)
- [match Statements](match-statements/index.md)
- [Defining Functions](defining-functions/index.md)
- [More on Defining Functions](more-on-defining-functions/index.md)
  - [Default Argument Values](more-on-defining-functions/default-argument-values/index.md)
  - [Keyword Arguments](more-on-defining-functions/keyword-arguments/index.md)
  - [Special parameters](more-on-defining-functions/special-parameters/index.md) — [Positional-or-Keyword Arguments](more-on-defining-functions/special-parameters/positional-or-keyword-arguments/index.md), [Positional-Only Parameters](more-on-defining-functions/special-parameters/positional-only-parameters/index.md), [Keyword-Only Arguments](more-on-defining-functions/special-parameters/keyword-only-arguments/index.md), [Function Examples](more-on-defining-functions/special-parameters/function-examples/index.md), [Recap](more-on-defining-functions/special-parameters/recap/index.md)
  - [Arbitrary Argument Lists](more-on-defining-functions/arbitrary-argument-lists/index.md)
  - [Unpacking Argument Lists](more-on-defining-functions/unpacking-argument-lists/index.md)
  - [Lambda Expressions](more-on-defining-functions/lambda-expressions/index.md)
  - [Documentation Strings](more-on-defining-functions/documentation-strings/index.md)
  - [Function Annotations](more-on-defining-functions/function-annotations/index.md)
- [Intermezzo: Coding Style](intermezzo-coding-style/index.md)


Next: [Data Structures](../data-structures/index.md)