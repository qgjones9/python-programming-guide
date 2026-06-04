# [4. Execution model](https://docs.python.org/3/reference/executionmodel.html)

Chapter **4. Execution model** describes how Python **runs** programs: what counts as a code block, how **names** are bound and resolved, how **exceptions** unwind control flow, and how the conceptual **runtime** maps onto host processes and threads. Normative grammar and statement forms live in other reference chapters; this one is the bridge between syntax and observable behavior. Full prose remains on [docs.python.org](https://docs.python.org/3/reference/executionmodel.html).

Related chapters: [Data model](../data-model/index.md) (objects and types), [The import system](../the-import-system/index.md) (module namespaces), [Compound statements](../compound-statements/index.md) (`try` / `except` / `finally`), and [Built-in exceptions](../../standard-library/built-in-exceptions/index.md) (exception classes).

---

## Chapter map

| Section | Topic |
|---------|--------|
| [4.1. Structure of a program](structure-of-a-program/index.md) | Code blocks, execution frames, and what “runs as a unit” |
| [4.2. Naming and binding](naming-and-binding/index.md) | Binding operations, scopes, `global` / `nonlocal`, annotation scopes |
| [4.3. Exceptions](exceptions/index.md) | Raising, handling, termination model, handler matching |
| [4.4. Runtime Components](runtime-components/index.md) | Host process/thread model and Python runtime layers |

---

## Cross-cutting ideas

| Idea | Summary |
|------|---------|
| **Code block** | Module body, class body, function body, interactive input, `-c` / `-m` scripts, and strings passed to `eval()` / `exec()` each form blocks executed in **frames**. |
| **Binding vs object** | Names refer to objects; assignment **binds** a name in a scope. Multiple names can alias one object. |
| **LEGB resolution** | Unqualified names resolve in the nearest enclosing scope (local → enclosing functions → global → builtins), with special rules for class bodies and annotation scopes. |
| **Termination exceptions** | Handlers can recover at an outer level but cannot “retry” the failing operation in place (except by re-entering from the top). |
| **Threads share process memory** | Python’s threading model assumes host threads in one process share resources; coordination is the programmer’s responsibility. |

```python
# Goal: a function body is its own block; outer names are resolved at runtime
counter = 0

def bump():
    global counter
    counter += 1

bump()
assert counter == 1
```

```python
# Goal: exception unwinds to the nearest matching handler
log = []

try:
    log.append("enter")
    raise ValueError("detected")
except ValueError as exc:
    log.append(type(exc).__name__)
finally:
    log.append("cleanup")

assert log == ["enter", "ValueError", "cleanup"]
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Using a name before binding in a function | `UnboundLocalError` if any assignment to that name exists in the block | Assign before use, or use `global` / `nonlocal` deliberately |
| Assuming class-body names are visible in methods | Class scope does not extend into method bodies (or most comprehensions there) | Use `self.attr`, defaults, or nested class / annotation-scope rules |
| Treating exception **messages** as API | Wording changes across Python versions | Catch by **type** (and attributes you document), not `str(exc)` |
| Sharing mutable globals across threads without locks | Nondeterministic corruption | Use `threading` locks, queues, or process isolation |
| Expecting `exec()` to see enclosing closures | Free variables resolve in **global** namespace for `exec` / `eval` | Pass explicit `globals` / `locals` dicts |

---

## Sections in this repo

- [4.1. Structure of a program](structure-of-a-program/index.md)
- [4.2. Naming and binding](naming-and-binding/index.md)
- [4.3. Exceptions](exceptions/index.md)
- [4.4. Runtime Components](runtime-components/index.md)
