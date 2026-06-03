# [Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)

A **mapping** associates **hashable keys** with arbitrary values. Python’s built-in **`dict`** is the standard mutable mapping type. Full specification remains on [docs.python.org](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict); this page explains how dictionaries fit everyday code.

---

## Role of `dict` in Python programs

Dictionaries are the default **key–value store**: JSON-like records, caches, registries, keyword arguments, and object `__dict__` attributes all build on the same model.

| Task | Typical approach |
|------|------------------|
| Named fields | `user = {'name': 'Ada', 'id': 42}` |
| Counting / grouping | `counts[key] = counts.get(key, 0) + 1` |
| Config overrides | `defaults \|= user_settings` (3.9+) |
| Unique keys with order | Iterate `d` or `d.keys()` — insertion order is preserved (3.7+) |

For other containers see [`list`](../sequence-types-list-tuple-range/index.md), [`set`](../set-types-set-frozenset/index.md), and [`tuple`](../sequence-types-list-tuple-range/index.md), plus the [**`collections`**](https://docs.python.org/3/library/collections.html) module (`defaultdict`, `Counter`, `OrderedDict` is largely redundant since 3.7).

---

## Dictionary keys

Keys must be **hashable**. Lists, dicts, and other mutable containers cannot be keys because they are compared by value and may change.

Values that **compare equal** index the **same** slot—for example `1`, `1.0`, and `True` are interchangeable as keys:

```python
d = {}
d[1] = 'one'
assert d[1.0] == d[True] == 'one'
```

Keyword-argument forms of `dict()` (`dict(foo=1)`) only work when keys are valid **Python identifiers**; use literals or two-element iterables for other keys (for example `(4098, 'jack')`).

Dictionaries compare **equal** iff they have the same `(key, value)` pairs regardless of insertion order. Ordering comparisons (`<`, `<=`, `>=`, `>`) raise **`TypeError`**.

Dictionaries are **generic** over key and value types (3.9+).

---

## Creating dictionaries

| Form | Example |
|------|---------|
| Literal | `{'jack': 4098, 'sjoerd': 4127}` or `{4098: 'jack'}` |
| Dict comprehension | `{x: x ** 2 for x in range(10)}` |
| Constructor | `dict()`, `dict([('foo', 100), ('bar', 200)])`, `dict(foo=100, bar=200)` |
| Empty literal | `{}` (empty **dict**, not a set) |

```python
target = {"one": 1, "two": 2, "three": 3}
assert dict(one=1, two=2, three=3) == target
assert {'one': 1, 'two': 2, 'three': 3} == target
assert dict(zip(['one', 'two', 'three'], [1, 2, 3])) == target
assert dict([('two', 2), ('one', 1), ('three', 3)]) == target
assert dict({'three': 3, 'one': 1, 'two': 2}) == target
assert dict({'one': 1, 'three': 3}, two=2) == target
```

With no positional argument, `dict()` returns `{}`. With a **mapping** positional argument (object with `keys()`), keys come from `keys()` and values from `mapping[key]`. With an **iterable** of pairs, each pair supplies one key and value; duplicate keys keep the **last** value. Keyword arguments merge afterward and override positional keys.

---

## Constructor — [`dict`](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)

### `dict(**kwargs)` · `dict(mapping, /, **kwargs)` · `dict(iterable, /, **kwargs)`

Return a new dictionary from an optional positional argument plus optional keyword arguments.

```python
assert dict() == {}
assert dict([('a', 1), ('b', 2)]) == {'a': 1, 'b': 2}
assert dict({'x': 1}, y=2) == {'x': 1, 'y': 2}
```

---

## Insertion order

Since 3.7, dict order is guaranteed to match **insertion order** (CPython 3.6 implementation detail). **Updating** an existing key does **not** move it. **Re-inserting** a key after deletion appends it at the **end**.

```python
d = {"one": 1, "two": 2, "three": 3, "four": 4}
assert list(d) == ['one', 'two', 'three', 'four']
d["one"] = 42
assert list(d) == ['one', 'two', 'three', 'four']
del d["two"]
d["two"] = None
assert list(d) == ['one', 'three', 'four', 'two']
```

> **Changed in version 3.7:** Guaranteed insertion order.

---

## Dictionary operations (reference)

Custom mapping types should implement the same protocol where practical.

| Operation | Category | Typical use |
|-----------|----------|-------------|
| [`list(d)` / `len(d)` / `iter(d)`](#size-and-iteration) | Size and iteration | Keys snapshot, count, iterate keys |
| [`d[key]` / `d[key] = v` / `del d[key]`](#item-access) | Item access | Read, write, delete by key |
| [`key in d`](#membership) | Membership | Test whether a key exists |
| [`get()`](#dictget) | Safe lookup | Read with default, no `KeyError` |
| [`setdefault()`](#dictsetdefault) | Upsert | Insert default value if key missing |
| [`keys()` / `values()` / `items()`](#dictkeys) | Views | Live views over keys, values, pairs |
| [`clear()` / `pop()` / `popitem()`](#dictclear) | Remove items | Empty dict or extract entries |
| [`copy()` / `fromkeys()`](#dictcopy) | Copy and factory | Shallow copy; keys with shared default |
| [`update()`](#dictupdate) | Bulk update | Merge mapping, pairs, or kwargs |
| [`d \| other` / `d \|= other`](#dict-merge-operators) | Merge (3.9+) | Combine dicts; right-hand wins on conflict |
| [`reversed(d)`](#dict-reversal) | Reverse iteration | Walk keys in reverse insertion order (3.8+) |

---

### Size and iteration

<a id="size-and-iteration"></a>

**`list(d)`** — list of all keys (insertion order).

**`len(d)`** — number of key–value pairs.

**`iter(d)`** — iterator over keys; equivalent to `iter(d.keys())`.

```python
d = {'a': 1, 'b': 2}
assert list(d) == ['a', 'b']
assert len(d) == 2
assert list(iter(d)) == ['a', 'b']
```

---

### Item access

<a id="item-access"></a>

**`d[key]`** — value for *key*; raises **`KeyError`** if missing (unless subclass defines **`__missing__`**).

**`d[key] = value`** — bind *key* to *value*.

**`del d[key]`** — remove *key*; raises **`KeyError`** if missing.

If a **`dict` subclass** defines **`__missing__(key)`**, a missing **`d[key]`** lookup calls that method and returns (or raises) its result. No other dict operation invokes **`__missing__`**. The hook must be a **method**, not an instance variable—see [`collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) and [`collections.defaultdict`](https://docs.python.org/3/library/collections.html#collections.defaultdict).

```python
class Counter(dict):
    def __missing__(self, key):
        return 0

c = Counter()
assert c['red'] == 0
c['red'] += 1
assert c['red'] == 1
```

---

### Membership

<a id="membership"></a>

**`key in d`** — `True` if *key* is present.

**`key not in d`** — negated membership.

```python
d = {'x': 1}
assert 'x' in d and 'y' not in d
```

---

### Safe lookup and upsert

<a id="dictget"></a>

### `dict.get(key, default=None, /)`

Return the value for *key* if present; otherwise *default* (or `None`). Never raises **`KeyError`**.

```python
d = {'name': 'Python'}
assert d.get('version') is None
assert d.get('version', 3) == 3
```

<a id="dictsetdefault"></a>

### `dict.setdefault(key, default=None, /)`

If *key* is present, return its value. Otherwise insert *key* with *default* and return *default*.

```python
d = {'name': 'Python'}
assert d.setdefault('version', 3) == 3
assert d.setdefault('name', 'Other') == 'Python'
assert d == {'name': 'Python', 'version': 3}
```

---

### Views

<a id="dictkeys"></a>

### `dict.keys()` · `dict.values()` · `dict.items()`

Return **view objects** — dynamic, set-like (for keys/items) windows on the dict. See [Dictionary view objects](#dictionary-view-objects) below.

!!! note
    **`dict.values()`** views never compare equal—even `d.values() == d.values()` is **`False`**.

```python
d = {'a': 1}
assert (d.values() == d.values()) is False
assert list(d.keys()) == ['a']
assert list(d.items()) == [('a', 1)]
```

---

### Remove items

<a id="dictclear"></a>

### `dict.clear()`

Remove all items.

### `dict.pop(key, /)` · `dict.pop(key, default, /)`

Remove *key* and return its value, or *default* if *key* is missing. Without *default*, missing keys raise **`KeyError`**.

### `dict.popitem()`

Remove and return a **`(key, value)`** pair in **LIFO** (last-in, first-out) insertion order. Raises **`KeyError`** on an empty dict. Useful for destructive iteration in graph/set algorithms.

```python
d = {'x': 10, 'y': 20}
assert d.pop('x') == 10
assert d.pop('missing', None) is None

d = {'a': 1, 'b': 2}
assert d.popitem() == ('b', 2)
assert d.popitem() == ('a', 1)
```

> **Changed in version 3.7:** `popitem()` LIFO order is guaranteed.

---

### Copy and factory

<a id="dictcopy"></a>

### `dict.copy()`

Return a **shallow** copy.

### `dict.fromkeys(iterable, value=None, /)` (classmethod)

New dict with keys from *iterable* and every value set to *value* (default `None`). All keys share the **same** value object—avoid mutable defaults; use a comprehension for independent values.

```python
original = {'a': [1]}
copy = original.copy()
copy['a'].append(2)
assert original == copy  # shallow: nested list is shared

shared = dict.fromkeys(['a', 'b'], [])
shared['a'].append(1)
assert shared == {'a': [1], 'b': [1]}

distinct = {k: [] for k in ['a', 'b']}
distinct['a'].append(1)
assert distinct == {'a': [1], 'b': []}
```

---

### Bulk update

<a id="dictupdate"></a>

### `dict.update(**kwargs)` · `dict.update(mapping, /, **kwargs)` · `dict.update(iterable, /, **kwargs)`

Merge key–value pairs from a mapping (via `keys()` + `__getitem__`), an iterable of pairs, and/or keyword arguments. Existing keys are **overwritten**. Returns **`None`**.

```python
d = {'a': 1}
d.update([('b', 2)], c=3, red=1, blue=2)
assert d == {'a': 1, 'b': 2, 'c': 3, 'red': 1, 'blue': 2}
```

---

### Merge operators (3.9+)

<a id="dict-merge-operators"></a>

**`d | other`** — new dict with merged keys; *other*’s values win on conflict. Both operands must be **`dict`** instances.

**`d |= other`** — in-place merge; *other* may be a **mapping** or iterable of pairs.

```python
base = {'a': 1, 'b': 2}
overlay = {'b': 99, 'c': 3}
assert base | overlay == {'a': 1, 'b': 99, 'c': 3}

d = {'a': 1}
d |= {'a': 2, 'b': 3}
assert d == {'a': 2, 'b': 3}
```

> **Added in version 3.9.**

---

### Reverse iteration (3.8+)

<a id="dict-reversal"></a>

**`reversed(d)`** — reverse iterator over keys (`reversed(d.keys())`). Dicts and their views are **reversible**.

```python
d = {"one": 1, "two": 2, "three": 3, "four": 4}
assert list(reversed(d)) == ['four', 'three', 'two', 'one']
assert list(reversed(d.values())) == [4, 3, 2, 1]
assert list(reversed(d.items())) == [
    ('four', 4), ('three', 3), ('two', 2), ('one', 1),
]
```

> **Changed in version 3.8:** Dictionaries and dict views are reversible.

---

## [Dictionary view objects](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)

**`keys()`**, **`values()`**, and **`items()`** return **view objects**: live windows on the dict that update when the dict changes.

| View operation | Behavior |
|----------------|----------|
| `len(dictview)` | Number of entries |
| `iter(dictview)` | Iterate keys, values, or `(key, value)` pairs in insertion order |
| `x in dictview` | Membership (`items` views expect `(key, value)` tuples) |
| `reversed(dictview)` | Reverse insertion order (3.8+) |
| `dictview.mapping` | Read-only [`MappingProxyType`](https://docs.python.org/3/library/types.html#types.MappingProxyType) wrapper (3.10+) |

**Keys** views are **set-like** (unique hashable members). **Items** views support set algebra when values are hashable. **Values** views are not set-like (values may repeat). Set operators on views accept **any iterable** as the other operand.

Iterating a view while **adding or deleting** dict entries may raise **`RuntimeError`** or skip entries—avoid mutating the dict during iteration.

```python
dishes = {'eggs': 2, 'sausage': 1, 'bacon': 1, 'spam': 500}
keys = dishes.keys()
values = dishes.values()
assert sum(values) == 504
assert list(keys) == ['eggs', 'sausage', 'bacon', 'spam']

del dishes['eggs']
del dishes['sausage']
assert list(keys) == ['bacon', 'spam']
assert keys & {'eggs', 'bacon', 'salad'} == {'bacon'}
assert keys ^ {'sausage', 'juice'} == {'juice', 'sausage', 'bacon', 'spam'}
assert keys | {'juice', 'juice', 'juice'} == {'bacon', 'spam', 'juice'}
assert values.mapping['spam'] == 500
```

> **Added in version 3.10:** `dictview.mapping`.

---

## Related topics in this guide

| Subject | Description |
|---------|-------------|
| [Set Types — set, frozenset](../set-types-set-frozenset/index.md) | Hashable unique elements; dict keys share hashability rules with set elements. |
| [Comparisons](../comparisons/index.md) | Dict equality vs ordering; `is` vs `==` for objects used as values. |
| [Truth Value Testing](../truth-value-testing/index.md) | Empty `{}` is falsy; non-empty dicts are truthy. |

**See also:** [`types.MappingProxyType`](https://docs.python.org/3/library/types.html#types.MappingProxyType) for a read-only dict proxy; [Thread safety for dict objects](https://docs.python.org/3/library/stdtypes.html#thread-safety-for-dict-objects) in the free-threaded build.
