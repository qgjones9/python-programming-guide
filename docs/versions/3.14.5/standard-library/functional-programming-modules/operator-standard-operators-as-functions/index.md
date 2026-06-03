# [operator — Standard operators as functions](https://docs.python.org/3/library/operator.html)

The [`operator`](https://docs.python.org/3/library/operator.html) module exports **C-speed equivalents** of Python's intrinsic operators and helpers for attribute/item/method access. Use them as arguments to `map`, `filter`, `sorted`, `itertools.groupby`, and `functools.reduce` when lambdas would add overhead. Names mirror special methods without dunder prefixes (`add` not `__add__`). Full operator-to-syntax mapping is on [docs.python.org](https://docs.python.org/3/library/operator.html).

---

## Comparisons and logic

| Function | Equivalent |
|----------|------------|
| `lt`, `le`, `eq`, `ne`, `ge`, `gt` | Rich comparisons `<`, `<=`, `==`, … |
| `not_(obj)` | `not obj` |
| `truth(obj)` | `bool(obj)` |
| `is_(a, b)` / `is_not(a, b)` | Identity tests |
| `is_none(a)` / `is_not_none(a)` | `a is None` / `a is not None` (3.14+) |

Rich comparison functions may return any value (not strictly `bool`) per operand `__lt__` etc.

```python
# Goal: sort and filter with operator functions
import operator

pairs = [(3, "c"), (1, "a"), (2, "b")]
assert sorted(pairs, key=operator.itemgetter(0)) == [
    (1, "a"), (2, "b"), (3, "c")
]
assert list(filter(operator.truth, [0, "", "x", None])) == ["x"]
assert operator.is_not(None, 0) is True
```

---

## Arithmetic and bitwise

| Category | Examples |
|----------|----------|
| Arithmetic | `add`, `sub`, `mul`, `matmul`, `truediv`, `floordiv`, `mod`, `pow`, `neg`, `pos`, `abs` |
| Bitwise | `and_`, `or_`, `xor`, `invert`, `lshift`, `rshift` |
| Sequence | `concat`, `contains`, `countOf`, `indexOf`, `getitem`, `setitem`, `delitem` |
| Callable | `call(obj, *args, **kwargs)` (3.11+) |

```python
# Goal: reduce and membership via operator functions
import functools
import operator

total = functools.reduce(operator.add, [1, 2, 3, 4])
assert total == 10

assert operator.pow(2, 5) == 32
assert operator.contains("hello", "ell") is True  # note: b in a
```

---

## Getters — [`itemgetter`](https://docs.python.org/3/library/operator.html#operator.itemgetter), [`attrgetter`](https://docs.python.org/3/library/operator.html#operator.attrgetter), [`methodcaller`](https://docs.python.org/3/library/operator.html#operator.methodcaller)

Fast field extractors for sorting and grouping:

| Factory | Returns |
|---------|---------|
| `itemgetter(i)` / `itemgetter(a, b, …)` | Index/slice lookup; tuple for multiple |
| `attrgetter("name")` / `attrgetter("a.b")` | Attribute; dotted paths |
| `methodcaller("name", *args, **kw)` | Bound method call on operand |

```python
# Goal: sort inventory and read nested attributes
import operator

inventory = [("pear", 5), ("apple", 3), ("banana", 2)]
by_qty = sorted(inventory, key=operator.itemgetter(1))
assert by_qty[0][0] == "banana"

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def sum(self):
        return self.x + self.y

pts = [Point(1, 2), Point(3, 4)]
assert list(map(operator.attrgetter("x"), pts)) == [1, 3]
assert operator.methodcaller("sum")(pts[0]) == 3
```

---

## In-place operators — [In-place Operators](https://docs.python.org/3/library/operator.html#in-place-operators)

`iadd`, `imul`, `iand`, etc. call in-place methods (`+=`, `*=`, …). For **immutable** targets the updated value is returned but **not** assigned back; for **mutable** targets the object is updated in place.

```python
# Goal: in-place list extend vs immutable no-op assignment
import operator

mutable = [1, 2, 3]
operator.iadd(mutable, [4, 5])
assert mutable == [1, 2, 3, 4, 5]

immutable = "hello"
result = operator.iadd(immutable, " world")
assert result == "hello world"
assert immutable == "hello"
```

---

## Mapping operators — [Mapping Operators to Functions](https://docs.python.org/3/library/operator.html#mapping-operators-to-functions)

The official table maps every syntax form (`a + b`, `seq[i:j]`, `a is b`, …) to its `operator` function. Prefer undecorated names (`add`) over dunder aliases (`__add__`) for readability.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`itemgetter`/`attrgetter`** in hot sort/group paths | C implementation; less bytecode than lambda |
| Remember **`contains(seq, item)`** operand order | Equivalent to `item in seq` |
| Pair with **`functools.reduce`** and **`itertools.accumulate`** | `operator.add`, `mul`, `or_` as fold funcs |
| Use **`methodcaller`** for repeated method names | Cleaner than `lambda o: o.m()` |
| Consult **mapping table** when unsure of name | Covers slices, formatting `%`, matrix `@` |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `contains(a, b)` argument swap | Wrong membership test | Think `b in a` |
| `iadd` on str expecting binding | Original name unchanged | Assign: `s = iadd(s, suffix)` |
| `attrgetter` on missing attribute | `AttributeError` at call time | Validate objects first |
| Rich compare return non-bool | Surprises in `if operator.lt(a,b)` | Use explicit `bool()` if needed |
| `countOf` / `indexOf` on non-sequence | Type errors | Require sequence protocol |
| Using `call` without checking callable | Runtime errors | Guard with `callable()` |

---

## See also

- [`functools.reduce`](../functools-higher-order-functions-and-operations-on-callable-objects/index.md) — fold with `operator.add`
- [`itertools`](../itertools-functions-creating-iterators-for-efficient-looping/index.md) — `starmap`, `accumulate` with operator funcs
- [`collections`](../data-types/collections-container-datatypes/index.md) — `Counter` vs `countOf` for tallies
