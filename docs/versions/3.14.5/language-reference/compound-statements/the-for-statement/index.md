# [The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)

The **`for` statement** iterates over an **iterable**: the `in` expression is evaluated once, an iterator is created, and each step assigns the next item to the **target list** (using [assignment](../../simple-statements/assignment-statements/index.md) rules) before running the suite. An optional **`else`** runs when the iterator is exhausted **without** **`break`**. See [docs.python.org](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement).

Parent: [Compound statements](../index.md)

---

## Grammar and evaluation order

| Step | Behavior |
|------|----------|
| Evaluate `starred_expression_list` once | Must yield an iterable |
| Create iterator | Protocol: `__iter__` / `__next__` |
| Each iteration | Assign next value to `target_list`, run suite |
| After exhaustion | Run `else` suite if present and no `break` |
| Loop variable lifetime | Names in `target_list` remain bound; empty iterable may leave them unassigned |

```ebnf
for_stmt ::= "for" target_list "in" starred_expression_list ":" suite
             ["else" ":" suite]
```

**Changed in 3.11:** starred elements are allowed in the `in` expression list.

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer `for x in iterable` over `while` + manual indexing | Uses iterator protocol directly |
| Use `enumerate` when you need indices | Avoid `range(len(...))` when unnecessary |
| Treat assignments in the suite as overwritten each iteration | `i = 5` inside `for i in range(10)` does not change the loop |
| Use `break` when searching; let `else` mean “not found” | Idiomatic search pattern |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Expecting `else` after `break` | `else` skipped on `break` | Remember “completed normally” semantics |
| Reusing a consumed iterator | Second `for` sees nothing | Call `iter()` again or rebuild the iterable |
| Mutating while iterating a list | Skips elements or surprises | Iterate a copy or collect indices first |
| Unpacking wrong arity | `ValueError` at runtime | Match pattern width to iterable items |

```python
# Goal: suite assignment does not affect next iteration value
seen = []
for i in range(4):
    i = 99
    seen.append(i)
assert seen == [99, 99, 99, 99]
```

```python
# Goal: for-else signals "no break" (search miss)
def find_first(pairs, key):
    for k, v in pairs:
        if k == key:
            return v
    else:
        return None


rows = [("a", 1), ("b", 2)]
assert find_first(rows, "b") == 2
assert find_first(rows, "z") is None
```

```python
# Goal: starred expression in "in" (3.11+)
parts = [0, 1, 2, 3, 4]
total = 0
for *middle, last in [parts]:
    total = sum(middle) + last
assert total == sum(parts)
```
