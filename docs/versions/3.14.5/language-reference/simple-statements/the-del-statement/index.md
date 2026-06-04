# [7.5. The del statement](https://docs.python.org/3/reference/simple_stmts.html#the-del-statement)

Notes on **7.5. The del statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-del-statement).

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

Parent: [7. Simple statements](../index.md)
