# [Data Structures](https://docs.python.org/3/tutorial/datastructures.html)

Condensed notes for [chapter 5 — Data Structures](https://docs.python.org/3/tutorial/datastructures.html): lists (including stacks, queues, comprehensions), `del`, tuples, sets, dictionaries, looping idioms, comparisons, and sequence ordering. Each **§** heading below links to the matching subsection on docs.python.org (`datastructures.html#…`). For full narrative and edge cases, follow those links or the chapter H1.

### 5.1 — [More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)

- **Mutating methods:** `append`, `extend`, `insert`, `remove`, `pop`, `clear`, `sort` (in-place), `reverse`, `copy`.
- **`sort`** accepts `key=` and `reverse=`; for a new sorted list without mutating the original, use **`sorted(iterable)`**.
- **Count / find:** `list.count(x)`, `list.index(value)` (raises `ValueError` if missing).

```python
# List methods mutate the same object in place (except where noted).

xs = [1, 2, 3]
xs.append(4)  # add one element at the end
assert xs == [1, 2, 3, 4]

xs.extend([5, 6])  # append each element from another iterable
assert xs[-2:] == [5, 6]

xs.insert(0, 0)  # insert before index 0
assert xs[0] == 0

xs.remove(0)  # remove first occurrence of value 0
assert 0 not in xs

last = xs.pop()  # remove and return last item (default index -1)
assert last == 6 and xs[-1] == 5

ys = [3, 1, 4, 1, 5]
ys.sort()  # in-place ascending sort
assert ys == [1, 1, 3, 4, 5]
# sorted() returns a new list; the original ys is unchanged by sorted().
assert sorted(ys, reverse=True) == [5, 4, 3, 1, 1] and ys == [1, 1, 3, 4, 5]

zs = ["bb", "aaa", "c"]
zs.sort(key=len)  # order by string length, not alphabetically
assert zs == ["c", "bb", "aaa"]
```

### 5.1.1 — [Using Lists as Stacks](https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-stacks)

- **LIFO:** push with **`append`**, pop with **`pop()`** from the end (amortized O(1)).

```python
# Stack: last item in is first out (LIFO) — use end of list as the "top".
stack: list[int] = []
stack.append(1)  # push
stack.append(2)
assert stack.pop() == 2 and stack == [1]  # pop from top
```

### 5.1.2 — [Using Lists as Queues](https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-queues)

- Popping from index **0** on a list is **O(n)** because elements shift. For a real FIFO queue, prefer **`collections.deque`**.

```python
# FIFO queue: deque supports fast appends and pops from both ends.
from collections import deque

q: deque[int] = deque([1, 2, 3])
q.append(4)  # enqueue at right end
assert q.popleft() == 1 and list(q) == [2, 3, 4]  # dequeue from left — O(1)
```

### 5.1.3 — [List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)

- Compact way to build lists: **`[expr for target in iterable if condition]`**.

```python
# List comprehension: [expression for variable in iterable optional_if_filter].

squares = [x * x for x in range(6)]  # square every x from 0..5
assert squares == [0, 1, 4, 9, 16, 25]

even_squares = [x * x for x in range(6) if x % 2 == 0]  # filter keeps even x only
assert even_squares == [0, 4, 16]
```

### 5.1.4 — [Nested List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#nested-list-comprehensions)

- Loops in comprehension read **left-to-right** like nested `for` loops (outer → inner).

```python
# Nested fors read outer-to-inner, left-to-right in the comprehension.

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [cell for row in matrix for cell in row]  # flatten rows left-to-right
assert flat == list(range(1, 10))

# Inner comprehension runs for each column index i (swap rows/columns).
transposed = [[row[i] for row in matrix] for i in range(3)]
assert transposed == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

### 5.2 — [The del statement](https://docs.python.org/3/tutorial/datastructures.html#the-del-statement)

- **`del`** removes slices from a list, clears elements, or deletes a **name** (not necessarily the object it referred to).

```python
# del removes items from a list (by index or slice) or removes a variable name.

a = list(range(6))  # [0, 1, 2, 3, 4, 5]
del a[0]  # delete single index — following items shift down
assert a[0] == 1

del a[2:4]  # delete slice [2:4), exclusive of upper bound
assert a == [1, 2, 5]

del a[:]  # delete all elements; list becomes empty but name a still exists
assert a == []

b = 42
del b  # unbind name b (do not reference b after this line)
```

### 5.3 — [Tuples and Sequences](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)

- **Tuples** are immutable sequences; **packing** `t = 1, 2, 3` and **unpacking** `a, b, c = t`.
- **Singleton tuple** needs a trailing comma: `(1,)`.

```python
# Tuple packing: commas create tuples. Unpacking assigns parts to names.

t = 1, 2, 3  # same as (1, 2, 3)
a, b, c = t  # length must match: three values → three names
assert (a, b, c) == (1, 2, 3)

# One-element tuple needs a trailing comma — ("x") is just a parenthesized string.
single = ("lonely",)
assert single == ("lonely",) and len(single) == 1

# Tuple unpacking swaps without a temporary variable.
x, y = 10, 20
x, y = y, x
assert (x, y) == (20, 10)
```

### 5.4 — [Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)

- **Unordered** collection of **distinct** elements; set literals `{a, b}`, empty set is **`set()`** (not `{}`, which is a dict).
- **Operations:** union `|`, intersection `&`, difference `-`, symmetric difference `^`.

```python
# Sets: unordered, unique members. Duplicate literals collapse to one element.

a = {1, 2, 3, 3}
assert a == {1, 2, 3}

b = {3, 4, 5}
assert a | b == {1, 2, 3, 4, 5}  # union — in either set
assert a & b == {3}  # intersection — in both
assert a - b == {1, 2}  # difference — in a but not b
assert a ^ b == {1, 2, 4, 5}  # symmetric difference — in exactly one set

# Set comprehension deduplicates while transforming (case-normalize words).
unique_words = {w.lower() for w in ["Hi", "hi", "BYE"]}
assert unique_words == {"hi", "bye"}
```

### 5.5 — [Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)

- **Keys** must be hashable; keys are unique. **`dict`** constructor accepts iterables of pairs.
- **`keys`**, **`values`**, **`items`** views; **dict comprehensions** mirror list comprehensions.

```python
# Dict literal: keys map to values; new key assignment adds or overwrites.

tel = {"guido": 4127, "jack": 4098}
tel["sape"] = 4139  # insert new key
assert tel["guido"] == 4127

# dict() accepts an iterable of (key, value) pairs — here a list of tuples.
built = dict([("a", 1), ("b", 2)])
assert built == {"a": 1, "b": 2}

# Dict comprehension builds {key_expr: value_expr from ...}.
squares_map = {x: x**2 for x in (2, 4, 6)}
assert squares_map[4] == 16

# .keys() / .items() are live "views" on the dict; here we just show they are non-empty.
assert list(tel.keys()) and set(tel.items())
```

### 5.6 — [Looping Techniques](https://docs.python.org/3/tutorial/datastructures.html#looping-techniques)

- **`dict.items()`** for key/value; **`enumerate`** for index + value; **`zip`** to pair iterables; **`reversed`** for reverse order.

```python
# Common iteration helpers when looping over data structures.

knights = {"gallahad": "the pure", "robin": "the brave"}
pairs = sorted(knights.items())  # items() yields (key, value); sort by key
assert pairs[0][0] == "gallahad"

# enumerate(iterable, start=0) attaches an index to each value.
indexed = list(enumerate(["tic", "tac", "toe"]))
assert indexed[1] == (1, "tac")

# zip stops at the shortest iterable — pairs up parallel streams.
zipped = list(zip("abc", range(3)))
assert zipped == [("a", 0), ("b", 1), ("c", 2)]

# reversed() yields values from last to first without copying the whole range.
rev = list(reversed(range(3)))
assert rev == [2, 1, 0]
```

### 5.7 — [More on Conditions](https://docs.python.org/3/tutorial/datastructures.html#more-on-conditions)

- **Chained comparisons:** `a < b == c` is equivalent to `a < b and b == c` (both `b` comparisons use the same `b` value).

```python
# Chained comparisons: a < b < c means (a < b) and (b < c); b is evaluated once.

assert 1 < 2 < 3
x = 5
assert 1 < x < 10  # same as 1 < x and x < 10
```

### 5.8 — [Comparing Sequences and Other Types](https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types)

- **Lexicographic order:** compare element by element; shorter sequence is smaller if it is a prefix of the other. **Types generally do not compare** across unrelated types (Python 3).

```python
# Sequences compare lexicographically: first unequal element decides; shorter prefix loses.

assert (1, 2, 3) < (1, 2, 4)  # 3 < 4 at third position
assert [1, 2] < [1, 2, 3]  # prefix [1,2] is shorter — it is "less"

# Strings are sequences of characters, so they use the same ordering rules.
assert "ABC" < "C" < "Pascal" < "Python"
```

## Sections in this repo

- [More on Lists](more-on-lists/index.md)
  - [Using Lists as Stacks](more-on-lists/using-lists-as-stacks/index.md)
  - [Using Lists as Queues](more-on-lists/using-lists-as-queues/index.md)
  - [List Comprehensions](more-on-lists/list-comprehensions/index.md)
  - [Nested List Comprehensions](more-on-lists/nested-list-comprehensions/index.md)
- [The del statement](the-del-statement/index.md)
- [Tuples and Sequences](tuples-and-sequences/index.md)
- [Sets](sets/index.md)
- [Dictionaries](dictionaries/index.md)
- [Looping Techniques](looping-techniques/index.md)
- [More on Conditions](more-on-conditions/index.md)
- [Comparing Sequences and Other Types](comparing-sequences-and-other-types/index.md)
