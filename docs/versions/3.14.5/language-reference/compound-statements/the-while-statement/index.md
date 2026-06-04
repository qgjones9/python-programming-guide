# [The while statement](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)

The **`while` statement** repeats its suite while the header **assignment expression** evaluates to true. On the first false result, the loop ends and the optional **`else` suite** runs (unless the loop exited via **`break`**). **`continue`** skips the rest of the current iteration and re-tests the condition. Normative details: [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement).

Parent: [Compound statements](../index.md)

---

## Grammar and control flow

| Piece | Role |
|-------|------|
| `while assignment_expression :` | Re-test before each iteration |
| `else :` | Runs when the condition becomes false without `break` |
| `break` | Exit loop immediately; skip `else` |
| `continue` | Jump to next condition test |

```ebnf
while_stmt ::= "while" assignment_expression ":" suite
               ["else" ":" suite]
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Ensure the condition eventually becomes false | Avoid unintentional infinite loops |
| Use `for` when iterating a known iterable | Clearer and often faster than manual indexing |
| Put loop-invariant work outside the `while` | Avoid redundant computation each iteration |
| Document intentional “infinite” loops with `while True` + `break` | Signals exit is internal (event loop, server) |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Expecting `else` after `break` | `else` is for normal completion only | Same rule as `for` loops |
| Mutating data tested in the condition | Skipped iterations or extra iterations | Copy or re-fetch the tested value explicitly |
| `continue` in `finally` | Was illegal before 3.8; still easy to misuse | Prefer restructuring the loop body |
| Heavy work in the condition expression | Runs every iteration | Bind once with walrus or a variable before the loop |

```python
# Goal: while-else runs when condition goes false without break
def drain(queue, limit):
    count = 0
    while queue:
        queue.pop(0)
        count += 1
        if count >= limit:
            break
    else:
        return "emptied"
    return "capped"


q = [1, 2, 3]
assert drain(list(q), 10) == "emptied"
assert drain(list(q), 2) == "capped"
```

```python
# Goal: continue skips to next condition test
total = 0
n = 0
while n < 6:
    n += 1
    if n % 2 == 0:
        continue
    total += n
assert total == 9  # 1 + 3 + 5
```
