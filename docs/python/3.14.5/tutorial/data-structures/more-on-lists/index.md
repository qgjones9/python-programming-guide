# [More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)

Condensed notes for **§5.1** of [Data Structures](https://docs.python.org/3/tutorial/datastructures.html): mutating methods, **`sort` vs `sorted`**, stacks, queues, and comprehensions. The parent [Data Structures](../index.md) page already walks these APIs in depth—this page is the structural mirror for nested stubs.

```python
# `sort` returns None — it mutates in place; `sorted` returns a new list.
xs = [2, 1]
ys = sorted(xs)
assert ys == [1, 2] and xs == [2, 1]
xs.sort()
assert xs == [1, 2]
```

## Sections in this repo

- [Using Lists as Stacks](using-lists-as-stacks/index.md)
- [Using Lists as Queues](using-lists-as-queues/index.md)
- [List Comprehensions](list-comprehensions/index.md)
- [Nested List Comprehensions](nested-list-comprehensions/index.md)

Parent: [Data Structures](../index.md)
