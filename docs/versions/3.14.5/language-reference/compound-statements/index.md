# [Compound statements](https://docs.python.org/3/reference/compound_stmts.html)

**Compound statements** group other statements and control how those inner statements run: conditional branches (`if`), loops (`while`, `for`), resource management (`with`), exception handling (`try`), structural pattern matching (`match`), and definitions that create callable or class objects (`def`, `class`, `async def`). Each compound form is built from one or more **clauses** (header keyword + colon + **suite**). Normative grammar and edge cases live on [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html); this hub orients you to each construct and links to deeper notes in this repo.

Related chapters: [Boolean operations](../expressions/boolean-operations/index.md) (truth tests in `if`/`while`), [Assignment statements](../simple-statements/assignment-statements/index.md) (`for` targets), [Exceptions](../execution-model/exceptions/index.md) (`try` / `raise`), [The raise statement](../simple-statements/the-raise-statement/index.md), [With Statement Context Managers](https://docs.python.org/3/library/stdtypes.html#context-manager-types) (stdlib protocol).

---

## Statement overview

| Construct | Role |
|-----------|------|
| [`if`](the-if-statement/index.md) | Run exactly one suite from `if` / `elif` / `else` |
| [`while`](the-while-statement/index.md) | Repeat a suite while a condition is true |
| [`for`](the-for-statement/index.md) | Iterate an iterable; optional `else` when not broken |
| [`try`](the-try-statement/index.md) | Handle exceptions, run `else` / `finally`, or `except*` groups |
| [`with`](the-with-statement/index.md) | Enter/exit context managers (sync or `async with`) |
| [`match`](the-match-statement/index.md) | Structural pattern matching (3.10+) |
| [`def`](function-definitions/index.md) | Bind a function object; decorators, defaults, annotations |
| [`class`](class-definitions/index.md) | Create a class object from a suite and bases |
| [Coroutines](coroutines/index.md) | `async def`, `async for`, `async with` |
| [Type parameter lists](type-parameter-lists/index.md) | Generic `def` / `class` / `type` syntax (3.12+) |
| [Annotations](annotations/index.md) | Parameter, return, and variable annotations |

---

## Clause and suite structure

| Term | Meaning |
|------|---------|
| **Clause** | Header (`if`, `for`, `try`, …) ending with `:` at one indentation level |
| **Suite** | Statements controlled by the clause: same-line simple statements after `:`, or an indented block |
| **Nested compound** | Only the indented suite form may contain another compound statement |

Semicolons on one line bind tighter than the colon: in `if x: print(a); print(b)`, both prints are in the `if` suite when the condition is true.

```python
# Goal: one-line suite vs indented nested if (else attaches to inner if)
def nested_else(x):
    if x > 0:
        if x < 10:
            return "small"
        else:
            return "large-nonpositive"
    return "nonpositive"


assert nested_else(5) == "small"
assert nested_else(15) == "large-nonpositive"
```

---

## Choosing the right construct

| Goal | Prefer |
|------|--------|
| Pick one branch among many tests | `if` / `elif` / `else` |
| Repeat until a condition fails | `while` (+ optional `else`) |
| Walk every item of an iterable | `for` (+ optional `else`) |
| Handle errors or guarantee cleanup | `try` / `except` / `finally` (or `except*` for groups) |
| Acquire/release resources | `with` or `async with` |
| Destructure by shape/type | `match` / `case` |
| Reusable callable | `def` or `async def` |
| New type with shared/class state | `class` |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Indent `else` with the `if` it belongs to | Avoids the classic “dangling else” ambiguity |
| Treat `for`/`while` `else` as “completed without `break`” | `else` does not run after `break` |
| Use `None` defaults for mutable parameters | Default expressions run once at function definition time |
| Prefer `with` over manual `try`/`finally` for resources | Documents enter/exit protocol clearly |
| Put irrefutable `match` cases last | At most one catch-all `case _` without a guard |
| Inspect generics via `__type_params__` at runtime | Type parameter names are not module globals |

```python
# Goal: for-else runs only when loop completes without break
def classify(items, bad):
    for item in items:
        if item == bad:
            break
    else:
        return "all_ok"
    return "stopped_early"


assert classify([1, 2, 3], 99) == "all_ok"
assert classify([1, 2, 3], 2) == "stopped_early"
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `if` on one line with `;` and nested `if` | `else` may bind to the wrong `if` | Use indented blocks for nested conditionals |
| Mutable default arguments | Shared list/dict across calls | Default to `None`, allocate in the body |
| `return` in `finally` | Overrides `try`/`except` return value | Avoid returning from `finally` (3.14+ warns) |
| Relying on bindings after failed `match` | Implementation may optimize evaluation | Only use names from the selected `case` |
| `except*` with `BaseExceptionGroup` subclass | `TypeError` — ambiguous semantics | Match concrete exception types |
| Assuming annotation expressions run at definition | Lazy evaluation by default (3.14+) | Use `annotationlib` / `typing.get_type_hints` |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [The if statement](the-if-statement/index.md) | `if` / `elif` / `else`, assignment expressions in headers |
| [The while statement](the-while-statement/index.md) | Condition loop, `break` / `continue`, `else` |
| [The for statement](the-for-statement/index.md) | Iteration, target assignment, starred `in` items |
| [The try statement](the-try-statement/index.md) | `except`, `except*`, `else`, `finally` |
| [The with statement](the-with-statement/index.md) | Context managers, multi-item `with` |
| [The match statement](the-match-statement/index.md) | Patterns, guards, irrefutable cases |
| [Function definitions](function-definitions/index.md) | `def`, decorators, parameters, defaults |
| [Class definitions](class-definitions/index.md) | `class`, bases, metaclass hooks, decorators |
| [Coroutines](coroutines/index.md) | `async def`, `async for`, `async with` |
| [Type parameter lists](type-parameter-lists/index.md) | `TypeVar`, `TypeVarTuple`, `ParamSpec` |
| [Annotations](annotations/index.md) | Lazy annotations, `__future__` strings |
