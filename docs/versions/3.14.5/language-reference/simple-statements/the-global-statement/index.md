# [7.12. The global statement](https://docs.python.org/3/reference/simple_stmts.html#the-global-statement)

Notes on **7.12. The global statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-global-statement).

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

Parent: [7. Simple statements](../index.md)
