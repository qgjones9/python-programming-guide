# [7.2. Assignment statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements)

Notes on **7.2. Assignment statements** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements).

- `(target_list "=")+ expression` binds names or mutates attributes, subscriptions, and slices.
- Sequence unpacking requires matching arity; `*target` collects surplus items (PEP 3132).
- Overlapping targets in one statement are applied **left to right** — e.g. `i, x[i] = 1, 2` can surprise readers.
- See also [7.2.1 Augmented assignment](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) and [7.2.2 Annotated assignment](https://docs.python.org/3/reference/simple_stmts.html#annotated-assignment-statements) on the same page.

```python
# Basic binding and tuple unpacking.
a, b = 1, 2
assert (a, b) == (1, 2)

first, *middle, last = range(5)
assert first == 0 and middle == [1, 2, 3] and last == 4

# Left-to-right overlap within one target list (reference example).
x = [0, 1]
i = 0
i, x[i] = 1, 2
assert i == 1 and x == [0, 2]

# Augmented assignment evaluates the target once before the RHS.
nums = [1, 2, 3]
idx = 1
nums[idx] += 10
assert nums == [1, 12, 3]
```

Parent: [7. Simple statements](../index.md)
