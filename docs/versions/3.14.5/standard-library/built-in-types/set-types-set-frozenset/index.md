# [Set Types — set, frozenset](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)

**Sets** are **unordered collections of distinct hashable objects**. They excel at membership tests, deduplicating sequences, and mathematical operations (intersection, union, difference, symmetric difference). Full specification remains on [docs.python.org](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset); this page explains how `set` and `frozenset` fit everyday code.

---

## Role of sets in Python programs

Like other collections, sets support **`x in s`**, **`len(s)`**, and **`for x in s`**. Because they are unordered, sets do **not** record insertion order for indexing purposes and do **not** support indexing, slicing, or other sequence-like behavior.

Common patterns:

| Task | Typical approach |
|------|------------------|
| Fast membership | `if tag in tags:` |
| Remove duplicates | `unique = list(dict.fromkeys(items))` or `set(items)` when order does not matter |
| Tag / category algebra | `required & installed`, `installed - required` |
| Nested sets | Inner sets must be **`frozenset`** (hashable) |

For other containers see built-in [`dict`](../mapping-types-dict/index.md), [`list`](../sequence-types-list-tuple-range/index.md), and [`tuple`](../sequence-types-list-tuple-range/index.md), plus the [**`collections`**](https://docs.python.org/3/library/collections.html) module.

Set elements, like dictionary keys, must be **hashable** (immutable or otherwise hash-stable).

---

## `set` vs `frozenset`

Python provides two built-in set types:

| Type | Mutability | Hashable | Use when |
|------|------------|----------|----------|
| **`set`** | Mutable (`add`, `remove`, in-place updates) | No | Working set you change in place |
| **`frozenset`** | Immutable | Yes | Dict keys, elements of other sets, hash-stable snapshots |

```python
mutable = {'a', 'b'}
mutable.add('c')
assert mutable == {'a', 'b', 'c'}

frozen = frozenset('ab')
d = {frozen: 1}
nested = {frozenset('xy'), frozenset('z')}
assert d[frozen] == 1 and len(nested) == 2
```

Binary operations that mix `set` and `frozenset return the type of the **first** operand—for example `frozenset('ab') | set('bc')` is a `frozenset`.

Sets and frozensets are **generic** over the type of their elements (3.9+).

---

## Creating sets

Non-empty **mutable** sets can be built with **`{…}`** literals (not available for `frozenset`):

| Form | Example |
|------|---------|
| Literal | `{'jack', 'sjoerd'}` |
| Set comprehension | `{c for c in 'abracadabra' if c not in 'abc'}` |
| Constructor | `set()`, `set('foobar')`, `set(['a', 'b', 'foo'])` |
| `frozenset` constructor | `frozenset('abc')`, `frozenset([1, 2, 2])` → `{1, 2}` |

```python
assert set('foobar') == {'f', 'o', 'b', 'a', 'r'}
assert {c for c in 'abracadabra' if c not in 'abc'} == {'r', 'd'}
assert frozenset([1, 2, 2]) == frozenset({1, 2})
```

!!! note
    **`{}`** creates an empty **`dict`**, not a set. Use **`set()`** for an empty set.

---

## Constructors — [`set`](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset) and [`frozenset`](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)

### `set(iterable=(), /)` · `frozenset(iterable=(), /)`

Return a new set or frozenset whose elements come from *iterable*. Elements must be hashable. To represent sets of sets, inner sets must be `frozenset` objects. With no *iterable*, return a new empty set (or empty frozenset).

```python
assert set() == set([])
assert set(['a', 'b', 'foo']) == {'a', 'b', 'foo'}
inner = frozenset('ab')
assert set([inner, frozenset('cd')]) == {inner, frozenset('cd')}
```

---

## Operations on `set` and `frozenset` (reference)

Both types share the operations below. Methods that **mutate** a set are listed in a [later section](#mutable-set-only-operations); `frozenset` provides only the non-mutating API.

| Operation | Category | Typical use |
|-----------|----------|-------------|
| [`len(s)`](#len-and-membership) | Size and membership | Cardinality and containment tests |
| [`x in s` / `x not in s`](#len-and-membership) | Size and membership | Cardinality and containment tests |
| [`isdisjoint()`](#setisdisjoint) | Set relations | Test whether two sets share no elements |
| [`issubset()` / `<=` / `<`](#setissubset) | Set relations | Subset and proper-subset tests |
| [`issuperset()` / `>=` / `>`](#setissuperset) | Set relations | Superset and proper-superset tests |
| [`union()` / `\|`](#setunion) | Non-destructive algebra | Combine all elements |
| [`intersection()` / `&`](#setintersection) | Non-destructive algebra | Elements in every operand |
| [`difference()` / `-`](#setdifference) | Non-destructive algebra | Elements in self but not others |
| [`symmetric_difference()` / `^`](#setsymmetric_difference) | Non-destructive algebra | Elements in exactly one operand |
| [`copy()`](#setcopy) | Non-destructive algebra | Shallow copy |

!!! note
    Non-operator methods (`union()`, `intersection()`, …) accept **any iterable**. Operator forms (`&`, `|`, …) require **set** operands—prefer `set('abc').intersection('cba')` over error-prone `set('abc') & 'cba'`.

---

### Size and membership

<a id="len-and-membership"></a>

**`len(s)`** — number of elements (cardinality).

**`x in s`** / **`x not in s`** — membership test.

```python
s = {'jack', 'sjoerd'}
assert len(s) == 2
assert 'jack' in s and 'guido' not in s
```

---

### Set relations

<a id="setisdisjoint"></a>

### `set.isdisjoint(other, /)` · `frozenset.isdisjoint(other, /)`

Return `True` if the set has no elements in common with *other* (equivalently, intersection is empty).

```python
assert set('ab').isdisjoint(set('cd'))
assert not set('abc').isdisjoint(set('c'))
```

<a id="setissubset"></a>

### `set.issubset(other, /)` · `frozenset.issubset(other, /)` · `set <= other` · `set < other`

**`issubset`** / **`<=`** — every element of the set is in *other*. **`<`** — proper subset (`<=` and not equal).

```python
assert set('ab') <= set('abc')
assert set('ab') < set('abc')
assert not set('abc') < set('abc')
```

<a id="setissuperset"></a>

### `set.issuperset(other, /)` · `frozenset.issuperset(other, /)` · `set >= other` · `set > other`

**`issuperset`** / **`>=`** — every element of *other* is in the set. **`>`** — proper superset.

```python
assert set('abc') >= set('ab')
assert set('abc') > set('ab')
```

---

### Non-destructive set algebra

Methods in this group return a **new** set (or frozenset); operands are unchanged.

<a id="setunion"></a>

### `set.union(*others)` · `frozenset.union(*others)` · `set | other | …`

Return a new set with elements from the set and all *others*.

```python
assert set('ab') | set('bc') == set('abc')
assert set('ab').union('cba') == set('abc')
```

<a id="setintersection"></a>

### `set.intersection(*others)` · `frozenset.intersection(*others)` · `set & other & …`

Return a new set with elements common to the set and all *others*.

```python
assert set('abc') & set('cdef') == set('c')
assert set('abc').intersection('cba') == set('abc')
```

<a id="setdifference"></a>

### `set.difference(*others)` · `frozenset.difference(*others)` · `set - other - …`

Return a new set with elements in the set that are not in the others.

```python
assert set('abcd') - set('cdef') == set('ab')
assert set('abcd').difference('cdef') == set('ab')
```

<a id="setsymmetric_difference"></a>

### `set.symmetric_difference(other, /)` · `frozenset.symmetric_difference(other, /)` · `set ^ other`

Return a new set with elements in either operand but not both.

```python
assert set('abcd') ^ set('cdef') == set('abef')
assert set('abcd').symmetric_difference(set('cdef')) == set('abef')
```

<a id="setcopy"></a>

### `set.copy()` · `frozenset.copy()`

Return a shallow copy of the set.

```python
original = {1, 2}
duplicate = original.copy()
duplicate.add(3)
assert original == {1, 2} and duplicate == {1, 2, 3}
```

---

## Set comparisons and ordering

Both `set` and `frozenset` support **set-to-set comparisons**:

- **Equal** iff each is a subset of the other (same members).
- **Less than** iff proper subset; **greater than** iff proper superset.

`set` and `frozenset` compare by **members**, not type—for example `set('abc') == frozenset('abc')` is `True`, and `set('abc') in {frozenset('abc')}` is `True`.

Subset relations define only a **partial** order: two non-empty disjoint sets are neither equal nor subsets of each other, so `<`, `==`, and `>` can all be false. **`list.sort()`** on a list of sets is therefore **undefined**.

```python
a, b = set('ab'), set('cd')
assert not (a < b or a == b or a > b)
assert set('abc') == frozenset('abc')
```

---

## Mutable `set`-only operations

These methods exist on **`set`** but not on immutable **`frozenset`**. In-place forms mutate the set and return **`None`**.

| Method | Operator | Effect |
|--------|----------|--------|
| [`update()`](#setupdate) | `\|=` | Add all elements from *others* |
| [`intersection_update()`](#setintersection_update) | `&=` | Keep only elements also in *others* |
| [`difference_update()`](#setdifference_update) | `-=` | Remove elements found in *others* |
| [`symmetric_difference_update()`](#setsymmetric_difference_update) | `^=` | Keep elements in exactly one of the sets |
| [`add()`](#setadd) | — | Add one element |
| [`remove()`](#setremove) | — | Remove element; **`KeyError`** if missing |
| [`discard()`](#setdiscard) | — | Remove element if present |
| [`pop()`](#setpop) | — | Remove and return arbitrary element |
| [`clear()`](#setclear) | — | Remove all elements |

Non-operator update methods accept **any iterable**, like their read-only counterparts.

!!! note
    The *elem* argument to **`__contains__`**, **`remove()`**, and **`discard()`** may be a **set**; to match an equivalent **`frozenset`**, a temporary frozenset is built from *elem*.

---

### In-place updates

<a id="setupdate"></a>

### `set.update(*others)` · `set |= other | …`

Update the set, adding elements from all *others*.

```python
s = set('ab')
s.update('bc')
assert s == set('abc')
```

<a id="setintersection_update"></a>

### `set.intersection_update(*others)` · `set &= other & …`

Update the set, keeping only elements found in it and all *others*.

```python
s = set('abcd')
s &= set('cdef')
assert s == set('cd')
```

<a id="setdifference_update"></a>

### `set.difference_update(*others)` · `set -= other | …`

Update the set, removing elements found in *others*.

```python
s = set('abcd')
s -= set('cdef')
assert s == set('ab')
```

<a id="setsymmetric_difference_update"></a>

### `set.symmetric_difference_update(other, /)` · `set ^= other`

Update the set, keeping only elements found in exactly one of the two sets.

```python
s = set('abcd')
s ^= set('cdef')
assert s == set('abef')
```

---

### Element add and remove

<a id="setadd"></a>

### `set.add(elem, /)`

Add *elem* to the set.

```python
s = set()
s.add(42)
assert s == {42}
```

<a id="setremove"></a>

### `set.remove(elem, /)`

Remove *elem* from the set. Raises **`KeyError`** if *elem* is not present.

```python
s = {1, 2}
s.remove(2)
assert s == {1}
```

<a id="setdiscard"></a>

### `set.discard(elem, /)`

Remove *elem* from the set if it is present (no error if missing).

```python
s = {1}
s.discard(99)
s.discard(1)
assert s == set()
```

<a id="setpop"></a>

### `set.pop()`

Remove and return an **arbitrary** element. Raises **`KeyError`** if the set is empty.

```python
s = {99}
assert s.pop() == 99
assert len(s) == 0
```

<a id="setclear"></a>

### `set.clear()`

Remove all elements from the set.

```python
s = {1, 2, 3}
s.clear()
assert s == set()
```

---

## Related topics in this guide

| Subject | Description |
|---------|-------------|
| [Mapping Types — dict](../mapping-types-dict/index.md) | Another hashable-key container; compare dict keys with set membership. |
| [Sequence Types — list, tuple, range](../sequence-types-list-tuple-range/index.md) | Ordered collections; dedupe sequences into sets when order is irrelevant. |
| [Truth Value Testing](../truth-value-testing/index.md) | Empty sets are falsy; non-empty sets are truthy. |

**See also:** [Thread safety for set objects](https://docs.python.org/3/library/stdtypes.html#thread-safety-for-set-objects) in the free-threaded build.
