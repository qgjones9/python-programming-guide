# [Tuples](https://docs.python.org/3/library/stdtypes.html#tuples)

Tuples are **immutable sequences** in Python, commonly used for:

- Storing collections of **heterogeneous data** (such as the pairs returned by the `enumerate()` function).
- Cases where an immutable, fixed-length collection is needed (e.g., as a key in a `dict`, in a `set`, or for data that must not change).

---

## Tuple Construction

**Definition:**  
```python
class tuple(iterable=(), /)
```

You can create tuples with several standard methods:

- **Empty tuple:**  
  ```python
  empty = ()
  ```

- **Singleton tuple (one item):**  
  ```python
  single = a,
  single = (a,)
  ```

- **Multiple items:**  
  ```python
  t = a, b, c
  t = (a, b, c)
  ```

- **From an iterable object:**  
  ```python
  tuple('abc')         # ('a', 'b', 'c')
  tuple([1, 2, 3])     # (1, 2, 3)
  tuple()              # ()
  ```

> **Note:**  
> It is the **comma** that forms a tuple in Python, not the parentheses. Parentheses are only required to disambiguate expressions or to denote an empty tuple:
> 
> - `f(a, b, c)` – function call with 3 arguments
> - `f((a, b, c))` – function call with a single tuple argument

If an `iterable` is provided to the tuple constructor, its items are used (in order) to populate the new tuple. If the argument is already a tuple, it is returned unchanged. An empty call (`tuple()`) produces an empty tuple: `()`.

---

## Tuple Characteristics

- Tuples **implement all common sequence operations** (see [Common Sequence Operations](../common-sequence-operations/index.md)).
- Tuples are **generic** over the types of their contents — for more on this, see the Python typing documentation.
- For *heterogeneous* records, where field names are desired, [`collections.namedtuple()`](https://docs.python.org/3/library/collections.html#collections.namedtuple) may be a better fit than a plain tuple.

---