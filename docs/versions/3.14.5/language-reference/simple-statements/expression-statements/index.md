# [7.1. Expression statements](https://docs.python.org/3/reference/simple_stmts.html#expression-statements)

Notes on **7.1. Expression statements** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#expression-statements).

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

Parent: [7. Simple statements](../index.md)
