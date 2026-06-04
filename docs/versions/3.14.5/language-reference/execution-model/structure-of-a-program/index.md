# [4.1. Structure of a program](https://docs.python.org/3/reference/executionmodel.html#structure-of-a-program)

A Python program is built from **code blocks**—text executed as a unit. Each block runs inside an **execution frame** that holds administrative data (for debuggers) and defines how control continues after the block finishes. This section does not define statement syntax; it explains what the interpreter treats as one runnable chunk. Authoritative detail: [Structure of a program](https://docs.python.org/3/reference/executionmodel.html#structure-of-a-program).

Parent: [4. Execution model](../index.md)

---

## What counts as a code block

| Construct | Block? | Notes |
|-----------|--------|-------|
| Module (imported or `__main__`) | Yes | Top-level statements run at import or script start |
| Function / async function body | Yes | Parameters bound when the function is called |
| Class body | Yes | Executed at class creation time; namespace becomes the class dict |
| Interactive REPL input | Yes | Each submitted statement sequence |
| Script file (`python file.py`, stdin script) | Yes | One file’s top-level block |
| `python -c '…'` | Yes | Command-line script block |
| `python -m pkg` (`__main__`) | Yes | Module run as top-level script |
| String to `eval()` / `exec()` | Yes | Compiled and executed in a fresh frame context |

```python
# Goal: function body is a nested block; module-level binding is visible
module_flag = "outer"

def inner():
    return module_flag

assert inner() == "outer"
```

```python
# Goal: exec() runs a string as its own code block in caller namespaces
ns = {"x": 1}
exec("x += 1", ns)
assert ns["x"] == 2
```

---

## Execution frames

| Role | Behavior |
|------|----------|
| **Administrative info** | Supports tracebacks, profilers, and debuggers (filename, line numbers, locals snapshot semantics) |
| **Continuation** | Determines where execution resumes after the block completes (return, exception, or fall-through) |
| **Nesting** | Calling a function pushes a new frame; returning or raising pops it |

```python
# Goal: return exits the function's block; caller's frame continues
trail = []

def callee():
    trail.append("callee")
    return 99

def caller():
    trail.append("before")
    value = callee()
    trail.append("after")
    return value

assert caller() == 99
assert trail == ["before", "callee", "after"]
```

---

## Relationship to other chapters

| Topic | Where to read next |
|-------|-------------------|
| Import runs a module block once | [The import system](../../the-import-system/index.md) |
| `class` and `def` compound statements | [Compound statements](../../compound-statements/index.md) |
| Objects created while a block runs | [Data model](../../data-model/index.md) |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Side effects at **import** time | Module block runs on first import; globals persist in `sys.modules` | Keep module top level idempotent; use `if __name__ == "__main__"` for scripts |
| Assuming `exec` shares function locals | `exec` uses provided dicts; does not automatically see closure cells | Pass an explicit namespace or refactor into a real function |
| Editing a running `.py` file | Already-imported module block is not re-run until reload | Use `importlib.reload` knowing its limits |
